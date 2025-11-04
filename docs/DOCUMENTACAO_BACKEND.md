# 🛒 Documentação Completa do Backend Flask - Sistema E-commerce

## 📋 Sumário
1. [Visão Geral](#-visão-geral)
2. [Arquitetura do Sistema](#-arquitetura-do-sistema)
3. [Tecnologias Utilizadas](#-tecnologias-utilizadas)
4. [Estrutura de Pastas](#-estrutura-de-pastas)
5. [Modelos de Dados](#-modelos-de-dados)
6. [API Endpoints](#-api-endpoints)
7. [Sistema de Autenticação](#-sistema-de-autenticação)
8. [Gestão de Imagens](#-gestão-de-imagens)
9. [Como Executar](#-como-executar)
10. [Exemplos de Uso](#-exemplos-de-uso)

---

## 🎯 Visão Geral

Este é um sistema backend completo para e-commerce desenvolvido em **Python Flask**, que oferece:

- **API RESTful** para gestão de produtos, clientes, funcionários e vendas
- **Sistema de autenticação JWT** para segurança
- **Upload e processamento de imagens** com múltiplas resoluções
- **Arquitetura DAO (Data Access Object)** para abstração do banco de dados
- **Documentação Swagger** automática das APIs
- **Suporte a SQLite e PostgreSQL**

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cliente       │    │   Frontend      │    │   Backend       │
│   (PyQt/Web)    │◄──►│   (Opcional)    │◄──►│   Flask API     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │   Camada DAO    │
                                              │   (Abstração)   │
                                              └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │   Banco de      │
                                              │   Dados         │
                                              │ (SQLite/Postgres)│
                                              └─────────────────┘
```

### Princípios da Arquitetura:
- **Separação de Responsabilidades**: Models, DAOs e Controllers
- **API First**: Backend independente do frontend
- **Configuração Flexível**: Suporte a múltiplos bancos de dados
- **Escalabilidade**: Estrutura preparada para crescimento

---

## 🛠️ Tecnologias Utilizadas

### Core Framework
- **Flask 2.2.5**: Framework web minimalista e flexível
- **Werkzeug 2.2.3**: Utilitários WSGI para Flask

### Autenticação e Segurança
- **Flask-JWT-Extended 4.4.4**: Implementação JWT para autenticação
- **Werkzeug Security**: Para hash de senhas e validações

### Banco de Dados
- **psycopg2-binary**: Adapter PostgreSQL para Python
- **SQLite3**: Banco embarcado (built-in no Python)

### Documentação e Testes
- **Flasgger 0.9.5**: Geração automática de documentação Swagger
- **Requests 2.28.0**: Para testes e comunicação HTTP

### Processamento de Imagens
- **Pillow (PIL)**: Manipulação e redimensionamento de imagens
- **UUID**: Geração de nomes únicos para arquivos

---

## 📁 Estrutura de Pastas

```
app_flask/
│
├── 📄 app.py                    # Arquivo principal da aplicação
├── 📄 requirements.txt          # Dependências do projeto
├── 📄 readme.md                 # Documentação básica
├── 📄 SETUP.md                  # Instruções de configuração
├── 📄 test_api.py              # Testes da API
│
├── 📂 models/                   # Modelos de dados (Classes)
│   ├── __init__.py
│   ├── cliente.py              # Modelo Cliente
│   ├── funcionario.py          # Modelo Funcionário
│   ├── produto.py              # Modelo Produto
│   ├── venda.py                # Modelo Venda
│   └── item_venda.py           # Modelo Item de Venda
│
├── 📂 dao_sqlite/              # Data Access Objects (SQLite)
│   ├── __init__.py
│   ├── db.py                   # Configuração e conexão
│   ├── cliente_dao.py          # DAO para clientes
│   ├── funcionario_dao.py      # DAO para funcionários
│   ├── produto_dao.py          # DAO para produtos
│   ├── venda_dao.py            # DAO para vendas
│   └── item_venda_dao.py       # DAO para itens de venda
│
├── 📂 dao_postgres/            # Data Access Objects (PostgreSQL)
│   └── [mesma estrutura SQLite]
│
├── 📂 static/                  # Arquivos estáticos
│   └── images/
│       └── produtos/           # Imagens de produtos
│           ├── thumbs/         # Miniaturas (150x150)
│           ├── medium/         # Médias (400x400)
│           └── full/           # Grandes (800x800)
│
├── 📂 swagger_docs/            # Documentação Swagger
│   └── clientes.yml            # Spec do endpoint clientes
│
├── 📂 scripts/                 # Scripts de teste e debug
│   ├── test_*.py              # Vários testes específicos
│   └── debug_*.py             # Scripts de debug
│
└── 📂 docs/                    # Documentação adicional
    ├── banco_1.sql            # Scripts SQL
    └── *.md                   # Documentos diversos
```

---

## 🗃️ Modelos de Dados

### 👤 Cliente
```python
{
    "id_cliente": int,          # Identificador único
    "nome": str,                # Nome completo
    "email": str,               # Email (único)
    "telefone": str,            # Telefone de contato
    "endereco": str,            # Endereço (opcional)
    "created_at": datetime      # Data de criação
}
```

### 👨‍💼 Funcionário
```python
{
    "id_funcionario": int,      # Identificador único
    "nome": str,                # Nome completo
    "cargo": str,               # Cargo/função
    "salario": float,           # Salário (opcional)
    "data_contratacao": date,   # Data de contratação
    "created_at": datetime      # Data de criação
}
```

### 📦 Produto
```python
{
    "id_produto": int,          # Identificador único (auto-increment)
    "nome": str,                # Nome do produto
    "descricao": str,           # Descrição detalhada
    "preco": float,             # Preço unitário
    "estoque": int,             # Quantidade em estoque
    "nome_imagem": str,         # JSON com URLs das imagens
    "created_at": datetime      # Data de criação
}
```

### 🧾 Venda
```python
{
    "id_venda": int,            # Identificador único
    "id_cliente": int,          # FK para Cliente
    "id_funcionario": int,      # FK para Funcionário
    "data_venda": date,         # Data da venda
    "total": float,             # Valor total da venda
    "created_at": datetime      # Data de criação
}
```

### 📋 Item de Venda
```python
{
    "id_item": int,             # Identificador único
    "id_venda": int,            # FK para Venda
    "id_produto": int,          # FK para Produto
    "quantidade": int,          # Quantidade vendida
    "preco_unitario": float,    # Preço no momento da venda
    "subtotal": float           # quantidade * preco_unitario
}
```

---

## 🌐 API Endpoints

### 🧑‍🤝‍🧑 Clientes
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `POST` | `/clientes` | Criar novo cliente | ❌ |
| `GET` | `/clientes` | Listar todos os clientes | ❌ |
| `GET` | `/clientes/{id}` | Obter cliente específico | ❌ |
| `PUT` | `/clientes/{id}` | Atualizar cliente | ❌ |
| `DELETE` | `/clientes/{id}` | Excluir cliente | ❌ |

### 👨‍💼 Funcionários
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `POST` | `/funcionarios` | Criar novo funcionário | ❌ |
| `GET` | `/funcionarios` | Listar funcionários | ❌ |
| `GET` | `/funcionarios/{id}` | Obter funcionário específico | ❌ |
| `PUT` | `/funcionarios/{id}` | Atualizar funcionário | ❌ |
| `DELETE` | `/funcionarios/{id}` | Excluir funcionário | ❌ |

### 📦 Produtos
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `POST` | `/produtos` | Criar novo produto | ❌ |
| `GET` | `/produtos` | Listar produtos | ✅ |
| `GET` | `/produtos/{id}` | Obter produto específico | ❌ |
| `PUT` | `/produtos/{id}` | Atualizar produto | ❌ |
| `DELETE` | `/produtos/{id}` | Excluir produto | ❌ |

### 🖼️ Gestão de Imagens
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `POST` | `/produtos/{id}/upload-image` | Upload de imagem | ❌ |
| `DELETE` | `/produtos/{id}/remove-image` | Remover imagem | ❌ |
| `GET` | `/images/produtos/{filename}` | Servir imagem | ❌ |

### 🧾 Vendas
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `POST` | `/vendas` | Criar nova venda | ❌ |
| `GET` | `/vendas` | Listar vendas | ❌ |
| `GET` | `/vendas/{id}` | Obter venda específica | ❌ |
| `DELETE` | `/vendas/{id}` | Excluir venda | ❌ |

### 📋 Itens de Venda
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `GET` | `/itens_venda` | Listar todos os itens | ❌ |
| `GET` | `/itens_venda/{id}` | Obter item específico | ❌ |
| `GET` | `/vendas/{id}/itens` | Itens de uma venda | ❌ |

### 🔐 Autenticação
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `POST` | `/login` | Fazer login | ❌ |
| `POST` | `/logout` | Fazer logout | ❌ |

### 🧪 Utilitários
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `GET` | `/test` | Verificar se API está funcionando | ❌ |
| `GET` | `/test-db` | Testar conexão com banco | ✅ |

---

## 🔐 Sistema de Autenticação

### Configuração JWT
```python
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config["JWT_ISSUER"] = "Flask_PyJWT"
app.config["JWT_AUTHTYPE"] = "HS256"
app.config["JWT_AUTHMAXAGE"] = 3600        # 1 hora
app.config["JWT_REFRESHMAXAGE"] = 604800   # 7 dias
```

### Como Usar
1. **Login**: `POST /login` com `{"usuario": "...", "senha": "..."}`
2. **Receber Token**: Resposta contém `{"token": "eyJ..."}`
3. **Usar Token**: Header `Authorization: Bearer eyJ...`

### Usuários Padrão
```json
{
    "joaovitorvlb@hotmail.com": "1234",
    "admin": "admin"
}
```

---

## 🖼️ Gestão de Imagens

### Formatos Suportados
- PNG, JPG, JPEG, GIF, WEBP

### Tamanho Máximo
- 16MB por arquivo

### Resoluções Automáticas
```python
IMAGE_RESOLUTIONS = {
    'thumbnail': (150, 150),   # Para listas/miniaturas
    'medium': (400, 400),      # Para detalhes/cards  
    'large': (800, 800)        # Para visualização ampliada
}
```

### Estrutura de Armazenamento
```
static/images/produtos/
├── produto_1_abc123_thumbnail.jpg
├── produto_1_abc123_medium.jpg
└── produto_1_abc123_large.jpg
```

### URLs Geradas
```json
{
    "thumbnail": "http://localhost:5001/images/produtos/produto_1_abc123_thumbnail.jpg",
    "medium": "http://localhost:5001/images/produtos/produto_1_abc123_medium.jpg", 
    "large": "http://localhost:5001/images/produtos/produto_1_abc123_large.jpg"
}
```

---

## 🚀 Como Executar

### 1. Pré-requisitos
```bash
# Python 3.8+
python --version

# Git (para clonar)
git --version
```

### 2. Instalação
```bash
# Clonar projeto
git clone <repository-url>
cd app_flask

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configuração do Banco
```bash
# Para SQLite (padrão - nenhuma configuração necessária)
# O banco será criado automaticamente

# Para PostgreSQL (opcional)
export DB_HOST=localhost
export DB_NAME=ecommerce
export DB_USER=postgres
export DB_PASSWORD=sua_senha
export DB_PORT=5432
```

### 4. Executar Servidor
```bash
# Desenvolvimento
python app.py

# Produção (com gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### 5. Testar API
```bash
# Teste básico
curl http://localhost:5001/test

# Com autenticação
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"admin","senha":"admin"}'
```

---

## 🧪 Exemplos de Uso

### 1. Criar Produto
```bash
curl -X POST http://localhost:5001/produtos \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Mouse Gamer",
    "descricao": "Mouse RGB para gamers",
    "preco": 149.90,
    "estoque": 50
  }'
```

### 2. Upload de Imagem
```bash
curl -X POST http://localhost:5001/produtos/1/upload-image \
  -F "image=@/path/to/image.jpg"
```

### 3. Criar Venda Completa
```bash
curl -X POST http://localhost:5001/vendas \
  -H "Content-Type: application/json" \
  -d '{
    "id_venda": 1,
    "id_cliente": 1,
    "id_funcionario": 1,
    "itens": [
      {
        "id_item": 1,
        "id_produto": 1,
        "quantidade": 2,
        "preco_unitario": 149.90
      }
    ]
  }'
```

### 4. Listar Produtos (com JWT)
```bash
# 1. Fazer login
TOKEN=$(curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"admin","senha":"admin"}' \
  | jq -r '.token')

# 2. Usar token
curl -X GET http://localhost:5001/produtos \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔧 Configurações Avançadas

### Variáveis de Ambiente
```bash
# Banco de dados
export DB_TYPE=sqlite           # ou postgresql
export DB_HOST=localhost
export DB_NAME=ecommerce
export DB_USER=usuario
export DB_PASSWORD=senha
export DB_PORT=5432

# Autenticação
export JWT_SECRET_KEY=sua-chave-secreta
export AUTH_USERS='{"admin":"senha123"}'

# Upload
export MAX_CONTENT_LENGTH=16777216  # 16MB
export UPLOAD_FOLDER=/path/to/uploads
```

### Customização de Resoluções
```python
# Em app.py
IMAGE_RESOLUTIONS = {
    'icon': (32, 32),
    'thumbnail': (150, 150),
    'small': (300, 300),
    'medium': (600, 600),
    'large': (1200, 1200),
    'xl': (1920, 1920)
}
```

---

## 📊 Monitoramento e Logs

### Debug Mode
```python
# Em desenvolvimento
app.run(debug=True)

# Logs detalhados aparecem no console
```

### Logs de Debug
```python
# O sistema já possui logs de debug extensivos
print("🚀 [DEBUG] Rota POST /produtos iniciada")
print(f"📦 [DEBUG] Dados JSON recebidos: {dados}")
```

### Health Checks
- `GET /test` - Verificar se API responde
- `GET /test-db` - Verificar conexão com banco

---

## 🛡️ Segurança

### Medidas Implementadas
- **JWT Tokens** para autenticação
- **Validação de tipos de arquivo** para uploads
- **Sanitização de nomes de arquivo** com `secure_filename()`
- **Limite de tamanho** para uploads (16MB)
- **Validação de entrada** em todos os endpoints

### Medidas Recomendadas para Produção
- Usar HTTPS
- Configurar CORS adequadamente
- Implementar rate limiting
- Usar variáveis de ambiente para credenciais
- Hash de senhas com bcrypt
- Validação mais rigorosa de entrada

---

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro de conexão com banco**
   ```
   Solution: Verificar se SQLite DB foi criado ou PostgreSQL está rodando
   ```

2. **Token JWT inválido**
   ```
   Solution: Verificar se token está sendo enviado no header correto
   ```

3. **Upload de imagem falha**
   ```
   Solution: Verificar permissões da pasta static/images/produtos/
   ```

4. **CORS errors**
   ```
   Solution: Instalar flask-cors e configurar
   ```

---

## 🚀 Próximos Passos

### Melhorias Planejadas
- [ ] Implementar paginação na listagem
- [ ] Adicionar filtros e busca
- [ ] Sistema de categorias para produtos
- [ ] Relatórios de vendas
- [ ] Cache com Redis
- [ ] Testes automatizados completos
- [ ] Docker containerization
- [ ] CI/CD pipeline

### Expansões Possíveis
- [ ] Sistema de cupons/desconto
- [ ] Gestão de fornecedores
- [ ] Histórico de preços
- [ ] Notificações push
- [ ] API de pagamentos
- [ ] Dashboard administrativo

---

## 👥 Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 📞 Contato

- **Desenvolvedor**: João Vitor
- **Email**: joaovitorvlb@hotmail.com
- **GitHub**: [seu-github]

---

*Documentação gerada em: November 2, 2025*