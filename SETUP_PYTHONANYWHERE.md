# 🚀 Setup da API AutoPeck no PythonAnywhere

Este guia completo explica como fazer o deploy da API Flask AutoPeck no PythonAnywhere, incluindo configuração do banco de dados MySQL, upload de arquivos e configurações de produção.

---

## 📋 Pré-requisitos

- Conta no PythonAnywhere (gratuita ou paga)
- Código da API AutoPeck no seu repositório GitHub
- Conhecimento básico de Python/Flask

---

## 1️⃣ Preparação no PythonAnywhere

### 1.1 Clonando o Repositório

Acesse o **Bash Console** no PythonAnywhere e execute:

```bash
# Navegar para o diretório home
cd ~

# Clonar o repositório
git clone https://github.com/joaovitorvlb/api_autopeck.git

# Entrar no diretório do projeto
cd api_autopeck

# Verificar estrutura
ls -la
```

### 1.2 Criar Ambiente Virtual

```bash
# Criar ambiente virtual
python3.10 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se está ativo (deve aparecer (venv) no prompt)
which python
```

### 1.3 Instalar Dependências

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

# Instalar dependência adicional para PythonAnywhere
pip install python-dotenv
```

---

## 2️⃣ Configuração do Banco de Dados MySQL

### 2.1 Configurar Banco no Dashboard

1. **Acesse o Dashboard** → **Databases** → **MySQL**
2. **Anote as informações**:
   - **Host**: `SEU_USUARIO.mysql.pythonanywhere-services.com`
   - **Usuário**: `SEU_USUARIO` (mesmo nome da conta)
   - **Banco**: `SEU_USUARIO$default`
   - **Porta**: `3306`

3. **Defina uma senha** para o MySQL (se ainda não tiver)

### 2.2 Executar Script de Criação do Banco

**Opção A - Console MySQL (Recomendado):**

1. Clique em **"Open MySQL console"** no dashboard
2. Cole e execute o script SQL:

```sql
-- Use o banco padrão
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

-- Dados iniciais para funcionários (para login)
INSERT INTO Funcionario (nome, cargo, salario, data_contratacao) VALUES
('Maria Silva', 'Vendedora', 2500.00, '2023-01-15'),
('Admin Sistema', 'Administrador', 4500.00, '2022-06-10'),
('Carlos Lima', 'Gerente', 3500.00, '2023-03-20');

-- Dados iniciais para clientes
INSERT INTO Cliente (nome, email, telefone, endereco) VALUES
('João Silva', 'joao@email.com', '11999999999', 'Rua A, 123'),
('Ana Santos', 'ana@email.com', '11888888888', 'Rua B, 456'),
('Pedro Oliveira', 'pedro@email.com', '11777777777', 'Rua C, 789');

-- Produtos de exemplo (AutoPeças)
INSERT INTO Produto (nome, descricao, preco, estoque, nome_imagem) VALUES
('Filtro de Óleo', 'Filtro de óleo para motores 1.0 a 2.0', 29.90, 100, 'filtro_oleo.jpg'),
('Pastilha de Freio', 'Jogo de pastilhas de freio dianteiro', 89.90, 50, 'pastilha_freio.jpg'),
('Amortecedor Dianteiro', 'Amortecedor dianteiro para carros populares', 189.90, 30, 'amortecedor.jpg'),
('Vela de Ignição', 'Jogo de velas de ignição NGK', 45.90, 80, 'vela_ignicao.jpg'),
('Correia Dentada', 'Correia dentada para motores 1.0/1.4/1.6', 65.90, 25, 'correia_dentada.jpg');
```

**Opção B - Script Python (Automático):**

```bash
# No Bash Console, execute:
cd ~/api_autopeck
python scripts/setup_mysql_pythonanywhere.py
```

---

## 3️⃣ Configuração da Aplicação Web

### 3.1 Configurar Aplicação Web no Dashboard

1. **Dashboard** → **Web** → **Add a new web app**
2. **Selecione**: **Manual configuration**
3. **Python version**: **Python 3.10**
4. **Next** até finalizar

### 3.2 Configurar o arquivo WSGI

1. No dashboard **Web**, clique no link do arquivo **WSGI**
2. **Substitua todo o conteúdo** por:

```python
import os
import sys

# Configurações de variáveis de ambiente para MySQL
os.environ['MYSQL_HOST'] = 'SEU_USUARIO.mysql.pythonanywhere-services.com'
os.environ['MYSQL_PORT'] = '3306'
os.environ['MYSQL_USER'] = 'SEU_USUARIO'
os.environ['MYSQL_PASSWORD'] = 'SUA_SENHA_MYSQL'  # ⚠️ SUBSTITUA pela sua senha
os.environ['MYSQL_DATABASE'] = 'SEU_USUARIO$default'

