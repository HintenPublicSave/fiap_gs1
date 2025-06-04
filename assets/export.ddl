
CREATE TABLE "ARQUIVO" (
	id INTEGER NOT NULL, 
	nome VARCHAR(255) NOT NULL, 
	tipo VARCHAR(15) NOT NULL, 
	ultima_atualizacao DATETIME, 
	bytes_arquivo BLOB NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "TIPO_SENSOR" (
	id INTEGER NOT NULL, 
	nome VARCHAR(255) NOT NULL, 
	tipo VARCHAR(15) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "POST_REDE_SOCIAL" (
	id INTEGER NOT NULL, 
	conteudo TEXT NOT NULL, 
	ultima_atualizacao DATETIME, 
	anexo_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(anexo_id) REFERENCES "ARQUIVO" (id)
)

;


CREATE TABLE "SENSOR" (
	id INTEGER NOT NULL, 
	tipo_sensor_id INTEGER NOT NULL, 
	nome VARCHAR(255) NOT NULL, 
	descricao VARCHAR(255), 
	data_instalacao DATETIME, 
	latitude FLOAT, 
	longitude FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(tipo_sensor_id) REFERENCES "TIPO_SENSOR" (id), 
	UNIQUE (nome)
)

;


CREATE TABLE "LEITURA_SENSOR" (
	id INTEGER NOT NULL, 
	sensor_id INTEGER NOT NULL, 
	data_leitura DATETIME NOT NULL, 
	valor FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sensor_id) REFERENCES "SENSOR" (id)
)

;

