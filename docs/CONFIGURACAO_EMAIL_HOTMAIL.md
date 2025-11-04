# 📧 Configuração de Email para Hotmail/Outlook

## ⚙️ Configurações Necessárias

### 1. **Preparar sua conta Hotmail/Outlook**

Para enviar emails pelo sistema, você precisa:

#### a) **Habilitar "Senha de App" (Recomendado)**
1. Acesse: https://account.microsoft.com/security
2. Vá em "Opções de segurança avançadas"
3. Clique em "Criar uma nova senha de app"
4. Escolha um nome (ex: "Sistema Flask")
5. **Copie a senha gerada** (use esta no lugar da sua senha normal)

#### b) **Ou habilitar "Aplicativos menos seguros"**
1. Acesse: https://account.microsoft.com/security
2. Vá em "Opções de segurança avançadas"
3. Desative "Autenticação de dois fatores" temporariamente
4. ⚠️ **Menos seguro, não recomendado para produção**

### 2. **Configurar Variáveis de Ambiente (Recomendado)**

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
EMAIL_USER=seu_email@hotmail.com
EMAIL_PASSWORD=sua_senha_de_app_gerada
```

**Instale python-dotenv:**
```bash
pip install python-dotenv
```

**Adicione no app.py:**
```python
from dotenv import load_dotenv
load_dotenv()  # Carrega variáveis do .env
```

### 3. **Configuração Direta (Para Testes Rápidos)**

No `app.py`, na função `send_recovery_email()`, substitua:

```python
sender_email = os.getenv('EMAIL_USER', 'SEU_EMAIL@hotmail.com')
sender_password = os.getenv('EMAIL_PASSWORD', 'SUA_SENHA_DE_APP')
```

## 🧪 Testando o Sistema

### 1. **Teste básico:**
```bash
curl -X POST http://localhost:5001/esqueci-senha \
  -H "Content-Type: application/json" \
  -d '{"email": "cliente@exemplo.com"}'
```

### 2. **Verificar logs no terminal:**
- ✅ Se funcionou: "Email enviado com sucesso"
- ❌ Se falhou: "Erro ao enviar email" + fallback para console

## 🔧 Configurações do Servidor SMTP

As configurações já estão prontas no código:

```python
smtp_server = "smtp-mail.outlook.com"  # Servidor do Outlook
smtp_port = 587                        # Porta TLS
server.starttls()                      # Criptografia obrigatória
```

## 🛠️ Solução de Problemas Comuns

### ❌ **"Authentication failed"**
- Verifique email e senha
- Use senha de app, não a senha normal
- Certifique-se que 2FA está configurado

### ❌ **"Connection refused"**
- Verifique sua conexão com internet
- Alguns firewalls bloqueiam porta 587

### ❌ **"Username and Password not accepted"**
- Outlook às vezes bloqueia aplicações "suspeitas"
- Tente fazer login manual no hotmail pelo navegador primeiro
- Aguarde alguns minutos e tente novamente

## 🚀 Para Produção

### Opções mais robustas:
1. **SendGrid** (gratuito até 100 emails/dia)
2. **Amazon SES** (muito barato)
3. **Mailgun** (primeiros 5000 emails grátis)

### Configuração atual é ideal para:
- ✅ Desenvolvimento e testes
- ✅ Aplicações pequenas (< 100 emails/dia)
- ✅ Prototipagem rápida

## 📝 Exemplo Completo

```python
# Testando manualmente no Python
import smtplib
from email.mime.text import MIMEText

# Suas credenciais
email = "seu_email@hotmail.com"
senha = "sua_senha_de_app"

# Teste rápido
msg = MIMEText("Teste do sistema")
msg['Subject'] = "Teste"
msg['From'] = email
msg['To'] = "destinatario@exemplo.com"

server = smtplib.SMTP("smtp-mail.outlook.com", 587)
server.starttls()
server.login(email, senha)
server.send_message(msg)
server.quit()
print("Email enviado!")
```

Agora seu sistema está pronto para enviar emails reais! 🎉