-- Criação do banco de dados

CREATE DATABASE ecommerce-relacional

-- Criação das tabelas

-- Entidade Empresa
CREATE TABLE Empresa (
  CNPJ CHAR(14) PRIMARY KEY,
  Localizacao VARCHAR(100),
  Contato VARCHAR(100)[] NOT NULL,
  Informacao TEXT,
  Nome VARCHAR(100),
  Ranking INTEGER
);

-- Especialização Transportadora
CREATE TABLE Transportadora (
  CNPJ CHAR(14) PRIMARY KEY REFERENCES Empresa(CNPJ)
);

-- Especialização Vendedor
CREATE TABLE Vendedor (
  CNPJ CHAR(14) PRIMARY KEY REFERENCES Empresa(CNPJ),
  QuantidadeVendas INTEGER
);

-- Entidade Produto
CREATE TABLE Produto (
  ID SERIAL PRIMARY KEY,
  Nome VARCHAR(100),
  Imagem TEXT[],
  InformacaoTecnica TEXT,
  Descricao TEXT,
  Fabricante VARCHAR(100),
  Marca VARCHAR(100)
);

-- Entidade Pedido
CREATE TABLE Pedido (
  ID SERIAL PRIMARY KEY,
  Status VARCHAR(100),
  Observacoes TEXT
);

-- Entidade Método Pagamento
CREATE TABLE MetodoPagamento (
  ID SERIAL PRIMARY KEY,
  Informacoes VARCHAR(100)[]
);

-- Entidade Usuário
CREATE TABLE Usuario (
  CPF CHAR(11) PRIMARY KEY,
  Endereco VARCHAR(100)[],
  Telefone VARCHAR(20)[],
  Nome VARCHAR(100),
  Senha VARCHAR(100),
  Email VARCHAR(100)
);

-- Especialização Usuário Assinante
CREATE TABLE UsuarioAssinante (
  CPF CHAR(11) PRIMARY KEY REFERENCES Usuario(CPF)
);

-- Especialização Usuário Comum
CREATE TABLE UsuarioComum (
  CPF CHAR(11) PRIMARY KEY REFERENCES Usuario(CPF)
);

-- Relacionamento Vende
CREATE TABLE Vende (
  VendedorCNPJ CHAR(14) REFERENCES Vendedor(CNPJ),
  ProdutoID INTEGER REFERENCES Produto(ID),
  Preco NUMERIC,
  Estoque INTEGER,
  Garantia VARCHAR(100),
  PRIMARY KEY (VendedorCNPJ, ProdutoID)
);

-- Relacionamento Faz promoção
CREATE TABLE FazPromocao (
  VendedorCNPJ CHAR(14) REFERENCES Vendedor(CNPJ),
  ProdutoID INTEGER REFERENCES Produto(ID),
  DataInicio DATE,
  DataFim DATE,
  Tipo VARCHAR(100),
  PRIMARY KEY (VendedorCNPJ, ProdutoID)
);

-- Relacionamento Busca
CREATE TABLE Busca (
  ProdutoID INTEGER REFERENCES Produto(ID),
  UsuarioCPF CHAR(11) REFERENCES Usuario(CPF),
  DataHora TIMESTAMP,
  PRIMARY KEY (ProdutoID, UsuarioCPF)
);

-- Relacionamento Deseja
CREATE TABLE Deseja (
  ProdutoID INTEGER REFERENCES Produto(ID),
  UsuarioCPF CHAR(11) REFERENCES Usuario(CPF),
  Quantidade INTEGER,
  PRIMARY KEY (ProdutoID, UsuarioCPF)
);

-- Relacionamento Paga
CREATE TABLE Paga (
  PedidoID INTEGER REFERENCES Pedido(ID),
  MetodoPagamentoID INTEGER REFERENCES MetodoPagamento(ID),
  Parcelamento VARCHAR(100),
  PRIMARY KEY (PedidoID, MetodoPagamentoID)
);

