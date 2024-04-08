from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(DeclarativeBase, MappedAsDataclass): ...


class Document(Base):
    __tablename__ = "documents"
    hash: Mapped[str] = mapped_column(primary_key=True)


class Word(Base):
    __tablename__ = "words"
    name: Mapped[str] = mapped_column(primary_key=True)
    count: Mapped[int] = mapped_column(default=1)
