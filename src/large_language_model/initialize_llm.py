from vertexai.generative_models import GenerativeModel
from google.cloud import aiplatform
from firebase_admin import App
from google.oauth2 import service_account


class InitializeAiPlatform:

    @classmethod
    def initialize_from_firebase(cls, firebase_app:App) -> None:
        """
        Inicializa a plataforma Vertex AI com as configurações necessárias.
        :param firebase_app: Instância do aplicativo Firebase já inicializada.
        """

        google_credentials = firebase_app.credential.get_credential()

        aiplatform.init(
            project=firebase_app.project_id,
            location=firebase_app.options.get('location', 'us-central1'),
            credentials=google_credentials
        )

    @classmethod
    def initialize_from_service_account(cls, service_account_path: str) -> None:
        """
        Inicializa a plataforma Vertex AI usando um arquivo de conta de serviço.
        :param service_account_path: Caminho para o arquivo JSON da conta de serviço.
        """

        credentials = service_account.Credentials.from_service_account_file(service_account_path)

        aiplatform.init(
            project=credentials.project_id,
            location='us-central1',
            credentials=credentials
        )


def get_generative_model(model_name: str = 'gemini-2.0-flash-lite') -> GenerativeModel:
    """

    Inicializa o modelo de linguagem generativa com o nome especificado.

    :param model_name: Nome do modelo de linguagem a ser inicializado. Padrão é 'gemini-2.0-flash-lite'.
    :return: Instância do modelo de linguagem generativa.

    """
    return GenerativeModel(model_name=model_name)

if __name__ == "__main__":
    InitializeAiPlatform.initialize_from_service_account(r"C:\Users\Lucas\PycharmProjects\fiap_gs1\fiap-gs1-343ac4a75e97.json")

    modelo_generativo = get_generative_model()

    chat = modelo_generativo.start_chat()

    response = chat.send_message("Olá, como você está?")

    print(response.text)