-- Relacionamento Possui
CREATE TABLE Possui (
  UsuarioCPF CHAR(11) REFERENCES Usuario(CPF),
  MetodoPagamentoID INTEGER REFERENCES MetodoPagamento(ID),
  PRIMARY KEY (UsuarioCPF, MetodoPagamentoID)
);

-- Relacionamento Faz
CREATE TABLE Faz (
  UsuarioCPF CHAR(11) REFERENCES Usuario(CPF),
  PedidoID INTEGER REFERENCES Pedido(ID),
  Data DATE,
  PRIMARY KEY (UsuarioCPF, PedidoID)
);

-- Relacionamento Tem Benefício
CREATE TABLE TemBeneficio (
  UsuarioAssinanteCPF CHAR(11) REFERENCES UsuarioAssinante(CPF),
  PedidoID INTEGER REFERENCES Pedido(ID),
  Tipo VARCHAR(100),
  PRIMARY KEY (UsuarioAssinanteCPF, PedidoID)
);

-- Relacionamento Contém
CREATE TABLE Contem (
  TransportadoraCNPJ CHAR(14) REFERENCES Transportadora(CNPJ),
  ItemID SERIAL,
  PedidoID INTEGER REFERENCES Pedido(ID),
  Quantidade INTEGER,
  Rastreio VARCHAR(100),
  DataEntrega DATE,
  Frete NUMERIC,
  PRIMARY KEY (TransportadoraCNPJ, ItemID, PedidoID)
);

-- Criação das restrições

-- Restrição NOT NULL
ALTER TABLE Empresa ALTER COLUMN Contato SET NOT NULL;
ALTER TABLE Usuario ALTER COLUMN Endereco SET NOT NULL;
ALTER TABLE Usuario ALTER COLUMN Telefone SET NOT NULL;

-- Restrição UNIQUE
ALTER TABLE Empresa ADD CONSTRAINT UniqueEmpresaNome UNIQUE (Nome);
ALTER TABLE Usuario ADD CONSTRAINT UniqueUsuarioEmail UNIQUE (Email);

-- Restrição CHECK
ALTER TABLE Pedido ADD CONSTRAINT CheckStatus CHECK (Status IN ('Aguardando', 'Em andamento', 'Concluído'));
ALTER TABLE FazPromocao ADD CONSTRAINT CheckTipo CHECK (Tipo IN ('Desconto', 'Brinde'));
ALTER TABLE Vende ADD CONSTRAINT CheckEstoque CHECK (Estoque >= 0);
ALTER TABLE Paga ADD CONSTRAINT CheckParcelamento CHECK (Parcelamento IN ('À vista', 'Parcelado'));
ALTER TABLE Contem ADD CONSTRAINT CheckQuantidade CHECK (Quantidade >= 0);
ALTER TABLE Contem ADD CONSTRAINT CheckFrete CHECK (Frete >= 0);

-- Restrição ON DELETE CASCADE
ALTER TABLE Vendedor DROP CONSTRAINT VendedorCNPJ;
ALTER TABLE Vendedor ADD CONSTRAINT VendedorCNPJ FOREIGN KEY (CNPJ) REFERENCES Empresa(CNPJ) ON DELETE CASCADE;

-- Restrição ON UPDATE CASCADE
ALTER TABLE Empresa DROP CONSTRAINT UniqueEmpresaNome;
ALTER TABLE Empresa ADD CONSTRAINT UniqueEmpresaNome UNIQUE (Nome) ON UPDATE CASCADE;

-- Restrição ON DELETE SET NULL
ALTER TABLE Pedido DROP CONSTRAINT FazPedidoID;
ALTER TABLE Pedido ADD CONSTRAINT FazPedidoID FOREIGN KEY (ID) REFERENCES Faz(PedidoID) ON DELETE SET NULL;
