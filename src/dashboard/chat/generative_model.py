import streamlit as st
from vertexai.preview.generative_models import ChatSession
from src.large_language_model.chatbot import get_chatbot
from src.large_language_model.initialize_llm import InitializeAiPlatform


def get_or_init_chat(new_chat: bool = False) -> ChatSession:
    """
    Função para obter ou inicializar o chat.
    :return: GenerativeModel - A instância do modelo de linguagem generativa.
    """
    if "generative_model" not in st.session_state:
        print("Initializing generative model...")
        InitializeAiPlatform.initialize_from_service_account(r"service_account.json")
        st.session_state.generative_model = get_chatbot()

    elif new_chat:
        st.session_state.generative_model = get_chatbot()

    return st.session_state.generative_model