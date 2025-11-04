# DAO MySQL

Este diretório contém a implementação dos Data Access Objects (DAO) para MySQL.

## Estrutura

- `db.py` - Gerenciamento de conexões e pool de conexões MySQL
- `cliente_dao.py` - DAO para operações com clientes
- `funcionario_dao.py` - DAO para operações com funcionários
- `produto_dao.py` - DAO para operações com produtos
- `venda_dao.py` - DAO para operações com vendas
- `item_venda_dao.py` - DAO para operações com itens de venda

## Configuração

### Variáveis de Ambiente

Você pode configurar a conexão MySQL através das seguintes variáveis de ambiente:

- `MYSQL_HOST` - Host do servidor MySQL (padrão: localhost)
- `MYSQL_PORT` - Porta do servidor MySQL (padrão: 3306)
- `MYSQL_USER` - Usuário MySQL (padrão: root)
- `MYSQL_PASSWORD` - Senha do usuário MySQL (padrão: 123456)
- `MYSQL_DATABASE` - Nome do banco de dados (padrão: e_comerce_flask)

### Configuração via Código

```python
from dao_mysql.db import init_db

# Configuração via dicionário
db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'sua_senha',
    'database': 'e_comerce_flask'
}

init_db(db_config)
```

## Uso

### Exemplo de uso básico

```python
from dao_mysql.cliente_dao import ClienteDAO

# Inicializar o banco
from dao_mysql.db import init_db
init_db()

# Usar o DAO
cliente_dao = ClienteDAO()

# Listar todos os clientes
clientes = cliente_dao.listar_clientes()

# Buscar um cliente específico
cliente = cliente_dao.buscar_cliente(1)

# Inserir um novo cliente
cliente_dao.inserir_cliente(1, "João Silva", "joao@email.com", "123456789", "Rua A, 123")
```

## Dependências

Para usar o DAO MySQL, você precisa instalar:

```bash
pip install mysql-connector-python>=8.0.33
```

## Características

- **Pool de Conexões**: Utiliza pool de conexões para melhor performance
- **Context Manager**: Usa context managers para gerenciamento automático de transações
- **Dictionary Cursor**: Retorna resultados como dicionários para facilitar o uso
- **Auto Commit/Rollback**: Commit automático em caso de sucesso, rollback em caso de erro
- **UTF-8 Support**: Configurado para usar UTF-8 com collation unicode

## Estrutura do Banco

O DAO espera as seguintes tabelas no MySQL:

- `Cliente` (id_cliente, nome, email, telefone, endereco)
- `Funcionario` (id_funcionario, nome, cargo, salario, data_contratacao)
- `Produto` (id_produto, nome, descricao, preco, estoque, nome_imagem, url)
- `Venda` (id_venda, id_cliente, id_funcionario, data_venda, total)
- `Item_Venda` (id_item, id_venda, id_produto, quantidade, preco_unitario)