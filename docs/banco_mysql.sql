-- Script para criação das tabelas no MySQL
-- Banco de dados: e_comerce_flask

-- Criar banco de dados (caso não exista)
CREATE DATABASE IF NOT EXISTS e_comerce_flask 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE e_comerce_flask;

-- Tabela Cliente
CREATE TABLE IF NOT EXISTS Cliente (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    telefone VARCHAR(20),
    endereco TEXT
);

-- Tabela Funcionario
CREATE TABLE IF NOT EXISTS Funcionario (
    id_funcionario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cargo VARCHAR(100),
    salario DECIMAL(10,2),
    data_contratacao DATE
);

-- Tabela Produto
CREATE TABLE IF NOT EXISTS Produto (
    id_produto INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    estoque INT DEFAULT 0,
    nome_imagem VARCHAR(255),
    url VARCHAR(255)
);

-- Tabela Venda
CREATE TABLE IF NOT EXISTS Venda (
    id_venda INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    id_funcionario INT,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente) ON DELETE SET NULL,
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario) ON DELETE SET NULL
);

-- Tabela Item_Venda
CREATE TABLE IF NOT EXISTS Item_Venda (
    id_item INT PRIMARY KEY AUTO_INCREMENT,
    id_venda INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    preco_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_venda) REFERENCES Venda(id_venda) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES Produto(id_produto) ON DELETE CASCADE
);

-- Índices para melhor performance
CREATE INDEX idx_cliente_email ON Cliente(email);
CREATE INDEX idx_venda_cliente ON Venda(id_cliente);
CREATE INDEX idx_venda_funcionario ON Venda(id_funcionario);
CREATE INDEX idx_venda_data ON Venda(data_venda);
CREATE INDEX idx_item_venda ON Item_Venda(id_venda);
CREATE INDEX idx_item_produto ON Item_Venda(id_produto);

-- Dados de exemplo (opcional)
INSERT IGNORE INTO Cliente (nome, email, telefone, endereco) VALUES
('João Silva', 'joao@email.com', '11999999999', 'Rua A, 123'),
('Maria Santos', 'maria@email.com', '11888888888', 'Rua B, 456'),
('Pedro Oliveira', 'pedro@email.com', '11777777777', 'Rua C, 789');

INSERT IGNORE INTO Funcionario (nome, cargo, salario, data_contratacao) VALUES
('Ana Costa', 'Vendedor', 2500.00, '2023-01-15'),
('Carlos Lima', 'Gerente', 4500.00, '2022-06-10'),
('Lucia Ferreira', 'Vendedor', 2300.00, '2023-03-20');

INSERT IGNORE INTO Produto (nome, descricao, preco, estoque, nome_imagem) VALUES
('Notebook Dell', 'Notebook Dell Inspiron 15 8GB RAM', 2500.00, 10, 'notebook_dell.jpg'),
('Mouse Logitech', 'Mouse óptico Logitech M90', 25.00, 50, 'mouse_logitech.jpg'),
('Teclado Mecânico', 'Teclado mecânico gamer RGB', 150.00, 20, 'teclado_mecanico.jpg');