from datetime import datetime
from src.database.tipos_base.database import Database
from src.database.models.sensor import TipoSensor, TipoSensorEnum, Sensor, LeituraSensor


def criar_tipo_sensor(nome: str, tipo_enum: TipoSensorEnum) -> TipoSensor:
    """Cria um novo tipo de sensor."""
    with Database.get_session() as session:
        tipo_sensor = TipoSensor(nome=nome, tipo=tipo_enum)
        session.add(tipo_sensor)
        session.commit()
        return tipo_sensor


def criar_sensor(nome: str, descricao: str, tipo_sensor_id: int,
                 latitude: float = None, longitude: float = None,
                 data_instalacao: datetime = None) -> Sensor:
    """Cria um novo sensor com dados básicos e localização."""
    with Database.get_session() as session:
        sensor = Sensor(
            nome=nome,
            descricao=descricao,
            tipo_sensor_id=tipo_sensor_id,
            latitude=latitude,
            longitude=longitude,
            data_instalacao=data_instalacao or datetime.now()
        )
        session.add(sensor)
        session.commit()
        return sensor


def salvar_leitura(sensor_id: int, valor: float, data_leitura: datetime = None) -> LeituraSensor:
    """Salva uma leitura de sensor."""
    with Database.get_session() as session:
        leitura = LeituraSensor(
            sensor_id=sensor_id,
            valor=valor,
            data_leitura=data_leitura or datetime.now()
        )
        session.add(leitura)
        session.commit()
        return leitura
