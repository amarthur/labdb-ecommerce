-- Inserção de dados de teste na tabela Empresa
INSERT INTO Empresa (CNPJ, Localizacao, Contato, Informacao, Nome, Ranking)
VALUES
  ('11111111111111', 'São Paulo, SP', '{"comercial@example.com", "suporte@example.com"}', 'Informações da empresa A', 'Empresa A', 4),
  ('22222222222222', 'Rio de Janeiro, RJ', '{"vendas@example.com", "atendimento@example.com"}', 'Informações da empresa B', 'Empresa B', 3),
  ('33333333333333', 'Belo Horizonte, MG', '{"contato@example.com"}', 'Informações da empresa C', 'Empresa C', 5),
  ('44444444444444', 'Porto Alegre, RS', '{"sac@example.com"}', 'Informações da empresa D', 'Empresa D', 2),
  ('55555555555555', 'Curitiba, PR', '{"suporte@example.com"}', 'Informações da empresa E', 'Empresa E', 4),
  ('66666666666666', 'Salvador, BA', '{"vendas@example.com"}', 'Informações da empresa F', 'Empresa F', 3),
  ('77777777777777', 'Recife, PE', '{"atendimento@example.com"}', 'Informações da empresa G', 'Empresa G', 5),
  ('88888888888888', 'Fortaleza, CE', '{"contato@example.com"}', 'Informações da empresa H', 'Empresa H', 2),
  ('99999999999999', 'Manaus, AM', '{"sac@example.com"}', 'Informações da empresa I', 'Empresa I', 4),
  ('00000000000000', 'Porto Velho, RO', '{"suporte@example.com"}', 'Informações da empresa J', 'Empresa J', 3);

-- Inserção de dados de teste na tabela Transportadora
INSERT INTO Transportadora (CNPJ)
VALUES
  ('11111111111111'),
  ('33333333333333'),
  ('55555555555555'),
  ('77777777777777'),
  ('99999999999999');

-- Inserção de dados de teste na tabela Vendedor
INSERT INTO Vendedor (CNPJ, QuantidadeVendas)
VALUES
  ('22222222222222', 50),
  ('44444444444444', 20),
  ('66666666666666', 35),
  ('88888888888888', 10),
  ('00000000000000', 15);

-- Inserção de dados de teste na tabela Produto
INSERT INTO Produto (Nome, Imagem, InformacaoTecnica, Descricao, Fabricante, Marca)
VALUES
  ('Produto A', '{"imagem1.jpg", "imagem2.jpg"}', 'Informações técnicas do Produto A', 'Descrição do Produto A', 'Fabricante A', 'Marca A'),
  ('Produto B', '{"imagem3.jpg", "imagem4.jpg"}', 'Informações técnicas do Produto B', 'Descrição do Produto B', 'Fabricante B', 'Marca B'),
  ('Produto C', '{"imagem5.jpg", "imagem6.jpg"}', 'Informações técnicas do Produto C', 'Descrição do Produto C', 'Fabricante C', 'Marca C'),
  ('Produto D', '{"imagem7.jpg", "imagem8.jpg"}', 'Informações técnicas do Produto D', 'Descrição do Produto D', 'Fabricante D', 'Marca D'),
  ('Produto E', '{"imagem9.jpg", "imagem10.jpg"}', 'Informações técnicas do Produto E', 'Descrição do Produto E', 'Fabricante E', 'Marca E'),
  ('Produto F', '{"imagem11.jpg", "imagem12.jpg"}', 'Informações técnicas do Produto F', 'Descrição do Produto F', 'Fabricante F', 'Marca F'),
  ('Produto G', '{"imagem13.jpg", "imagem14.jpg"}', 'Informações técnicas do Produto G', 'Descrição do Produto G', 'Fabricante G', 'Marca G'),
  ('Produto H', '{"imagem15.jpg", "imagem16.jpg"}', 'Informações técnicas do Produto H', 'Descrição do Produto H', 'Fabricante H', 'Marca H'),
  ('Produto I', '{"imagem17.jpg", "imagem18.jpg"}', 'Informações técnicas do Produto I', 'Descrição do Produto I', 'Fabricante I', 'Marca I'),
  ('Produto J', '{"imagem19.jpg", "imagem20.jpg"}', 'Informações técnicas do Produto J', 'Descrição do Produto J', 'Fabricante J', 'Marca J');

