# 🛒 Estrutura de Rotas da API - E-commerce com Flask e PyQt

Este documento descreve a organização das rotas da aplicação de e-commerce desenvolvida em **Python**, utilizando **Flask** como servidor e **PyQt** como interface gráfica.

---

## 📘 Visão Geral

O sistema segue a estrutura de um e-commerce simples, com as seguintes entidades principais:

- **Funcionario** — representa quem realiza as vendas.  
- **Cliente** — representa o comprador.  
- **Produto** — representa os itens disponíveis para venda.  
- **Venda** — representa a transação de venda feita por um funcionário a um cliente.  
- **Item_Venda** — representa os produtos específicos incluídos em uma venda.

Cada entidade possui rotas específicas que permitem as operações **CRUD** (Create, Read, Update, Delete) e algumas rotas compostas para relacionamentos.

---

## 🧍‍♂️ 1. Rotas de Cliente

Gerenciam os dados dos clientes do sistema.

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/clientes` | Cadastra um novo cliente |
| `GET` | `/clientes` | Lista todos os clientes |
| `GET` | `/clientes/<id>` | Retorna os dados de um cliente específico |
| `PUT` | `/clientes/<id>` | Atualiza os dados de um cliente |
| `DELETE` | `/clientes/<id>` | Exclui um cliente do banco de dados |

### Exemplo de corpo JSON (`POST /clientes`)
```json
{
  "nome": "João Barbosa",
  "email": "joao@email.com",
  "telefone": "(11) 99999-9999"
}
```
### Exemplo de resposta da rota (`GET /clientes/<id>`)
```json
{
  "id": 1,
  "nome": "João Barbosa",
  "email": "joao@email.com",
  "telefone": "(11) 99999-9999",
  "created_at": "2023-11-20T14:30:00Z"
}
```

## 👥 2. Rotas de Funcionário 

Gerenciam os dados dos funcionários responsáveis pelas vendas.

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/funcionarios` | Cadastra novo funcionário |
| `GET` | `/funcionarios` | Lista todos os funcionários |
| `GET` | `/funcionarios/<id>` | Retorna dados de um funcionário |
| `PUT` | `/funcionarios/<id>` | Atualiza informações do funcionário |
| `DELETE` | `/funcionarios/<id>` | Exclui funcionário do banco |

### Exemplo de corpo JSON (`POST /funcionarios`)
```json
{
  "nome": "Maria Silva",
  "cargo": "Vendedora",
  "senha": "1234"
}
```

### Exemplo de resposta da rota (`GET /funcionarios/<id>`)
```json
{
  "id": 2,
  "nome": "Maria Silva",
  "cargo": "Vendedora",
  "created_at": "2023-11-20T14:30:00Z"
}
```


## 📦 3. Rotas de Produto

Controlam o cadastro e o gerenciamento dos produtos disponíveis para venda.

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/produtos` | Cadastra novo produto |
| `GET` | `/produtos` | Lista todos os produtos |
| `GET` | `/produtos/<id>` | Mostra detalhes de um produto |
| `PUT` | `/produtos/<id>` | Atualiza dados do produto (ex: preço, estoque) |
| `DELETE` | `/produtos/<id>` | Remove produto do banco |

### Exemplo de corpo JSON (`POST /produtos`)
```json
{
  "nome": "Mouse Gamer RGB",
  "preco": 149.90,
  "estoque": 35
}
```

### Exemplo de resposta da rota (`GET /produtos/<id>`)
```json
{
  "id": 3,
  "nome": "Mouse Gamer RGB",
  "preco": 149.90,
  "estoque": 35,
  "created_at": "2023-11-20T14:30:00Z"
}
```

## 🧾 4. Rotas de Venda

Controlam o processo de venda realizado por um funcionário a um cliente.

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/vendas` | Cria uma nova venda (com cliente, funcionário e itens) |
| `GET` | `/vendas` | Lista todas as vendas registradas |
| `GET` | `/vendas/<id>` | Mostra detalhes de uma venda específica |
| `DELETE` | `/vendas/<id>` | Exclui uma venda e seus itens associados |

### Exemplo de corpo JSON (`POST /vendas`)
```json
{
  "id_cliente": 1,
  "id_funcionario": 2,
  "itens": [
    {"id_produto": 10, "quantidade": 2, "preco_unitario": 49.90},
    {"id_produto": 5, "quantidade": 1, "preco_unitario": 89.90}
  ]
}
```

### Exemplo de resposta da rota (`POST /vendas`)
```json
{
  "id": 1,
  "id_cliente": 1,
  "id_funcionario": 2,
  "itens": [
    {"id_produto": 10, "quantidade": 2, "preco_unitario": 49.90},
    {"id_produto": 5, "quantidade": 1, "preco_unitario": 89.90}
  ],
  "total": 189.70,
  "created_at": "2023-11-20T14:30:00Z"
}
```

Essa rota:
- Gera um novo registro na tabela Venda
- Cria automaticamente os registros na tabela Item_Venda
- Atualiza o estoque dos produtos envolvidos

## 📄 5. Rotas de Item_Venda

Permitem consultar os produtos vinculados a cada venda.

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/itens_venda` | Lista todos os itens de todas as vendas |
| `GET` | `/itens_venda/<id>` | Retorna detalhes de um item específico |
| `GET` | `/vendas/<id>/itens` | Lista todos os itens de uma venda específica |

### Exemplo de resposta da rota (`GET /itens_venda/<id>`)
```json
{
  "id": 1,
  "id_venda": 1,
  "id_produto": 10,
  "quantidade": 2,
  "preco_unitario": 49.90,
  "subtotal": 99.80,
  "created_at": "2023-11-20T14:30:00Z"
}
```

## 🔐 6. Rotas de Autenticação (opcional)

Rotas opcionais para controle de login de funcionários.

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/login` | Autentica funcionário (usuário e senha) |
| `POST` | `/logout` | Finaliza a sessão de autenticação |

### Exemplo de resposta da rota (`POST /login`)
```json
{
  "id": 2,
  "usuario": "maria",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "created_at": "2023-11-20T14:30:00Z"
}
```

### Exemplo de corpo JSON (`POST /login`)
```json
{
  "usuario": "maria",
  "senha": "1234"
}
```

## ⚙️ Fluxo de uso típico

1. Cadastrar clientes e produtos
2. Funcionário faz login
3. Cria uma nova venda (seleciona cliente e produtos)
4. A API registra a venda e os itens no banco
5. A interface PyQt consome as rotas e exibe os resultados (lista, busca e recibo)

