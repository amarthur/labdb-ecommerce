CREATE SCHEMA ecommerce;

CREATE TABLE usuario (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(15) NOT NULL,
    sobrenome VARCHAR(15) NOT NULL,
    email VARCHAR(50) NOT NULL,
    senha VARCHAR(50) NOT NULL
);

CREATE TABLE telefones_usuario (
    cpf VARCHAR(11),
    telefone VARCHAR(15),
    CONSTRAINT pk_cpf_tel PRIMARY KEY (cpf, telefone),
    CONSTRAINT fk_cpf FOREIGN KEY (cpf) REFERENCES usuario(cpf)
);

CREATE TABLE endereco_usuario (
    cpf VARCHAR(11),
    endereco VARCHAR(50),
    CONSTRAINT pk_cpf_end PRIMARY KEY (cpf, endereco),
    CONSTRAINT fk_cpf FOREIGN KEY (cpf) REFERENCES usuario(cpf)
);

CREATE TABLE usuario_assinante (
    tipo_beneficio TEXT
) INHERITS (usuario)
