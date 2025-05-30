from typing import Iterator, Any

import streamlit as st
from google.genai import types
from google.genai.types import GenerateContentResponse

from src.dashboard.chat.generative_chat import get_or_init_chat, get_or_init_chat_client
from src.large_language_model.base_tools import BaseTool
from src.large_language_model.client import AvailableGenerativeModels


def get_conversa():

    chat_client = get_or_init_chat_client()

    col1, col2 = st.columns((10, 4))

    with col1:
        st.title("Assistente Virtual")

    with col2:
        options = [item for item in AvailableGenerativeModels]

        initial_index = options.index(chat_client.generative_model)

        selected_model = st.selectbox(
            index=initial_index,
            options=options,
            format_func=lambda x: str(AvailableGenerativeModels(x)),
            label="Modelo de linguagem",
            placeholder="Escolha uma opção",

        )

        st.button(f"Novo Chat{'*' if selected_model != chat_client.generative_model else ''}",
                  icon="➕",
                  on_click=lambda: get_or_init_chat(new_chat=True, generative_model=selected_model),
                  # type="primary",
                  )

    generative_chat = get_or_init_chat()

    messages = st.container(
        border=True,
    )

    messages.chat_message("ai").write("Olá! Como posso ajudar você hoje?")



    # Necessário fazer isso pq os chuncks de resposta do modelo ficam em Contents separados
    if generative_chat.get_history():

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

            role = "user"

            if any(map(lambda x: x.function_call, grupo[0].parts)):
                role = "assistant"

            elif any(map(lambda x: x.function_response, grupo[0].parts)):
                role = "assistant"

            elif grupo[0].role == "model":
                role = "ai"

            with messages.chat_message(role):

                placeholder = st.empty()

                resposta_text = ""

                for content in grupo:

                    for part in content.parts:

                        if part.file_data:
                            st.write(
                                f"Arquivo recebido: {part.file_data.name} ({part.file_data.mime_type})"
                            )
                        if part.function_call:
                            tool = chat_client.get_tool(part.function_call.name)

                            st.write(
                                tool.call_chat_display(),
                            )

                        if part.function_response:
                            tool = chat_client.get_tool(part.function_response.name)
                            st.write(
                                tool.call_result_display(part.function_response.response),
                            )

                        if part.text:
                            resposta_text += part.text
                            placeholder.write(resposta_text)

    prompt = st.chat_input(
        "Digite sua mensagem aqui...",
        accept_file=True,
        file_type=["jpg", "jpeg", "png"],
    )

    if prompt is not None and prompt.text.strip() != "":
        messages.chat_message("user").write(prompt.text)
        first = True
        tool_calls:list[tuple[BaseTool, list]] = [] #tool + args
        tool_result:list[tuple[BaseTool, Any]] = []
        tool_result_display:list[str] = []

        while first or len(tool_calls) > 0:

            if not first and tool_calls:

                for call in tool_calls:
                    tool, args = call
                    result = tool.execute(*args)
                    tool_result.append((tool, result))
                    tool_result_display.append(tool.call_result_display(result))

            message_stream:Iterator[GenerateContentResponse]

            if first:
                message_stream = generative_chat.send_message_stream(
                    prompt.text.strip(),
                )
            else:
                message_stream = generative_chat.send_message_stream(
                    list(map(lambda x: x[0].get_result_as_part(x[1]), tool_result)),
                )

                with messages.chat_message("assistant"):
                    for display in tool_result_display:
                        st.write(display)

                tool_calls = []
                tool_result = []
                tool_result_display = []

            first = False

            with messages.chat_message("ai"):
                with st.spinner("Pensando..."):
                    placeholder = st.empty()
                    resposta = ""
                    for chunk in message_stream:

                        if chunk.function_calls:
                            for call in chunk.function_calls:

                                tool = chat_client.get_tool(call.name)

                                st.write(
                                    tool.call_chat_display(),
                                )

                                tool_calls.append((tool, call.args))

                        if chunk.executable_code:
                            for code in chunk.executable_code:
                                    st.write(
                                        f"Código executado chamada: {code.name}"
                                    )

                        if chunk.code_execution_result:
                            for result in chunk.code_execution_result:
                                st.write(
                                    f"Resultado da execução do código: {result.response}"
                                )

                        if chunk.text:
                            resposta += chunk.text
                            placeholder.write(resposta)

