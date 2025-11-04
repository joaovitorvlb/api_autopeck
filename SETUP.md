# 🚀 Setup e Testes da API Flask

Este guia explica como configurar o ambiente virtual, instalar dependências e testar a rota de produtos com autenticação JWT.

---

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

---

## 1️⃣ Criar e Ativar o Ambiente Virtual (venv)

### Linux / macOS:
```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate
```

### Windows (CMD):
```cmd
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
venv\Scripts\activate.bat
```

### Windows (PowerShell):
```powershell
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
venv\Scripts\Activate.ps1
```

**Nota:** Quando o ambiente virtual estiver ativo, você verá `(venv)` no início do prompt do terminal.

---

## 2️⃣ Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

As principais dependências instaladas são:
- `Flask` - Framework web
- `flasgger` - Documentação Swagger/OpenAPI
- `psycopg2-binary` - Driver PostgreSQL
- `PyJWT` - Autenticação JWT

---

## 3️⃣ Configurar Variáveis de Ambiente (Opcional)

Para PostgreSQL, configure as variáveis de ambiente:

### Linux / macOS:
```bash
export PGHOST=localhost
export PGPORT=5432
export PGUSER=postgres
export PGPASSWORD=sua_senha
export PGDATABASE=e_comerce_flask
export JWT_SECRET=minha-chave-secreta
```

### Windows (PowerShell):
```powershell
$env:PGHOST="localhost"
$env:PGPORT="5432"
$env:PGUSER="postgres"
$env:PGPASSWORD="sua_senha"
$env:PGDATABASE="e_comerce_flask"
$env:JWT_SECRET="minha-chave-secreta"
```

**Para SQLite:** Não é necessário configurar variáveis de ambiente do PostgreSQL.

---

## 4️⃣ Inserir Dados de Teste (SQLite)

Execute o script para popular o banco SQLite com dados de teste:

```bash
python scripts/test_sqlite_insert.py
```

Este script irá:
- Criar o banco `banco_api.sqlite`
- Inserir funcionários, clientes e produtos
- Testar os SELECTs

---

## 5️⃣ Iniciar o Servidor Flask

```bash
python app.py
```

O servidor será iniciado em: `http://127.0.0.1:5000`

---

## 6️⃣ Testar a Rota de Produtos com JWT

### Passo 1: Fazer Login e Obter o Token

```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"maria","senha":"1234"}'
```

**Resposta esperada:**
```json
{
  "usuario": "maria",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Copie o token** retornado para usar no próximo passo.

---

### Passo 2: Acessar a Rota de Produtos (Protegida)

Substitua `<SEU_TOKEN_AQUI>` pelo token obtido no passo anterior:

```bash
curl -X GET http://127.0.0.1:5000/produtos \
  -H "Authorization: Bearer <SEU_TOKEN_AQUI>"
```

**Exemplo completo:**
```bash
curl -X GET http://127.0.0.1:5000/produtos \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXN1YXJpbyI6Im1hcmlhIn0sImlhdCI6MTY5ODQyMzQwMCwiZXhwIjoxNjk4NDI3MDAwfQ.xKzJ..."
```

**Resposta esperada (lista de produtos):**
```json
[
  {
    "id_produto": 1,
    "nome": "Filtro de Óleo",
    "descricao": "Filtro de óleo para motores 1.0 a 2.0",
    "preco": 29.90,
    "estoque": 100
  },
  {
    "id_produto": 2,
    "nome": "Pastilha de Freio",
    "descricao": "Jogo de pastilhas de freio dianteiro",
    "preco": 89.90,
    "estoque": 50
  },
  ...
]
```

---

### Passo 3: Testar Acesso Sem Token (Deve Falhar)

```bash
curl -X GET http://127.0.0.1:5000/produtos
```

**Resposta esperada (erro 401):**
```json
{
  "erro": "Token ausente ou inválido"
}
```

---

## 7️⃣ Teste com Ferramenta Visual (Opcional)

### Usando Postman ou Insomnia:

1. **Login (POST):**
   - URL: `http://127.0.0.1:5000/login`
   - Método: `POST`
   - Headers: `Content-Type: application/json`
   - Body (JSON):
     ```json
     {
       "usuario": "maria",
       "senha": "1234"
     }
     ```
   - Copie o `token` da resposta

2. **Listar Produtos (GET):**
   - URL: `http://127.0.0.1:5000/produtos`
   - Método: `GET`
   - Headers:
     - `Authorization: Bearer <seu_token_aqui>`

---

## 8️⃣ Usuários Padrão de Teste

Os seguintes usuários estão disponíveis por padrão para login:

| Usuário | Senha  |
|---------|--------|
| maria   | 1234   |
| admin   | admin  |

---

## 🛠️ Comandos Úteis

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Popular banco SQLite com dados de teste
python scripts/test_sqlite_insert.py

# Iniciar servidor Flask
python app.py

# Desativar ambiente virtual
deactivate
```

---

## 📝 Notas Importantes

- **Token JWT:** Por padrão, o token expira em 60 minutos. Configure via variável `JWT_EXPIRES_MINUTES`.
- **Banco SQLite:** O arquivo do banco é criado automaticamente em `banco_api.sqlite`.
- **Banco PostgreSQL:** Configure as variáveis de ambiente antes de usar o PostgreSQL.
- **Segurança:** Em produção, use senhas fortes e hash (bcrypt) em vez de senhas em texto plano.

---

## 🐛 Solução de Problemas

### Erro: "Token ausente ou inválido"
- Verifique se o header `Authorization: Bearer <token>` está correto
- Certifique-se de que o token não expirou (padrão: 60 minutos)
- Faça login novamente para obter um novo token

### Erro: "Connection pool não inicializado"
- Execute `python scripts/test_sqlite_insert.py` primeiro para criar o banco
- Ou configure as variáveis de ambiente do PostgreSQL

### Erro: "Module not found"
- Certifique-se de que o ambiente virtual está ativado
- Execute `pip install -r requirements.txt` novamente

---

## ✅ Checklist de Configuração

- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Banco SQLite populado (`python scripts/test_sqlite_insert.py`)
- [ ] Servidor Flask iniciado (`python app.py`)
- [ ] Login realizado e token obtido
- [ ] Rota `/produtos` testada com token JWT

---

**Pronto! 🎉** Agora você pode testar todas as rotas da API com autenticação JWT.
