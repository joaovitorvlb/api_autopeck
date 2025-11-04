#!/usr/bin/env python3
"""
Script para configurar automaticamente o MySQL no PythonAnywhere
Execute: python setup_mysql_pythonanywhere.py

IMPORTANTE: Substitua os placeholders antes de executar:
- SEU_USUARIO → seu nome de usuário PythonAnywhere
- SUA_SENHA_MYSQL → sua senha MySQL
"""

import os
import mysql.connector
from mysql.connector import Error

# ========================================
# CONFIGURAÇÕES - SUBSTITUA PELOS SEUS DADOS
# ========================================
PYTHONANYWHERE_USER = "SEU_USUARIO"  # ← SUBSTITUA pelo seu usuário
MYSQL_PASSWORD = "SUA_SENHA_MYSQL"   # ← SUBSTITUA pela sua senha

def get_config():
    """Retorna configuração MySQL para PythonAnywhere"""
    return {
        'host': f'{PYTHONANYWHERE_USER}.mysql.pythonanywhere-services.com',
        'port': 3306,
        'user': PYTHONANYWHERE_USER,
        'password': MYSQL_PASSWORD,
        'database': f'{PYTHONANYWHERE_USER}$default',
        'charset': 'utf8mb4',
        'ssl_disabled': True,
        'autocommit': False
    }

def create_tables_sql():
    """Retorna SQL para criar todas as tabelas"""
    return """
-- Limpar tabelas existentes (se necessário)
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Item_Venda;
DROP TABLE IF EXISTS Venda;
DROP TABLE IF EXISTS Cliente;
DROP TABLE IF EXISTS Funcionario;
DROP TABLE IF EXISTS Produto;
SET FOREIGN_KEY_CHECKS = 1;

-- Tabela Cliente
CREATE TABLE Cliente (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    telefone VARCHAR(20),
    endereco TEXT,
    INDEX idx_cliente_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Funcionario
CREATE TABLE Funcionario (
    id_funcionario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cargo VARCHAR(100),
    salario DECIMAL(10,2),
    data_contratacao DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Produto
CREATE TABLE Produto (
    id_produto INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    estoque INT DEFAULT 0,
    nome_imagem VARCHAR(255),
    url VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Venda
CREATE TABLE Venda (
    id_venda INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    id_funcionario INT,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente) ON DELETE SET NULL,
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario) ON DELETE SET NULL,
    INDEX idx_venda_cliente (id_cliente),
    INDEX idx_venda_funcionario (id_funcionario),
    INDEX idx_venda_data (data_venda)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Item_Venda
CREATE TABLE Item_Venda (
    id_item INT PRIMARY KEY AUTO_INCREMENT,
    id_venda INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    preco_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_venda) REFERENCES Venda(id_venda) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES Produto(id_produto) ON DELETE CASCADE,
    INDEX idx_item_venda (id_venda),
    INDEX idx_item_produto (id_produto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

def insert_sample_data():
    """Retorna SQL para inserir dados de exemplo"""
    return [
        """INSERT INTO Cliente (nome, email, telefone, endereco) VALUES
        ('João Silva', 'joao@email.com', '11999999999', 'Rua A, 123'),
        ('Maria Santos', 'maria@email.com', '11888888888', 'Rua B, 456'),
        ('Pedro Oliveira', 'pedro@email.com', '11777777777', 'Rua C, 789')""",
        
        """INSERT INTO Funcionario (nome, cargo, salario, data_contratacao) VALUES
        ('Ana Costa', 'Vendedor', 2500.00, '2023-01-15'),
        ('Carlos Lima', 'Gerente', 4500.00, '2022-06-10'),
        ('Lucia Ferreira', 'Vendedor', 2300.00, '2023-03-20')""",
        
        """INSERT INTO Produto (nome, descricao, preco, estoque, nome_imagem) VALUES
        ('Notebook Dell', 'Notebook Dell Inspiron 15 8GB RAM', 2500.00, 10, 'notebook_dell.jpg'),
        ('Mouse Logitech', 'Mouse óptico Logitech M90', 25.00, 50, 'mouse_logitech.jpg'),
        ('Teclado Mecânico', 'Teclado mecânico gamer RGB', 150.00, 20, 'teclado_mecanico.jpg')"""
    ]

def setup_mysql_pythonanywhere():
    """Configura o banco MySQL no PythonAnywhere"""
    
    # Verificar se as configurações foram alteradas
    if PYTHONANYWHERE_USER == "SEU_USUARIO" or MYSQL_PASSWORD == "SUA_SENHA_MYSQL":
        print("❌ ERRO: Você precisa editar este arquivo e substituir:")
        print("   - SEU_USUARIO → seu nome de usuário PythonAnywhere")
        print("   - SUA_SENHA_MYSQL → sua senha MySQL")
        return False
    
    config = get_config()
    
    try:
        # Conectar ao MySQL
        print(f"📡 Conectando ao MySQL: {config['host']}")
        print(f"👤 Usuário: {config['user']}")
        print(f"🗄️  Banco: {config['database']}")
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("✅ Conexão estabelecida com sucesso!")
        
        # Criar tabelas
        print("\n🔨 Criando tabelas...")
        sql_script = create_tables_sql()
        
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                    print(f"   ✓ Executado: {statement[:50]}...")
                except Error as e:
                    print(f"   ⚠️  Aviso: {e}")
        
        connection.commit()
        print("✅ Tabelas criadas com sucesso!")
        
        # Inserir dados de exemplo
        print("\n📝 Inserindo dados de exemplo...")
        for query in insert_sample_data():
            try:
                cursor.execute(query)
                affected = cursor.rowcount
                table_name = query.split()[2]  # Pega o nome da tabela
                print(f"   ✓ {table_name}: {affected} registros inseridos")
            except Error as e:
                print(f"   ⚠️  Aviso: {e}")
        
        connection.commit()
        
        # Verificar instalação
        print("\n🔍 Verificando instalação...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"   📊 Tabelas criadas: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   📋 {table_name}: {count} registros")
        
        print("\n🎉 Setup MySQL concluído com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Configure as variáveis de ambiente no arquivo WSGI")
        print("2. Atualize o dao_mysql/db.py com as configurações")
        print("3. Teste a API com a nova configuração")
        
        return True
        
    except Error as e:
        print(f"\n❌ Erro MySQL: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Erro geral: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Conexão fechada")

def test_connection():
    """Testa apenas a conexão, sem criar tabelas"""
    config = get_config()
    
    try:
        print(f"🔍 Testando conexão com {config['host']}...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        
        if result[0] == 1:
            print("✅ Conexão OK!")
            return True
        else:
            print("❌ Conexão falhou")
            return False
            
    except Error as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Apenas testar conexão
        test_connection()
    else:
        # Setup completo
        print("🚀 Configurando MySQL para PythonAnywhere...")
        print("=" * 50)
        success = setup_mysql_pythonanywhere()
        
        if success:
            print("\n" + "=" * 50)
            print("✅ SUCESSO! Banco configurado e pronto para uso.")
        else:
            print("\n" + "=" * 50)
            print("❌ FALHOU! Verifique as configurações e tente novamente.")