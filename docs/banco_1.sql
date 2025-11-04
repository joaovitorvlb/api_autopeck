----------------------------------------------------------------
-- Banco de Dados: Sistema de Vendas
-- Descrição: Criação de tabelas para gerenciar funcionários, clientes, produtos e vendas
----------------------------------------------------------------

CREATE TABLE Funcionario (
    id_funcionario INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50),
    salario DECIMAL(10,2),
    data_contratacao DATE
);

CREATE TABLE Cliente (
    id_cliente INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    endereco VARCHAR(200)
);

CREATE TABLE Produto (
    id_produto INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(200),
    preco DECIMAL(10,2) NOT NULL,
    estoque INT NOT NULL
);

CREATE TABLE Venda (
    id_venda INT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_funcionario INT NOT NULL,
    data_venda DATE NOT NULL,
    total DECIMAL(10,2),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario)
);

CREATE TABLE Item_Venda (
    id_item INT PRIMARY KEY,
    id_venda INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_venda) REFERENCES Venda(id_venda),
    FOREIGN KEY (id_produto) REFERENCES Produto(id_produto)
);

-- Verifica a existência das tabelas criadas
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

-- seleciona funcionarios
SELECT * FROM Funcionario;

-- seleciona clientes
SELECT * FROM Cliente;

-- seleciona produtos
SELECT * FROM Produto;

-- seleciona vendas
SELECT * FROM Venda;

-- seleciona itens de venda
SELECT * FROM Item_Venda;

-- Insere dados na tabela Funcionario
INSERT INTO Funcionario (id_funcionario, nome, cargo, salario, data_contratacao)
VALUES (1, 'João Silva', 'Gerente', 5000.00, '2022-01-15'),
       (2, 'Maria Oliveira', 'Vendedor', 3000.00, '2022-03-22');        


-- Insere dados na tabela Cliente
INSERT INTO Cliente (id_cliente, nome, email, telefone, endereco)
VALUES
(1, 'Ana Souza', 'ana.souza@example.com', '+55 11 99999-0001', 'Rua das Flores, 123, São Paulo, SP'),
(2, 'Carlos Pereira', 'carlos.pereira@example.com', '+55 21 98888-0002', 'Av. Brasil, 456, Rio de Janeiro, RJ'),
(3, 'Mariana Costa', 'mariana.costa@example.com', '+55 31 97777-0003', 'Praça Sete, 789, Belo Horizonte, MG'),
(4, 'Roberto Lima', 'roberto.lima@example.com', '+55 41 96666-0004', 'Rua XV de Novembro, 101, Curitiba, PR'),
(5, 'Luciana Ramos', 'luciana.ramos@example.com', '+55 51 95555-0005', 'Av. Ipiranga, 202, Porto Alegre, RS');


-- Insere dados na tabela Produto (auto peças)
INSERT INTO Produto (id_produto, nome, descricao, preco, estoque)
VALUES
(1, 'Filtro de Óleo', 'Filtro de óleo para motores 1.0 a 2.0', 29.90, 100),
(2, 'Pastilha de Freio', 'Jogo de pastilhas de freio dianteiro', 89.90, 50),
(3, 'Amortecedor', 'Amortecedor dianteiro universal', 199.90, 30),
(4, 'Correia Dentada', 'Correia de distribuição para motores flex', 45.90, 80),
(5, 'Vela de Ignição', 'Jogo com 4 velas de ignição', 69.90, 60),
(6, 'Óleo de Motor', 'Óleo sintético 5W30 1L', 35.90, 150),
(7, 'Bateria Automotiva', 'Bateria 60Ah', 359.90, 25),
(8, 'Filtro de Ar', 'Filtro de ar motor 1.0 a 2.0', 25.90, 90),
(9, 'Radiador', 'Radiador de água universal', 299.90, 20),
(10, 'Kit Embreagem', 'Kit completo de embreagem', 459.90, 15);


-----------------------------------------------------------
-- Tabelas de log e auditoria (opcional)
-----------------------------------------------------------
CREATE TABLE auditoria (
    id SERIAL PRIMARY KEY,
    tabela TEXT,
    operacao TEXT,
    registro_id INTEGER,
    usuario TEXT,
    data TIMESTAMP DEFAULT NOW(),
    dados JSONB
);

-- seleciona auditoria
SELECT * FROM auditoria;

-- Função generica para registrar logs das tabelas
CREATE OR REPLACE FUNCTION auditoria_func()
RETURNS TRIGGER AS $$
DECLARE
    registro JSONB;
BEGIN
    IF (TG_OP = 'DELETE') THEN
        registro = to_jsonb(OLD);
    ELSE
        registro = to_jsonb(NEW);
    END IF;

    INSERT INTO auditoria (tabela, operacao, registro_id, dados)
    VALUES (TG_TABLE_NAME, TG_OP, COALESCE(NEW.id, OLD.id), registro);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers para as tabelas
CREATE TRIGGER auditoria_venda
AFTER INSERT OR UPDATE OR DELETE ON venda
FOR EACH ROW EXECUTE FUNCTION auditoria_func();

CREATE TRIGGER auditoria_cliente
AFTER INSERT OR UPDATE OR DELETE ON cliente
FOR EACH ROW EXECUTE FUNCTION auditoria_func();

CREATE TRIGGER auditoria_produto
AFTER INSERT OR UPDATE OR DELETE ON produto
FOR EACH ROW EXECUTE FUNCTION auditoria_func();

DROP TRIGGER IF EXISTS auditoria_venda ON venda;
DROP TRIGGER IF EXISTS auditoria_cliente ON cliente;
DROP TRIGGER IF EXISTS auditoria_produto ON produto;

DROP FUNCTION IF EXISTS auditoria_func() CASCADE;

-- Manipula dados na tabela Cliente para testar logs
-- Inserção
INSERT INTO Cliente (id_cliente, nome, email, telefone, endereco)
VALUES (6, 'Fernando Santos', 'fernando.santos@example.com', '+55 11 94444-0006', 'Rua Augusta, 303, São Paulo, SP');

-- Atualização
UPDATE Cliente
SET telefone = '+55 11 93333-0006'
WHERE id_cliente = 6;   

-- Exclusão
DELETE FROM Cliente
WHERE id_cliente = 6;

