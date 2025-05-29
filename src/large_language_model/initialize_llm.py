from google import genai
from google.genai import types, chats

#https://github.com/googleapis/python-genai
class GenerativeModelClient:

    def __init__(self, api_key='AIzaSyBBaXU3EV4tetwquRtuPmxH0oeVd6iGIqY'):

        self.client = genai.Client(api_key=api_key)

    def get_chat(self, model_name: str = 'gemini-2.0-flash-lite') -> chats.Chat:
        """

        Inicializa o modelo de linguagem generativa com o nome especificado.

        :param model_name: Nome do modelo de linguagem a ser inicializado. Padrão é 'gemini-2.0-flash-lite'.
        :return: Instância do modelo de linguagem generativa.

        """

        return self.client.chats.create(
            model=model_name,
            config=types.GenerateContentConfig(
                system_instruction="Você é um pirata que sempre responde com uma frase de pirata. Gosta de falar Yarr, gosta de aventuras e tesouros."
            )
        )


if __name__ == "__main__":
    instance = GenerativeModelClient('AIzaSyBBaXU3EV4tetwquRtuPmxH0oeVd6iGIqY')

    chat = instance.get_chat()

    response = chat.send_message("Olá, como você está?")

    print(response.text)