-- Inserção de dados de teste na tabela Pedido
INSERT INTO Pedido (Status, Observacoes)
VALUES
  ('Aguardando', 'Observações do pedido 1'),
  ('Em andamento', 'Observações do pedido 2'),
  ('Concluído', 'Observações do pedido 3'),
  ('Aguardando', 'Observações do pedido 4'),
  ('Em andamento', 'Observações do pedido 5'),
  ('Concluído', 'Observações do pedido 6'),
  ('Aguardando', 'Observações do pedido 7'),
  ('Em andamento', 'Observações do pedido 8'),
  ('Concluído', 'Observações do pedido 9'),
  ('Aguardando', 'Observações do pedido 10');

-- Inserção de dados de teste na tabela Método Pagamento
INSERT INTO MetodoPagamento (Informacoes)
VALUES
  ('Informações do método de pagamento 1'),
  ('Informações do método de pagamento 2'),
  ('Informações do método de pagamento 3'),
  ('Informações do método de pagamento 4'),
  ('Informações do método de pagamento 5'),
  ('Informações do método de pagamento 6'),
  ('Informações do método de pagamento 7'),
  ('Informações do método de pagamento 8'),
  ('Informações do método de pagamento 9'),
  ('Informações do método de pagamento 10');

-- Inserção de dados de teste na tabela Usuario
INSERT INTO Usuario (CPF, Endereco, Telefone, Nome, Senha, Email)
VALUES
  ('11111111111', '{"Endereco 1", "Endereco 2"}', '{"Telefone 1", "Telefone 2"}', 'Usuário A', 'senhaA', 'usuarioA@example.com'),
  ('22222222222', '{"Endereco 3"}', '{"Telefone 3"}', 'Usuário B', 'senhaB', 'usuarioB@example.com'),
  ('33333333333', '{"Endereco 4"}', '{"Telefone 4"}', 'Usuário C', 'senhaC', 'usuarioC@example.com'),
  ('44444444444', '{"Endereco 5"}', '{"Telefone 5"}', 'Usuário D', 'senhaD', 'usuarioD@example.com'),
  ('55555555555', '{"Endereco 6"}', '{"Telefone 6"}', 'Usuário E', 'senhaE', 'usuarioE@example.com'),
  ('66666666666', '{"Endereco 7"}', '{"Telefone 7"}', 'Usuário F', 'senhaF', 'usuarioF@example.com'),
  ('77777777777', '{"Endereco 8"}', '{"Telefone 8"}', 'Usuário G', 'senhaG', 'usuarioG@example.com'),
  ('88888888888', '{"Endereco 9"}', '{"Telefone 9"}', 'Usuário H', 'senhaH', 'usuarioH@example.com'),
  ('99999999999', '{"Endereco 10"}', '{"Telefone 10"}', 'Usuário I', 'senhaI', 'usuarioI@example.com'),
  ('00000000000', '{"Endereco 11"}', '{"Telefone 11"}', 'Usuário J', 'senhaJ', 'usuarioJ@example.com');

-- Inserção de dados de teste na tabela Usuário Assinante
INSERT INTO UsuarioAssinante (CPF)
VALUES
  ('11111111111'),
  ('33333333333'),
  ('55555555555'),
  ('77777777777'),
  ('99999999999');

