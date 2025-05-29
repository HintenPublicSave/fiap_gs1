import pandas as pd
import streamlit as st
from sqlalchemy import BinaryExpression
from src.dashboard.generic.model_form_fields import ModelFormField

from src.database.tipos_base.model import Model
from src.plots.model_plot import ModelPlotter


class SimplePlotView:

    def __init__(self, model:type[Model]):
        self.model = model

    def view(self):
        """
        Função para exibir a página principal do aplicativo.
        :return:
        """
        st.title(f"Gráfico de {self.model.display_name_plural()}")



        filter_data = {}

        #todo melhorar os filtros no gráfico
        for plot_field in self.model.__generic_plot__.filters:

            form_field = ModelFormField(self.model, plot_field.field)

            new_value = form_field.render()

            filter_data[plot_field.field] = new_value

        col1, col2 = st.columns(2)

        simulacao = None
        real = None

        with col1:
            simulacao = st.button("Gerar Simulação")


        with col2:
            real = st.button("Gerar Gráfico")

        if simulacao or real:

            for plot_field in self.model.__generic_plot__.filters:
                form_field = ModelFormField(self.model, plot_field.field)
                value = filter_data.get(plot_field.field)
                if not form_field.is_valid(value, required=not plot_field.optional):
                    st.error(f"Erro ao validar o campo {plot_field.field}: {form_field.validate(value, required=not plot_field.optional)}")
                    return

        if simulacao:
            data = []

            for i in range(100):
                data.append(self.model.random(nullable=False))

            dataframe = pd.DataFrame(map(lambda x: x.to_dict(), data))

            model_plotter = ModelPlotter(self.model)

            grafico = model_plotter.get_plot(dataframe)

            st.pyplot(grafico)

        elif real:

            filters:list[BinaryExpression] = []

            for key, value in filter_data.items():
                if value is not None:
                    filters.append(
                        getattr(self.model, self.model.get_field(key).name) == value
                    )

            print(filters)


            model_plotter = ModelPlotter(self.model)
            dataframe = model_plotter.get_data_for_plot(filters=filters)
            grafico = model_plotter.get_plot(dataframe)
            st.pyplot(grafico)



    def get_page(self) -> st.Page:
        """
        Função para retornar a página de gráfico de umidade.
        :return: st.Page - A página para gerar o gráfico de umidade do aplicativo.
        """
        return st.Page(
            self.view,
            title=self.title,
            url_path=self.url_path
        )

