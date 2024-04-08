from collections.abc import Iterable

from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Document, Word


class DocumentRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data_hash: str) -> None:
        await self.session.execute(insert(Document).values(hash=data_hash))

    async def is_exists(self, data_hash: str) -> bool:
        data = await self.session.scalar(select(Document.hash).where(Document.hash == data_hash))
        return bool(data)

    async def count(self) -> int:
        result = await self.session.scalar(select(func.count(Document.hash)))
        return result or 0


class WordRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find(self, words: Iterable[str]) -> list[Word]:
        exists_words = await self.session.execute(select(Word).where(Word.name.in_(words)))
        return list(exists_words.scalars())

    async def increment(self, words: set[str]) -> list[Word]:
        exists_words_result = await self.session.scalars(
            update(Word)
            .values({"count": Word.count + 1})
            .where(Word.name.in_(words))
            .returning(Word)
        )

        exists_words = sorted(exists_words_result.all(), key=lambda x: x.count)

        not_exists_words = words.copy()
        for word in exists_words:
            not_exists_words.remove(word.name)
        if not not_exists_words:
            return exists_words

        new_words_result = await self.session.scalars(
            insert(Word)
            .values([{"name": word, "count": 1} for word in not_exists_words])
            .returning(Word)
        )
        return list(new_words_result.all()) + exists_words
