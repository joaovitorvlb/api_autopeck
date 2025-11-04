-- Criação das tabelas para o banco SQLite

CREATE TABLE IF NOT EXISTS Funcionario (
    id_funcionario INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    cargo TEXT,
    salario REAL,
    data_contratacao TEXT
);

CREATE TABLE IF NOT EXISTS Cliente (
    id_cliente INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT,
    telefone TEXT,
    endereco TEXT
);

CREATE TABLE IF NOT EXISTS Produto (
    id_produto INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL,
    estoque INTEGER NOT NULL,
    nome_imagem TEXT
);

CREATE TABLE IF NOT EXISTS Venda (
    id_venda INTEGER PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    data_venda TEXT NOT NULL,
    total REAL,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario)
);

CREATE TABLE IF NOT EXISTS Item_Venda (
    id_item INTEGER PRIMARY KEY,
    id_venda INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    FOREIGN KEY (id_venda) REFERENCES Venda(id_venda),
    FOREIGN KEY (id_produto) REFERENCES Produto(id_produto)
);

-- Seleciona todos os registros das tabelas

SELECT * FROM Funcionario;
SELECT * FROM Cliente;
SELECT * FROM Produto;
SELECT * FROM Venda;
SELECT * FROM Item_Venda;

-- Comandos de apagamento de tabelas
DROP TABLE IF EXISTS Item_Venda;
DROP TABLE IF EXISTS Venda;
DROP TABLE IF EXISTS Produto;
DROP TABLE IF EXISTS Cliente;
DROP TABLE IF EXISTS Funcionario;
