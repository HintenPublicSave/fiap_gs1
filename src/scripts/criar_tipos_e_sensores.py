import random
from datetime import datetime
from src.database.tipos_base.database import Database
from src.database.models.sensor import TipoSensorEnum, TipoSensor, Sensor
from src.database.models.sensor import LeituraSensor
from datetime import datetime

def criar_tipos_sensores_e_leituras():
    """
    Cria tipos de sensores, sensores e leituras iniciais no banco de dados.
    """

    sensores_padrao = [
    {
        "tipo": TipoSensorEnum.PROFUNDIDADE,
        "nome_tipo": "Sensor de Profundidade",
        "sensores": [
            {"nome": "Sensor Profundidade A", "descricao": "Sensor A para profundidade"},
            {"nome": "Sensor Profundidade B", "descricao": "Sensor B para profundidade"},
        ],
        "intervalo_valores": (10.0, 100.0),
        "qtd_leituras": 5
    },
    {
        "tipo": TipoSensorEnum.BUEIRO,
        "nome_tipo": "Sensor de Bueiro",
        "sensores": [
            {"nome": "Sensor Bueiro A", "descricao": "Sensor A para bueiro"},
            {"nome": "Sensor Bueiro B", "descricao": "Sensor B para bueiro"},
        ],
        "intervalo_valores": (0.0, 1.0), 
        "qtd_leituras": 5
    },
    {
        "tipo": TipoSensorEnum.LEITO,
        "nome_tipo": "Sensor de Leito",
        "sensores": [
            {"nome": "Sensor Leito A", "descricao": "Sensor A para leito de rio"},
            {"nome": "Sensor Leito B", "descricao": "Sensor B para leito de rio"},
        ],
        "intervalo_valores": (0.5, 10.0),
        "qtd_leituras": 5
    }
]


    with Database.get_session() as session:
        novos_tipos = []
        novos_sensores = []

        for entrada in sensores_padrao:
            tipo = session.query(TipoSensor).filter_by(nome=entrada["nome_tipo"]).first()

            if not tipo:
                tipo = TipoSensor(nome=entrada["nome_tipo"], tipo=entrada["tipo"])
                session.add(tipo)
                session.flush()
                novos_tipos.append(entrada["nome_tipo"])

            for sensor_data in entrada["sensores"]:
                sensor = session.query(Sensor).filter_by(nome=sensor_data["nome"]).first()
                if not sensor:
                    sensor = Sensor(
                        nome=sensor_data["nome"],
                        descricao=sensor_data["descricao"],
                        tipo_sensor_id=tipo.id,
                        data_instalacao=datetime.utcnow(),  # Define a data atual como instalação
                        latitude=round(random.uniform(-90.0, 90.0), 6),  # Latitude aleatória
                        longitude=round(random.uniform(-180.0, 180.0), 6)  # Longitude aleatória
                    )
                    session.add(sensor)
                    session.flush()
                    novos_sensores.append(sensor.nome)

                    # Criar leituras aleatórias para esse sensor
                    for _ in range(entrada["qtd_leituras"]):
                        valor = round(random.uniform(*entrada["intervalo_valores"]), 2)
                        leitura = LeituraSensor(
                                sensor_id=sensor.id,
                                valor=valor,
                                data_leitura=datetime.utcnow()
                            )
                        session.add(leitura)

        session.commit()

        if novos_tipos or novos_sensores:
            print(f"Tipos criados: {', '.join(novos_tipos)}")
            print(f"Sensores criados: {', '.join(novos_sensores)}")
        else:
            print("Nenhum novo tipo ou sensor foi criado (todos já existiam).")
