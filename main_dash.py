from src.dashboard.main import main as dashboard_main
from dotenv import load_dotenv
from src.scripts.criar_tipos_e_sensores import criar_tipos_sensores_e_leituras


import os

def main():
    """
    Função principal do aplicativo Streamlit.
    para rodar o aplicativo, execute o seguinte comando:
    streamlit run main_dash.py
    """
    load_dotenv()

    dashboard_main()

if __name__ == "__main__":
    main()
    # criar_tipos_sensores_e_leituras()
