import math
from itertools import islice

from src.db.models import Word
from src.db.uow import SqlAlchemyUnitOfWork
from src.models_pydantic import FileContent, WordScore


class CalculateTFIDFHandler:
    def __init__(self, uow: SqlAlchemyUnitOfWork) -> None:
        self.uow = uow

    async def execute(
        self,
        content: FileContent,
        limit: int = 50,
    ) -> list[WordScore]:
        words = await self._get_or_update_words(content=content)
        count_documents = await self.uow.documents.count()

        collection_words_score: list[WordScore] = []
        for el in islice(words, limit):
            collection_words_score.append(
                WordScore(
                    name=el.name,
                    tf=self.calculate_TF(word=el.name, content=content),
                    idf=self.calculate_IDF(
                        count_documents_with_cur_word=el.count,
                        count_all_documents=count_documents,
                    ),
                )
            )

        return sorted(collection_words_score, key=lambda x: x.idf, reverse=True)

    async def _get_or_update_words(self, content: FileContent) -> list[Word]:
        exist = await self.uow.documents.is_exists(content.content_hash)
        if not exist:
            await self.uow.documents.create(content.content_hash)
            return await self.uow.words.increment(words=set(content.words))

        return await self.uow.words.find(words=content.words)

    @staticmethod
    def calculate_TF(word: str, content: FileContent) -> float:
        return round(content.words[word] / content.count_all_words, 2)

    @staticmethod
    def calculate_IDF(count_documents_with_cur_word: int, count_all_documents: int) -> float:
        return round(math.log(count_all_documents / count_documents_with_cur_word, 10), 2)