# Configurações JWT
os.environ['JWT_SECRET'] = 'minha-chave-secreta-super-segura-2023'
os.environ['JWT_EXPIRES_MINUTES'] = '60'

# Configurações de email (se usar recuperação de senha)
os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USER'] = 'seu-email@gmail.com'  # ⚠️ SUBSTITUA
os.environ['EMAIL_PASSWORD'] = 'sua-app-password'  # ⚠️ SUBSTITUA

# Adicionar o projeto ao Python path
project_home = '/home/SEU_USUARIO/api_autopeck'  # ⚠️ SUBSTITUA SEU_USUARIO
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Ativar ambiente virtual (método manual - mais compatível)
venv_path = '/home/SEU_USUARIO/api_autopeck/venv'  # ⚠️ SUBSTITUA
site_packages = os.path.join(venv_path, 'lib', 'python3.10', 'site-packages')

# Adicionar site-packages do venv ao Python path
if site_packages not in sys.path:
    sys.path.insert(0, site_packages)

# Definir variável de ambiente VIRTUAL_ENV
os.environ['VIRTUAL_ENV'] = venv_path

# Importar a aplicação Flask
from app import app as application

# Configurações específicas para produção
if hasattr(application, 'config'):
    application.config['DEBUG'] = False
    application.config['TESTING'] = False
```

### 3.3 Configurar Diretórios

No dashboard **Web**:

1. **Source code**: `/home/SEU_USUARIO/api_autopeck`
2. **Working directory**: `/home/SEU_USUARIO/api_autopeck`
3. **Static files**:
   - **URL**: `/static/`
   - **Directory**: `/home/SEU_USUARIO/api_autopeck/static/`

---

## 4️⃣ Criar Arquivo de Configuração para MySQL

Crie o arquivo `config_pythonanywhere.py` no diretório raiz:

```bash
cd ~/api_autopeck
nano config_pythonanywhere.py
```

**Conteúdo do arquivo:**

```python
import os

def get_mysql_config_pythonanywhere():
    """Configuração MySQL específica para PythonAnywhere"""
    return {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'database': os.getenv('MYSQL_DATABASE', 'default'),
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci',
        'autocommit': False,
        'ssl_disabled': True,  # PythonAnywhere não precisa SSL
        'connection_timeout': 60,
        'pool_reset_session': True
    }

def is_pythonanywhere():
    """Detecta se está rodando no PythonAnywhere"""
    return 'pythonanywhere.com' in os.getenv('SERVER_NAME', '')

# Configurações de email para produção
EMAIL_CONFIG = {
    'smtp_server': os.getenv('EMAIL_HOST', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('EMAIL_PORT', 587)),
    'email_user': os.getenv('EMAIL_USER'),
    'email_password': os.getenv('EMAIL_PASSWORD'),
    'use_tls': True
}
```

---

## 5️⃣ Adaptar a Aplicação para Produção

### 5.1 Modificar app.py para Usar MySQL

Adicione no início do `app.py` (após os imports):

```python
# Detectar ambiente e configurar banco apropriado
if 'pythonanywhere.com' in os.getenv('SERVER_NAME', '') or os.getenv('MYSQL_HOST'):
    # Usar MySQL no PythonAnywhere
    from dao_mysql.db_pythonanywhere import init_db
    from dao_mysql.funcionario_dao import FuncionarioDAO
    from dao_mysql.produto_dao import ProdutoDAO
    from dao_mysql.venda_dao import VendaDAO
    from dao_mysql.item_venda_dao import ItemVendaDAO
    from dao_mysql.cliente_dao import ClienteDAO
else:
    # Usar SQLite no desenvolvimento local
    from dao_sqlite.db import init_db
    from dao_sqlite.funcionario_dao import FuncionarioDAO
    from dao_sqlite.produto_dao import ProdutoDAO
    from dao_sqlite.venda_dao import VendaDAO
    from dao_sqlite.item_venda_dao import ItemVendaDAO
    from dao_sqlite.cliente_dao import ClienteDAO
```

### 5.2 Criar Diretórios Necessários

```bash
cd ~/api_autopeck

# Criar diretório para uploads
mkdir -p static/images/produtos

# Definir permissões corretas (importante!)
chmod 755 static
chmod 755 static/images
chmod 755 static/images/produtos

# Verificar permissões
ls -la static/
ls -la static/images/
ls -la static/images/produtos/

# Criar arquivo README para o diretório
echo "# Diretório para imagens de produtos" > static/images/produtos/README.md
```

### 5.3 ⚠️ Importante: Caminhos Absolutos no PythonAnywhere

**O código já está configurado para usar caminhos absolutos automaticamente:**

```python
# Em app.py (já implementado)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'images', 'produtos')

