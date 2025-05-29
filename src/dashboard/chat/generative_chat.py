import streamlit as st
from src.large_language_model.initialize_llm import GenerativeModelClient
from google.genai import types, chats
import logging


def get_or_init_chat(new_chat: bool = False) -> chats.Chat:
    """
    Função para obter ou inicializar o chat.
    :return: GenerativeModel - A instância do modelo de linguagem generativa.
    """
    if "generative_model_client" not in st.session_state:
        logging.debug("Initializing generative model...")
        st.session_state.generative_model_client = GenerativeModelClient()

    if "generative_chat" not in st.session_state or new_chat:
        logging.info("Creating new chat...")
        st.session_state.generative_chat = st.session_state.generative_model_client.get_chat()

    return st.session_state.generative_chat