from io import BytesIO

from httpx import AsyncClient
from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Document, Word


async def test_add_document(client: AsyncClient, session: AsyncSession) -> None:
    response = await client.post(
        url="/api/documents/", files={"file": ("asd.txt", BytesIO(b"must 123"), "text/plain")}
    )
    assert response.status_code == 200
    assert response.json() == [{"name": "must", "idf": 0.0, "tf": 1.0}]

    words = await session.scalars(select(Word))
    documents = await session.scalars(select(Document))
    assert words.all() == [Word(name="must", count=1)]
    assert documents.all() == [Document(hash="7fefc5473f826628cf170b816dbd75da")]


async def test_add_document_error_txt(client: AsyncClient) -> None:
    response = await client.post(
        url="/api/documents/", files={"file": ("asd.pdf", BytesIO(b"must 123"), "text/plain")}
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "The file must have the extension .txt"}


async def test_add_document_error_type(client: AsyncClient) -> None:
    response = await client.post(
        url="/api/documents/", files={"file": ("asd.txt", BytesIO(b"must 123"), "application/pdf")}
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "MIME type must be: text/plain"}


async def test_add_document_error_size(client: AsyncClient) -> None:
    response = await client.post(
        url="/api/documents/",
        files={"file": ("asd.txt", BytesIO(b"must " * int(10e5)), "text/plain")},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "The file must be no larger than 1 MB in size"}


async def test_add_document_error_coding(client: AsyncClient) -> None:
    response = await client.post(
        url="/api/documents/",
        files={"file": ("asd.txt", BytesIO("must 123".encode("utf-32")), "text/plain")},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "The file encoding must be UTF-8"}


async def test_add_document_where_document_is_exist(
    client: AsyncClient, session: AsyncSession
) -> None:
    await session.execute(insert(Word).values(name="must", count=1))
    await session.execute(insert(Document).values(hash="7fefc5473f826628cf170b816dbd75da"))

    response = await client.post(
        url="/api/documents/", files={"file": ("asd.txt", BytesIO(b"must 123"), "text/plain")}
    )
    assert response.status_code == 200
    assert response.json() == [{"idf": 0.0, "name": "must", "tf": 1}]

    words = await session.scalars(select(Word))
    documents = await session.scalars(select(Document))
    assert words.all() == [Word(name="must", count=1)]
    assert documents.all() == [Document(hash="7fefc5473f826628cf170b816dbd75da")]


async def test_add_document_where_word_is_update(
    client: AsyncClient, session: AsyncSession
) -> None:
    await session.execute(insert(Word).values(name="must", count=1))

    await client.post(
        url="/api/documents/", files={"file": ("asd.txt", BytesIO(b"must 123"), "text/plain")}
    )

    response = await session.scalars(select(Word))
    assert response.all() == [Word(name="must", count=2)]


async def test_add_document_result_sorted_by_idf(
    client: AsyncClient, session: AsyncSession
) -> None:
    await session.execute(
        insert(Word).values(
            [
                {"name": "must", "count": 2},
                {"name": "hello", "count": 1},
            ]
        )
    )
    await session.execute(
        insert(Document).values(
            [
                {"hash": "a2112ccca6196eaa982479150923a2d3"},
                {"hash": "7fefc5473f826628cf170b816dbd75da"},
            ]
        )
    )

    response = await client.post(
        url="/api/documents/",
        files={"file": ("asd.txt", BytesIO(b"Must Hello World"), "text/plain")},
    )
    assert response.status_code == 200
    assert response.json() == [
        {"idf": 0.48, "name": "world", "tf": 0.33},
        {"idf": 0.18, "name": "hello", "tf": 0.33},
        {"idf": 0.0, "name": "must", "tf": 0.33},
    ]


async def test_add_document_where_more_than_fifty_words(
    client: AsyncClient, session: AsyncSession
) -> None:
    content = (
        b"He tried not to look but he could resist. Three men had come in together. "
        b"He could make out much through the press of his regulars but they had an air "
        b"to them, the sort that said they were used to trouble. They did look like they "
        b"were local, either. Not city folk. Most likely they were sailors up from the "
        b"docks, although the Barrow of Beer was closer to the market side of the Maze and "
        b"not many sailors made it this far. The taverns and the Moongrass dens and the "
        b"brothels and the muggers and the press gangs saw to that. The three of them "
        b"settled into a corner near the door, crowding tightly onto wooden stools around "
        b"a tiny table. An unspoken accommodation was reached and the mood in the Barrow "
        b"sighed and relaxed back to its usual loudness. Three men who were used to "
        b"trouble, but they were looking for it here and that was all that mattered. "
        b"Kasmin finished what he was doing, wiping empty tankards and poured a couple "
        b"more. Most of the men in here passed as friends, people who been coming to the "
        b"Barrow for years. They were his family, his safe place. He took comfort from "
        b"that.Strangers made him uneasy. He had always kept a tavern. That done, he did "
        b"what was expected of him and wandered across the floor, easing himself between "
        b"the knots of drinkers until he reached the three strangers by the door."
    )

    response = await client.post(
        url="/api/documents/",
        files={"file": ("asd.txt", BytesIO(content), "text/plain")},
    )

    count_words = await session.scalar(select(func.count(Word.name)))
    assert response.status_code == 200
    assert count_words == 136
    assert len(response.json()) == 50
