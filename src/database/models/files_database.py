from enum import StrEnum
from typing import List
from sqlalchemy import Sequence, String, Text, ForeignKey, Float, DateTime, Enum, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.tipos_base.model import Model
from datetime import datetime


class TipoArquivoEnum(StrEnum):
    jpeg = "image/jpeg"
    png = "image/png"

    def __str__(self):

        if self.value == "image/jpeg":
            return "image/jpeg"

        if self.value == "image/png":
            return "image/png"

        return super().name


class Arquivo(Model):
    """Tabela para armazenar arquivos na database.
     Posteriormente os arquivos serão armazenados numa CDN ou em um bucket de armazenamento."""

    __tablename__ = 'ARQUIVO'
    __menu_group__ = "Arquivos"
    __menu_order__ = 1
    __database_import_order__ = 1
    __table_view_fields__ = [
        'id',
        'nome',
        'tipo',
        'ultima_atualizacao'
    ]

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_SEQ_ID"),
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        info={
            'label': 'Nome'
        },
        comment="Ex.: foto.jpeg"
    )

    tipo: Mapped[TipoArquivoEnum] = mapped_column(
        Enum(TipoArquivoEnum, length=15),
        nullable=False,
        unique=False,
        info={
            'label': 'Tipo'
        },
        comment="Mime type do arquivo, ex.: image/jpeg"
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

    bytes_arquivo: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
        info={
            'label': 'Bytes do Arquivo',
            'extensions': ['jpg', 'jpeg', 'png'],
        },
    )

    posts = relationship(
        'PostRedeSocial',
        back_populates='anexo',
        cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"{self.id} - {self.nome}"