# Criar diretório automaticamente se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
```

**Por que isso é necessário?**
- PythonAnywhere executa a aplicação em um diretório diferente do código
- Caminhos relativos como `'static/images/produtos'` não funcionam
- Caminhos absolutos garantem que o diretório seja encontrado sempre

**Verificar se está funcionando:**
```bash
# No console Python
cd ~/api_autopeck
python -c "
import os
from app import app
print('UPLOAD_FOLDER:', app.config['UPLOAD_FOLDER'])
print('Existe?', os.path.exists(app.config['UPLOAD_FOLDER']))
print('Pode escrever?', os.access(app.config['UPLOAD_FOLDER'], os.W_OK))
"
```

---

## 6️⃣ Configurações de Segurança

### 6.1 Arquivo .env (Opcional)

Crie um arquivo `.env` para desenvolvimento local:

```bash
nano .env
```

**Conteúdo:**

```env
# Configurações MySQL PythonAnywhere
MYSQL_HOST=SEU_USUARIO.mysql.pythonanywhere-services.com
MYSQL_PORT=3306
MYSQL_USER=SEU_USUARIO
MYSQL_PASSWORD=SUA_SENHA_MYSQL
MYSQL_DATABASE=SEU_USUARIO$default

# Configurações JWT
JWT_SECRET=minha-chave-secreta-super-segura-2023
JWT_EXPIRES_MINUTES=60

# Configurações Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seu-email@gmail.com
EMAIL_PASSWORD=sua-app-password
```

### 6.2 Ignorar arquivos sensíveis

```bash
# Adicionar ao .gitignore
echo ".env" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "banco_api.sqlite*" >> .gitignore
```

---

## 7️⃣ Testar a Aplicação

### 7.1 Teste via Console

```bash
cd ~/api_autopeck
source venv/bin/activate

# Testar conexão com MySQL
python -c "
from dao_mysql.db_pythonanywhere import init_db, get_cursor, test_connection
init_db()
if test_connection():
    print('✅ Conexão MySQL OK!')
else:
    print('❌ Erro na conexão MySQL')
"

# Testar importação da aplicação
python -c "
from app import app
print('✅ Aplicação importada com sucesso!')
print(f'DEBUG: {app.config.get(\"DEBUG\", False)}')
"
```

### 7.2 Reload da Aplicação Web

1. **Dashboard** → **Web** → **Reload** (botão verde)
2. Aguardar alguns segundos
3. Acessar: `https://SEU_USUARIO.pythonanywhere.com`

### 7.3 Testar Endpoints Principais

**Teste de saúde:**
```bash
curl https://SEU_USUARIO.pythonanywhere.com/
```

**Teste de login:**
```bash
curl -X POST https://SEU_USUARIO.pythonanywhere.com/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"maria","senha":"1234"}'
```

**Teste de produtos (com token):**
```bash
# Substitua TOKEN_JWT pelo token obtido no login
curl -X GET https://SEU_USUARIO.pythonanywhere.com/produtos \
  -H "Authorization: Bearer TOKEN_JWT"
```

---

## 8️⃣ Configuração de Upload de Imagens

### 8.1 Configurar Nginx (se necessário)

Para uploads maiores, configure no arquivo de configuração:

```python
# Em app.py, ajustar limite de upload
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### 8.2 Testar Upload

```bash
# Teste de upload de imagem (substitua TOKEN_JWT)
curl -X POST https://SEU_USUARIO.pythonanywhere.com/produtos \
  -H "Authorization: Bearer TOKEN_JWT" \
  -F "nome=Teste Produto" \
  -F "descricao=Produto de teste" \
  -F "preco=99.90" \
  -F "estoque=10" \
  -F "imagem=@caminho/para/imagem.jpg"
```

---

## 9️⃣ Monitoramento e Logs

### 9.1 Verificar Logs de Erro

**Dashboard** → **Web** → **Log files**:
- **Error log**: Erros da aplicação
- **Access log**: Requests HTTP
- **Server log**: Logs do servidor

### 9.2 Log Personalizado

Adicione logging ao `app.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    # Configurar logging para produção
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('API AutoPeck startup')
```

---

## 🔟 Documentação Swagger

A documentação da API estará disponível em:
- **URL**: `https://SEU_USUARIO.pythonanywhere.com/apidocs/`
- **Swagger JSON**: `https://SEU_USUARIO.pythonanywhere.com/apispec_1.json`

---

## 1️⃣1️⃣ Backup e Manutenção

### 11.1 Backup do Banco

