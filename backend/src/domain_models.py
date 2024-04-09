import hashlib
import re
from collections import Counter
from typing import Self

from pydantic import BaseModel
from textblob import TextBlob


class WordScore(BaseModel):
    name: str
    tf: float
    idf: float


class FileContent(BaseModel):
    count_all_words: int
    words: Counter[str]
    content_hash: str

    @classmethod
    def from_content(cls, content: bytes) -> Self:
        words = TextBlob(content.decode()).lower().words
        en_words = [word for word in words if re.match("^[a-z/-]+$", word)]

        return cls(
            count_all_words=len(en_words),
            words=Counter(en_words),
            content_hash=hashlib.md5(content).hexdigest(),
        )
