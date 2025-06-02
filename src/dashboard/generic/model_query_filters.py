from sqlalchemy import BinaryExpression

from src.dashboard.generic.model_form_fields import ModelFormField
from src.database.tipos_base.model import Model
import streamlit as st
import json
import base64
from typing import Any

from src.database.tipos_base.model_mixins.display import SimpleTableFilter


class ModelQueryFilters:
    """
    Classe para gerenciar filtros de consulta em um modelo.
    """

    def __init__(self, model:type[Model],
                 filters: list[SimpleTableFilter] = None,
                 show_validation: bool = False,
                 show_botao_filtrar: bool = True
                 ):
        """
        :param model: O modelo para o qual os filtros serão aplicados.
        :param filters: Lista de filtros a serem aplicados ao modelo.
        :param show_validation: Se True, exibe validações nos campos de filtro.
        :param show_botao_filtrar: Se True, exibe o botão de filtrar.
        """
        self.model = model

        filters_base_64_string = st.query_params.get('filters', None)

        filters_parsed:list[SimpleTableFilter] = []

        if filters_base_64_string is not None:
            filters_base_64 = base64.b64decode(filters_base_64_string).decode('utf-8')
            filters_json = json.loads(filters_base_64)

            for f in filters_json:
                filters_parsed.append(SimpleTableFilter.from_json(f))

        self.filters_parsed = filters_parsed
        self._render_filters = filters if filters is not None else self.model.__table_view_filters__
        self.show_validation = show_validation
        self.show_botao_filtrar = show_botao_filtrar

    def get_filters(self) -> list[SimpleTableFilter]:
        """
        Retorna os filtros aplicados ao modelo.
        :return: Lista de filtros aplicados.
        """
        return self.filters_parsed

    def get_sqlalchemy_filters(self) -> list[BinaryExpression]:
        """
        Retorna os filtros aplicados ao modelo como expressões SQLAlchemy.
        :return: Lista de expressões SQLAlchemy.
        """
        return [filtro.get_sqlalchemy_filter(self.model) for filtro in self.filters_parsed if filtro.value is not None or filtro.optional == False]

    def get_filter_values(self) -> dict[str, Any]:
        """
        Retorna os valores dos filtros aplicados ao modelo.
        :return: Dicionário com os valores dos filtros.
        """
        return {filtro.field: filtro.value for filtro in self.filters_parsed if filtro.value is not None or filtro.optional == False}

    def get_filter_values_by_name(self) -> dict[str, Any]:
        """
        Retorna os valores dos filtros aplicados ao modelo, incluindo os overrides de campo.
        :return: Dicionário com os valores dos filtros e seus overrides.
        """
        return {filtro.name or filtro.field: filtro.value for filtro in self.filters_parsed if filtro.value is not None or filtro.optional == False}

    _filtros_updated: list[SimpleTableFilter] = []

    def render(self):
        """
        Renderiza os filtros de consulta para o modelo.
        :return: None
        """

        self._filtros_updated = []

        colf1, colf2 = st.columns([1, 1])
        with colf1:
            st.write("Filtros")
        with colf2:
            if st.button("🗑️", help="Limpar filtros", key="clear_filters"):
                st.query_params.pop('filters', None)
                st.rerun()


        for _filtro in self._render_filters:
            filtro = next((f for f in self.filters_parsed if f.field == _filtro.field and f.operator == _filtro.operator),
                          _filtro)

            new_value = self._render_form_field(filtro)

            filtro_update = filtro.copy_with(value=new_value)

            self._filtros_updated.append(filtro_update)

        if self.show_botao_filtrar and st.button("Filtrar"):
            self.apply_filters()
            st.rerun()

    def apply_filters(self):

        novos_filtros_parsed = json.dumps(list(map(lambda x: x.to_json(), self._filtros_updated)))
        st.query_params['filters'] = base64.b64encode(str(novos_filtros_parsed).encode('utf-8')).decode('utf-8')

    def _render_form_field(self, filtro:SimpleTableFilter) -> Any:
        form_field = ModelFormField(
            model=self.model,
            field_name=filtro.field,
            label=filtro.label,
        )

        return form_field.render(initial_value=filtro.value, show_validation=self.show_validation)

    def filters_valid(self) -> bool:
        """
        Verifica se os filtros aplicados são válidos.
        :return: True se os filtros forem válidos, False caso contrário.
        """
        for filtro in self.filters_parsed:
            form_field = ModelFormField(
                model=self.model,
                field_name=filtro.field,
                label=filtro.label,
                nullable=filtro.optional
            )
            if not form_field.is_valid(filtro.value, required=not filtro.optional):
                return False
        return True