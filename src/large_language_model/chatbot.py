#from google.cloud.aiplatform_v1 import GenerationConfig, SafetySetting, Content, Part
# from google.genai.types import Content
from vertexai.generative_models import GenerativeModel, ToolConfig
from vertexai.preview.generative_models import ChatSession

from src.large_language_model.initialize_llm import InitializeAiPlatform


def get_chatbot() -> ChatSession:


    generative_model = GenerativeModel(
        model_name="gemini-2.0-flash-lite",
        # generation_config=GenerationConfig(),
        # safety_settings=[SafetySetting()],
        # tools=[],
        # tool_config=ToolConfig(),
        system_instruction=["Você é um pirata que sempre responde com uma frase de pirata. Gosta de falar Yarr, gosta de aventuras e tesouros."]
    )

    return generative_model.start_chat()


if __name__ == "__main__":
    InitializeAiPlatform.initialize_from_service_account(
        r"/service_account.json")

    chat = get_chatbot()

    response = chat.send_message("Olá, como você está?")

    print(response.text)

    response = chat.send_message("Qual é o seu tesouro favorito?")

    print(response.text)

    response = chat.send_message("Yarr, o que você acha de aventuras no mar?")

    print(response.text)


    print(chat.history)