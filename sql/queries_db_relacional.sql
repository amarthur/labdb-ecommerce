-- Selecionar todas as empresas e suas localizações

SELECT CNPJ, Nome, Localizacao FROM Empresa;

-- Atualizar o status de um pedido

UPDATE Pedido SET Status = 'Concluído' WHERE ID = 1;

-- Inserir uma nova transportadora

INSERT INTO Transportadora (CNPJ) VALUES ('123456789');

-- Remover um produto e todas as suas vendas relacionadas

DELETE FROM Vende WHERE ItemID = 1;
DELETE FROM Produto WHERE ID = 1;

-- Selecionar todos os pedidos concluídos junto com as informações do usuário que os fez

SELECT p.ID, p.Status, p.Observacoes, u.Nome, u.Email
FROM Pedido p
JOIN Usuario u ON p.CPF = u.CPF
WHERE p.Status = 'Concluído';

-- Calcular o ranking de cada empresa com base na quantidade de vendas realizadas pelos vendedores

UPDATE Empresa SET Ranking = (
  SELECT SUM(QuantidadeVendas)
  FROM Vendedor
  WHERE CNPJ = Empresa.CNPJ
);