```bash
# Fazer backup do banco MySQL
mysqldump -u SEU_USUARIO -p'SUA_SENHA' \
  -h SEU_USUARIO.mysql.pythonanywhere-services.com \
  SEU_USUARIO$default > backup_$(date +%Y%m%d).sql
```

### 11.2 Atualizar Código

```bash
cd ~/api_autopeck
git pull origin main
pip install -r requirements.txt --upgrade

# Reload da aplicação
# Dashboard → Web → Reload
```

### 11.3 Limpar Dados de Teste

**🧹 Após testar a aplicação, você pode limpar os dados de teste:**

```bash
# Método automático (recomendado)
cd ~/api_autopeck
source venv/bin/activate
python scripts/limpar_producao.py
```

**📚 Para instruções detalhadas, consulte:**
- [`docs/GUIA_LIMPEZA_PRODUCAO.md`](docs/GUIA_LIMPEZA_PRODUCAO.md) - Guia completo de limpeza

Este guia inclui:
- Script automatizado de limpeza
- Limpeza manual passo a passo
- Como fazer backup antes de limpar
- Como restaurar se necessário
- Limpeza seletiva (apenas imagens ou apenas banco)

---

## 🚨 Solução de Problemas Comuns

### Erro: "No module named 'dao_mysql'"
```bash
cd ~/api_autopeck
source venv/bin/activate
pip install mysql-connector-python
```

### Erro: "Access denied for user"
- Verificar senha MySQL no arquivo WSGI
- Testar conexão no console MySQL

### Erro: "Static files not found"
- Verificar configuração de diretórios no dashboard Web
- Conferir permissões: `chmod 755 static/`

### Aplicação não carrega
1. Verificar logs de erro
2. Testar importação no console: `python -c "from app import app"`
3. Verificar arquivo WSGI

### Erro: "No such file or directory" no upload de imagens
**Causa**: Caminho relativo não funciona no PythonAnywhere

**Solução**: O código já usa caminho absoluto. Se o erro persistir:
```bash
# Criar diretório manualmente
cd ~/api_autopeck
mkdir -p static/images/produtos
chmod 755 static/images/produtos

# Verificar se o diretório existe
ls -la static/images/produtos/
```

**Importante**: O `app.py` já está configurado para usar caminhos absolutos:
```python
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'images', 'produtos')
```

### Erro: "module 'PIL.Image' has no attribute 'Resampling'"
**Causa**: Versão antiga do Pillow no PythonAnywhere

**Solução**: O código já tem compatibilidade com versões antigas e novas. Se persistir:
```bash
cd ~/api_autopeck
source venv/bin/activate
pip install --upgrade Pillow
```

**Nota**: O código usa detecção automática:
```python
# Compatibilidade com Pillow < 9.1.0 e >= 9.1.0
try:
    RESAMPLE_FILTER = Image.Resampling.LANCZOS  # Versão nova
except AttributeError:
    RESAMPLE_FILTER = Image.LANCZOS  # Versão antiga
```

### Upload de imagens não funciona
- Verificar permissões: `chmod 755 static/images/produtos/`
- Conferir tamanho máximo: `MAX_CONTENT_LENGTH`
- Verificar se o diretório existe: `ls -la static/images/produtos/`
- Testar criação manual de arquivo: `touch static/images/produtos/test.txt`

---

## ✅ Checklist Final

- [ ] **Código clonado** no PythonAnywhere
- [ ] **Ambiente virtual** criado e ativado
- [ ] **Dependências instaladas** (`pip install -r requirements.txt`)
- [ ] **Banco MySQL** configurado e populado
- [ ] **Arquivo WSGI** configurado com variáveis corretas
- [ ] **Diretórios** configurados no dashboard Web
- [ ] **Aplicação reloadada** e funcionando
- [ ] **Endpoints testados** (login, produtos, etc.)
- [ ] **Upload de imagens** funcionando
- [ ] **Documentação Swagger** acessível
- [ ] **Logs** configurados e monitorados

---

## 🎉 Parabéns!

Sua API AutoPeck está agora rodando em produção no PythonAnywhere! 

**URL da API**: `https://SEU_USUARIO.pythonanywhere.com`
**Documentação**: `https://SEU_USUARIO.pythonanywhere.com/apidocs/`

### Próximos Passos:
1. **Personalizar domínio** (conta paga)
2. **Configurar HTTPS** personalizado
3. **Implementar cache** (Redis)
4. **Monitoramento avançado**
5. **CI/CD** com GitHub Actions

---

**⚠️ Lembrete Important⚠️ **: 
- Substitua **todos** os `SEU_USUARIO` pelo seu nome de usuário real
- Defina senhas seguras para MySQL e JWT
- Configure email real para recuperação de senha
- Mantenha backups regulares do banco de dados

**Boa sorte com sua API! 🚀**