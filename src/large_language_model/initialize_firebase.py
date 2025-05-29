import json
from firebase_admin import credentials, App
from firebase_admin import initialize_app


def initialize_firebase_app(credential_path: str) -> App:
    """
    Inicializa o aplicativo Firebase com as credenciais fornecidas.
    :param credential_path: caminho para o arquivo de credenciais JSON do Firebase.
    :return:
    """

    with open(credential_path) as source:
        info = json.load(source)

    firebase_credentials = credentials.Certificate(info)

    app = initialize_app(credential=firebase_credentials)

    return app

if __name__ == "__main__":

    firebase_app = initialize_firebase_app(r"/service_account.json")
    print(f"Firebase app initialized: {firebase_app.name}")