-- Script MySQL para PythonAnywhere
-- Substitua SEU_USUARIO pelo seu nome de usuário PythonAnywhere
-- Execute este script no MySQL console do PythonAnywhere

-- ========================================
-- INSTRUÇÕES DE USO:
-- ========================================
-- 1. Acesse o Dashboard do PythonAnywhere
-- 2. Vá em "Databases" 
-- 3. Clique em "Open MySQL console"
-- 4. Cole e execute este script
-- ========================================

-- Limpar tabelas existentes se necessário
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Item_Venda;
DROP TABLE IF EXISTS Venda;
DROP TABLE IF EXISTS Cliente;
DROP TABLE IF EXISTS Funcionario;
DROP TABLE IF EXISTS Produto;
SET FOREIGN_KEY_CHECKS = 1;

-- Tabela Cliente
CREATE TABLE Cliente (
    id_cliente INT AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    telefone VARCHAR(20),
    endereco TEXT,
    PRIMARY KEY (id_cliente),
    UNIQUE KEY unique_email (email),
    KEY idx_cliente_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Funcionario
CREATE TABLE Funcionario (
    id_funcionario INT AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cargo VARCHAR(100),
    salario DECIMAL(10,2),
    data_contratacao DATE,
    PRIMARY KEY (id_funcionario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Produto
CREATE TABLE Produto (
    id_produto INT AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    estoque INT DEFAULT 0,
    nome_imagem VARCHAR(255),
    url VARCHAR(255),
    PRIMARY KEY (id_produto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Venda
CREATE TABLE Venda (
    id_venda INT AUTO_INCREMENT,
    id_cliente INT,
    id_funcionario INT,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_venda),
    KEY idx_venda_cliente (id_cliente),
    KEY idx_venda_funcionario (id_funcionario),
    KEY idx_venda_data (data_venda),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente) ON DELETE SET NULL,
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Item_Venda
CREATE TABLE Item_Venda (
    id_item INT AUTO_INCREMENT,
    id_venda INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    preco_unitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_item),
    KEY idx_item_venda (id_venda),
    KEY idx_item_produto (id_produto),
    FOREIGN KEY (id_venda) REFERENCES Venda(id_venda) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES Produto(id_produto) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inserir dados de exemplo
INSERT INTO Cliente (nome, email, telefone, endereco) VALUES
('João Silva', 'joao@email.com', '11999999999', 'Rua A, 123'),
('Maria Santos', 'maria@email.com', '11888888888', 'Rua B, 456'),
('Pedro Oliveira', 'pedro@email.com', '11777777777', 'Rua C, 789');

INSERT INTO Funcionario (nome, cargo, salario, data_contratacao) VALUES
('Ana Costa', 'Vendedor', 2500.00, '2023-01-15'),
('Carlos Lima', 'Gerente', 4500.00, '2022-06-10'),
('Lucia Ferreira', 'Vendedor', 2300.00, '2023-03-20');

INSERT INTO Produto (nome, descricao, preco, estoque, nome_imagem) VALUES
('Notebook Dell', 'Notebook Dell Inspiron 15 8GB RAM', 2500.00, 10, 'notebook_dell.jpg'),
('Mouse Logitech', 'Mouse óptico Logitech M90', 25.00, 50, 'mouse_logitech.jpg'),
('Teclado Mecânico', 'Teclado mecânico gamer RGB', 150.00, 20, 'teclado_mecanico.jpg');

-- Verificar se as tabelas foram criadas
SHOW TABLES;

-- Verificar dados inseridos
SELECT 'Cliente' as tabela, COUNT(*) as registros FROM Cliente
UNION ALL
SELECT 'Funcionario', COUNT(*) FROM Funcionario  
UNION ALL
SELECT 'Produto', COUNT(*) FROM Produto;

-- Verificar estrutura das tabelas
DESCRIBE Cliente;
DESCRIBE Funcionario;
DESCRIBE Produto;
DESCRIBE Venda;
DESCRIBE Item_Venda;