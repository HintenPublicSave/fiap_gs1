from sqlalchemy import Sequence, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.tipos_base.model import Model
from datetime import datetime
from src.database.models.files_database import Arquivo
from src.database.tipos_base.model_mixins.display import SimpleTableFilter


class PostRedeSocial(Model):
    """
    Modelo para representar um post em uma rede social.
    """

    __tablename__ = 'POST_REDE_SOCIAL'
    __menu_group__ = "Posts"
    __menu_order__ = 1
    __database_import_order__ = 10

    __table_view_filters__ = [
        SimpleTableFilter(
            field='ultima_atualizacao',
            operator='>=',
            label="Data Inicial"
        ),
        SimpleTableFilter(
            field='ultima_atualizacao',
            operator='<=',
            label="Data Final"
        )
    ]

    @classmethod
    def display_name(cls) -> str:
        return "Post Rede Social"

    @classmethod
    def display_name_plural(cls) -> str:
        return "Posts Rede Social"

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_SEQ_ID"),
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    conteudo: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=False,
        info={
            'label': 'Conteúdo',
        },
        comment="Conteúdo do post na rede social"
    )

    ultima_atualizacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        unique=False,
        info={
            'label': 'Ultima atualização'
        },
        default= datetime.now,
    )

    anexo_id: Mapped[int] = mapped_column(
        ForeignKey('ARQUIVO.id'),
        nullable=True,
        info={
            'label': 'anexo',
        },
        comment="Anexo do post, se houver"
    )

    anexo = relationship(
        Arquivo,
        back_populates='posts',
    )



    def __str__(self):
        return f"{self.id} - {self.ultima_atualizacao}"