import streamlit as st
from google.genai import types
from src.dashboard.chat.generative_chat import get_or_init_chat


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

    messages.chat_message("assistant").write("Olá! Como posso ajudar você hoje?")



    # Necessário fazer isso pq os chuncks de resposta do modelo ficam em Contents separados
    if len(generative_chat.get_history()) > 0:

        agrupados:list[list[types.Content]] = []

        last_content = None
        current_agrupamento = []

        for content in generative_chat.get_history():
            if last_content is None or content.role != last_content.role:
                if current_agrupamento:
                    agrupados.append(current_agrupamento)

                current_agrupamento = [content]
            else:
                current_agrupamento.append(content)
            last_content = content

        if current_agrupamento:
            agrupados.append(current_agrupamento)


        for grupo in agrupados:

            role = "user" if grupo[0].role == "user" else "assistant"
            with messages.chat_message(role):

                placeholder = st.empty()

                resposta_text = ""

                for content in grupo:
                    for part in content.parts:

                        if part.text:
                            resposta_text += part.text
                            placeholder.write(resposta_text)

                        if part.file_data:
                            st.write(
                                f"Arquivo recebido: {part.file_data.name} ({part.file_data.mime_type})"
                            )
                        if part.function_call:
                            st.write(
                                f"Função chamada: {part.function_call.name} com argumentos {part.function_call.arguments}"
                            )
                        if part.function_response:
                            st.write(
                                f"Resposta da função: {part.function_response.text}"
                            )

    prompt = st.chat_input(
        "Digite sua mensagem aqui...",
        accept_file=True,
        file_type=["jpg", "jpeg", "png"],
    )

    if prompt is not None and prompt.text.strip() != "":
        messages.chat_message("user").write(prompt.text)

        with messages.chat_message("assistant"):
            with st.spinner("Pensando..."):
                placeholder = st.empty()
                resposta = ""
                for chunk in generative_chat.send_message_stream(prompt.text.strip()):
                    if chunk.text:
                        resposta += chunk.text
                        placeholder.write(resposta)
