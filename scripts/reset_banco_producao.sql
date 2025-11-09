-- ================================================================
-- Script de Reset para Produção - PythonAnywhere
-- ================================================================
-- Este script limpa todos os dados de teste e insere dados padrão
--
-- ATENÇÃO: Esta operação é DESTRUTIVA e NÃO PODE SER DESFEITA!
--
-- Como usar:
-- 1. Acesse o MySQL Console no PythonAnywhere
-- 2. Cole e execute este script completo
-- 3. Verifique se os dados padrão foram inseridos
-- ================================================================

-- Selecionar o banco de dados
USE seu_usuario$default;  -- ⚠️ SUBSTITUA "seu_usuario" pelo seu nome de usuário

-- Desabilitar checagem de chaves estrangeiras temporariamente
SET FOREIGN_KEY_CHECKS = 0;

-- ================================================================
-- LIMPEZA DE DADOS DE TESTE
-- ================================================================

-- 1. Limpar todas as tabelas (ordem importante por causa das FKs)
TRUNCATE TABLE Item_Venda;
TRUNCATE TABLE Venda;
TRUNCATE TABLE Produto;
TRUNCATE TABLE Cliente;
TRUNCATE TABLE Funcionario;

-- Reabilitar checagem de chaves estrangeiras
SET FOREIGN_KEY_CHECKS = 1;

-- ================================================================
-- INSERIR DADOS PADRÃO
-- ================================================================

-- 1. FUNCIONÁRIOS (para login)
INSERT INTO Funcionario (nome, cargo, salario, data_contratacao) VALUES
('Maria Silva', 'Vendedora', 2500.00, '2023-01-15'),
('Admin Sistema', 'Administrador', 4500.00, '2022-06-10'),
('Carlos Lima', 'Gerente', 3500.00, '2023-03-20');

-- 2. CLIENTES INICIAIS
INSERT INTO Cliente (nome, email, telefone, endereco) VALUES
('João Silva', 'joao@email.com', '11999999999', 'Rua A, 123'),
('Ana Santos', 'ana@email.com', '11888888888', 'Rua B, 456'),
('Pedro Oliveira', 'pedro@email.com', '11777777777', 'Rua C, 789');

-- 3. PRODUTOS PADRÃO (AutoPeças - sem imagens)
INSERT INTO Produto (nome, descricao, preco, estoque, nome_imagem) VALUES
('Filtro de Óleo', 'Filtro de óleo para motores 1.0 a 2.0', 29.90, 100, NULL),
('Pastilha de Freio', 'Jogo de pastilhas de freio dianteiro', 89.90, 50, NULL),
('Amortecedor Dianteiro', 'Amortecedor dianteiro para carros populares', 189.90, 30, NULL),
('Vela de Ignição', 'Jogo de velas de ignição NGK', 45.90, 80, NULL),
('Correia Dentada', 'Correia dentada para motores 1.0/1.4/1.6', 65.90, 25, NULL);

-- ================================================================
-- VERIFICAÇÃO
-- ================================================================

-- Contar registros inseridos
SELECT 
    'Funcionários' AS Tabela, 
    COUNT(*) AS Total 
FROM Funcionario
UNION ALL
SELECT 
    'Clientes' AS Tabela, 
    COUNT(*) AS Total 
FROM Cliente
UNION ALL
SELECT 
    'Produtos' AS Tabela, 
    COUNT(*) AS Total 
FROM Produto
UNION ALL
SELECT 
    'Vendas' AS Tabela, 
    COUNT(*) AS Total 
FROM Venda
UNION ALL
SELECT 
    'Itens de Venda' AS Tabela, 
    COUNT(*) AS Total 
FROM Item_Venda;

-- ================================================================
-- RESULTADO ESPERADO:
-- ================================================================
-- Funcionários: 3
-- Clientes: 3
-- Produtos: 5
-- Vendas: 0
-- Itens de Venda: 0
-- ================================================================

-- ✅ Se os números acima estiverem corretos, o reset foi bem-sucedido!
