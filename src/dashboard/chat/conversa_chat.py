import streamlit as st

from src.dashboard.chat.generative_model import get_or_init_chat


def get_conversa():

    col1, col2 = st.columns((10, 3))

    with col1:
        st.title("Conversa com o Modelo de Linguagem")

    with col2:
        st.button("Novo Chat",
                  icon="➕",
                  on_click=lambda: get_or_init_chat(new_chat=True),
                  # type="primary",
                  )

    generative_chat = get_or_init_chat()

    messages = st.container(
        border=True,
    )

    reset_initial = False

    if generative_chat.history is not None and len(generative_chat.history) > 0:

        for part in generative_chat.history:
            if part.role == "user":
                messages.chat_message("user").write(part.text)
            else:
                messages.chat_message("assistant").write(part.text)
    else:
        reset_initial = True
        messages.chat_message("assistant").write("Olá! Como posso ajudar você hoje?")


    prompt = st.chat_input(
        "Say something and/or attach an image",
        accept_file=True,
        file_type=["jpg", "jpeg", "png"],
    )

    if prompt is not None and prompt.text.strip() != "":
        messages.chat_message("user").write(prompt.text)

        with messages.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = generative_chat.send_message(prompt.text.strip())
                st.write(response.text)

        if reset_initial:
            st.rerun()