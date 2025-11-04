# Configuração MySQL no PythonAnywhere - Guia Completo

## 1. Configuração Inicial no PythonAnywhere

### 1.1 Acessar o Console MySQL
No dashboard do PythonAnywhere:
1. Vá para **"Databases"**
2. Clique em **"Open MySQL console"**
3. Ou use o terminal: `mysql -u SEU_USUARIO -p'SUA_SENHA' SEU_USUARIO$default`

### 1.2 Informações Importantes do PythonAnywhere
- **Host MySQL**: `SEU_USUARIO.mysql.pythonanywhere-services.com`
- **Usuário**: `SEU_USUARIO` (mesmo nome da sua conta)
- **Banco padrão**: `SEU_USUARIO$default`
- **Porta**: 3306

## 2. Script MySQL Otimizado para PythonAnywhere

### 2.1 Script de Criação das Tabelas
```sql
-- Use o banco padrão do PythonAnywhere
USE SEU_USUARIO$default;

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

-- Dados de exemplo
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
```

## 3. Configuração Python para PythonAnywhere

### 3.1 Arquivo de Configuração Específico
Crie `config_pythonanywhere.py`:

```python
import os

# Configurações específicas do PythonAnywhere
PYTHONANYWHERE_CONFIG = {
    'host': 'SEU_USUARIO.mysql.pythonanywhere-services.com',
    'port': 3306,
    'user': 'SEU_USUARIO',
    'password': 'SUA_SENHA_MYSQL',  # Defina nas variáveis de ambiente
    'database': 'SEU_USUARIO$default',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': False,
    'ssl_disabled': True  # PythonAnywhere não requer SSL
}

def get_mysql_config():
    """Retorna configuração MySQL para PythonAnywhere"""
    return {
        'host': os.getenv('MYSQL_HOST', PYTHONANYWHERE_CONFIG['host']),
        'port': int(os.getenv('MYSQL_PORT', PYTHONANYWHERE_CONFIG['port'])),
        'user': os.getenv('MYSQL_USER', PYTHONANYWHERE_CONFIG['user']),
        'password': os.getenv('MYSQL_PASSWORD', PYTHONANYWHERE_CONFIG['password']),
        'database': os.getenv('MYSQL_DATABASE', PYTHONANYWHERE_CONFIG['database']),
        'charset': PYTHONANYWHERE_CONFIG['charset'],
        'collation': PYTHONANYWHERE_CONFIG['collation'],
        'autocommit': PYTHONANYWHERE_CONFIG['autocommit'],
        'ssl_disabled': PYTHONANYWHERE_CONFIG['ssl_disabled']
    }
```

### 3.2 Atualizar o arquivo db.py para PythonAnywhere
```python
import os
from contextlib import contextmanager
import mysql.connector
from mysql.connector import pooling

_pool = None

def init_db(db_config: dict = None, minconn: int = 1, maxconn: int = 3):
    """Inicializa o pool de conexões MySQL otimizado para PythonAnywhere"""
    global _pool
    if _pool is not None:
        return

    if db_config is None:
        # Configuração específica para PythonAnywhere
        db_config = {
            'host': os.getenv('MYSQL_HOST', 'SEU_USUARIO.mysql.pythonanywhere-services.com'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'user': os.getenv('MYSQL_USER', 'SEU_USUARIO'),
            'password': os.getenv('MYSQL_PASSWORD'),  # OBRIGATÓRIO definir
            'database': os.getenv('MYSQL_DATABASE', 'SEU_USUARIO$default'),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': False,
            'ssl_disabled': True,  # PythonAnywhere não precisa de SSL
            'connection_timeout': 60,
            'pool_reset_session': True
        }

    # Pool menor para PythonAnywhere (limite de conexões)
    _pool = pooling.MySQLConnectionPool(
        pool_name="mysql_pool",
        pool_size=min(maxconn, 3),  # Máximo 3 conexões no free tier
        pool_reset_session=True,
        **db_config
    )

@contextmanager
def get_cursor(commit: bool = True):
    """Context manager otimizado para PythonAnywhere"""
    if _pool is None:
        raise RuntimeError("Connection pool não inicializado. Chame init_db() primeiro.")

    conn = None
    cur = None
    try:
        conn = _pool.get_connection()
        cur = conn.cursor(dictionary=True, buffered=True)
        yield cur
        if commit:
            conn.commit()
    except mysql.connector.Error as e:
        if conn:
            try:
                conn.rollback()
            except:
                pass
        raise e
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except:
                pass
        raise e
    finally:
        if cur:
            try:
                cur.close()
            except:
                pass
        if conn:
            try:
                conn.close()
            except:
                pass

def close_pool():
    """Fecha o pool de conexões"""
    global _pool
    if _pool is not None:
        try:
            _pool._remove_connections()
        except:
            pass
        _pool = None
```

## 4. Variáveis de Ambiente no PythonAnywhere

### 4.1 Configurar no WSGI file
No arquivo `mysite/wsgi.py`:

```python
import os
import sys

# Configurações MySQL para PythonAnywhere
os.environ['MYSQL_HOST'] = 'SEU_USUARIO.mysql.pythonanywhere-services.com'
os.environ['MYSQL_PORT'] = '3306'
os.environ['MYSQL_USER'] = 'SEU_USUARIO'
os.environ['MYSQL_PASSWORD'] = 'SUA_SENHA_MYSQL'  # SUBSTITUA pela sua senha
os.environ['MYSQL_DATABASE'] = 'SEU_USUARIO$default'

# Adicionar seu projeto ao path
path = '/home/SEU_USUARIO/api_autopeck'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### 4.2 Arquivo .env (opcional)
```env
MYSQL_HOST=SEU_USUARIO.mysql.pythonanywhere-services.com
MYSQL_PORT=3306
MYSQL_USER=SEU_USUARIO
MYSQL_PASSWORD=SUA_SENHA_MYSQL
MYSQL_DATABASE=SEU_USUARIO$default
```

## 5. Script de Inicialização Automática

### 5.1 Criar script setup_mysql.py
```python
#!/usr/bin/env python3
"""
Script para configurar automaticamente o MySQL no PythonAnywhere
Execute: python setup_mysql.py
"""

import os
import mysql.connector
from mysql.connector import Error

def setup_mysql_pythonanywhere():
    """Configura o banco MySQL no PythonAnywhere"""
    
    # Configurações (SUBSTITUA pelos seus dados)
    config = {
        'host': 'SEU_USUARIO.mysql.pythonanywhere-services.com',
        'port': 3306,
        'user': 'SEU_USUARIO',
        'password': input('Digite sua senha MySQL: '),  # Ou defina aqui
        'database': 'SEU_USUARIO$default',
        'charset': 'utf8mb4',
        'ssl_disabled': True
    }
    
    # SQL para criar as tabelas
    sql_script = """
    SET FOREIGN_KEY_CHECKS = 0;
    DROP TABLE IF EXISTS Item_Venda;
    DROP TABLE IF EXISTS Venda;
    DROP TABLE IF EXISTS Cliente;
    DROP TABLE IF EXISTS Funcionario;
    DROP TABLE IF EXISTS Produto;
    SET FOREIGN_KEY_CHECKS = 1;

    CREATE TABLE Cliente (
        id_cliente INT PRIMARY KEY AUTO_INCREMENT,
        nome VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE,
        telefone VARCHAR(20),
        endereco TEXT,
        INDEX idx_cliente_email (email)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    CREATE TABLE Funcionario (
        id_funcionario INT PRIMARY KEY AUTO_INCREMENT,
        nome VARCHAR(255) NOT NULL,
        cargo VARCHAR(100),
        salario DECIMAL(10,2),
        data_contratacao DATE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    CREATE TABLE Produto (
        id_produto INT PRIMARY KEY AUTO_INCREMENT,
        nome VARCHAR(255) NOT NULL,
        descricao TEXT,
        preco DECIMAL(10,2) NOT NULL,
        estoque INT DEFAULT 0,
        nome_imagem VARCHAR(255),
        url VARCHAR(255)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
    
    try:
        # Conectar ao MySQL
        print("Conectando ao MySQL...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Executar comandos SQL
        print("Criando tabelas...")
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        connection.commit()
        print("✅ Tabelas criadas com sucesso!")
        
        # Inserir dados de exemplo
        print("Inserindo dados de exemplo...")
        insert_data(cursor, connection)
        
        print("✅ Setup MySQL concluído com sucesso!")
        
    except Error as e:
        print(f"❌ Erro: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def insert_data(cursor, connection):
    """Insere dados de exemplo"""
    insert_queries = [
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
    
    for query in insert_queries:
        cursor.execute(query)
    
    connection.commit()

if __name__ == "__main__":
    setup_mysql_pythonanywhere()
```

## 6. Checklist de Implementação

### ✅ Passos Obrigatórios:

1. **Substituir placeholders**:
   - `SEU_USUARIO` → seu nome de usuário PythonAnywhere
   - `SUA_SENHA_MYSQL` → sua senha MySQL

2. **Configurar variáveis de ambiente** no arquivo WSGI

3. **Executar o script SQL** no console MySQL do PythonAnywhere

4. **Testar conexão** com o script Python

5. **Configurar DAO** para usar as novas configurações

### ⚠️ Limitações do PythonAnywhere (Free Tier):
- Máximo 3 conexões simultâneas ao MySQL
- 512MB de espaço em disco
- CPU limitada
- Apenas 1 aplicação web

### 🔧 Otimizações:
- Pool de conexões pequeno (máximo 3)
- Timeout de conexão aumentado
- SSL desabilitado (não necessário)
- Índices otimizados para consultas rápidas

## 7. Teste Final

Execute este script para testar:

```python
from dao_mysql.db import init_db, get_cursor

# Testar conexão
try:
    init_db()
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) as total FROM Cliente")
        result = cur.fetchone()
        print(f"✅ Conexão OK! Total de clientes: {result['total']}")
except Exception as e:
    print(f"❌ Erro na conexão: {e}")
```

Este guia garante uma implementação sem complicações no PythonAnywhere! 🚀