-- Inserção de dados de teste na tabela Vende
INSERT INTO Vende (CNPJ, ItemID, Preco, Estoque, Garantia)
VALUES
  ('22222222222222', 1, 100.00, 50, '1 ano'),
  ('22222222222222', 2, 200.00, 100, '2 anos'),
  ('44444444444444', 3, 150.00, 30, '1 ano'),
  ('44444444444444', 4, 300.00, 80, '2 anos'),
  ('66666666666666', 5, 50.00, 20, '6 meses'),
  ('66666666666666', 6, 80.00, 60, '1 ano'),
  ('88888888888888', 7, 120.00, 40, '1 ano'),
  ('88888888888888', 8, 250.00, 90, '2 anos'),
  ('00000000000000', 9, 70.00, 10, '6 meses'),
  ('00000000000000', 10, 180.00, 70, '1 ano');

-- Inserção de dados de teste na tabela Faz Promoção
INSERT INTO FazPromocao (CNPJ, ItemID, DataInicio, DataFim, Tipo)
VALUES
  ('22222222222222', 1, '2023-06-01', '2023-06-15', 'Desconto'),
  ('22222222222222', 2, '2023-06-05', '2023-06-20', 'Brinde'),
  ('44444444444444', 3, '2023-06-02', '2023-06-10', 'Desconto'),
  ('44444444444444', 4, '2023-06-08', '2023-06-18', 'Brinde'),
  ('66666666666666', 5, '2023-06-03', '2023-06-12', 'Desconto'),
  ('66666666666666', 6, '2023-06-06', '2023-06-17', 'Brinde'),
  ('88888888888888', 7, '2023-06-04', '2023-06-14', 'Desconto'),
  ('88888888888888', 8, '2023-06-07', '2023-06-22', 'Brinde'),
  ('00000000000000', 9, '2023-06-09', '2023-06-19', 'Desconto'),
  ('00000000000000', 10, '2023-06-11', '2023-06-25', 'Brinde');

-- Inserção de dados de teste na tabela Busca
INSERT INTO Busca (ItemID, CPF, DataHora)
VALUES
  (1, '11111111111', '2023-06-01 10:00:00'),
  (2, '22222222222', '2023-06-02 14:30:00'),
  (3, '33333333333', '2023-06-03 09:45:00'),
  (4, '44444444444', '2023-06-04 17:20:00'),
  (5, '55555555555', '2023-06-05 11:10:00'),
  (6, '66666666666', '2023-06-06 13:45:00'),
  (7, '77777777777', '2023-06-07 15:30:00'),
  (8, '88888888888', '2023-06-08 10:25:00'),
  (9, '99999999999', '2023-06-09 12:50:00'),
  (10, '00000000000', '2023-06-10 16:15:00');

-- Inserção de dados de teste na tabela Deseja
INSERT INTO Deseja (ItemID, CPF, Quantidade)
VALUES
  (1, '11111111111', 2),
  (2, '22222222222', 3),
  (3, '33333333333', 1),
  (4, '44444444444', 2),
  (5, '55555555555', 1),
  (6, '66666666666', 4),
  (7, '77777777777', 2),
  (8, '88888888888', 3),
  (9, '99999999999', 1),
  (10, '00000000000', 2);

-- Inserção de dados de teste na tabela Paga
INSERT INTO Paga (PedidoID, MetodoPagamentoID, Parcelamento)
VALUES
  (1, 1, 'À vista'),
  (2, 2, '3 vezes'),
  (3, 3, 'À vista'),
  (4, 4, '2 vezes'),
  (5, 5, 'À vista'),
  (6, 6, '4 vezes'),
  (7, 7, 'À vista'),
  (8, 8, '3 vezes'),
  (9, 9, 'À vista'),
  (10, 10, '2 vezes');

-- Inserção de dados de teste na tabela Possui
INSERT INTO Possui (CPF, MetodoPagamentoID)
VALUES
  ('11111111111', 1),
  ('22222222222', 2),
  ('33333333333', 3),
  ('44444444444', 4),
  ('55555555555', 5),
  ('66666666666', 6),
  ('77777777777', 7),
  ('88888888888', 8),
  ('99999999999', 9),
  ('00000000000', 10);
