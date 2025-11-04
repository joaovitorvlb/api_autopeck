# 🔐 Sistema de Recuperação de Senha - Guia Completo

## 📋 Funcionalidades Implementadas

O sistema agora possui um mecanismo completo de recuperação de senha com as seguintes funcionalidades:

1. **Solicitação de recuperação** via email
2. **Tokens seguros** com expiração automática
3. **Validação de tokens** antes da redefinição
4. **Interface web** para redefinir senha
5. **Sistema de logs** para auditoria
6. **Limpeza automática** de tokens expirados

---

## 🌐 Endpoints Disponíveis

### **1. POST /esqueci-senha**
Solicita recuperação de senha via email

**Request:**
```json
{
    "email": "joaovitorvlb@hotmail.com"
}
```

**Response (Sucesso):**
```json
{
    "mensagem": "Instruções de recuperação enviadas para seu email.",
    "status": "enviado",
    "validade": "30 minutos",
    "token_debug": "abc123def456..." 
}
```

**Response (Email não encontrado):**
```json
{
    "mensagem": "Se o email estiver cadastrado, você receberá instruções de recuperação.",
    "status": "processado"
}
```

### **2. POST /validar-token-recuperacao**
Valida se um token de recuperação é válido

**Request:**
```json
{
    "token": "abc123def456..."
}
```

**Response (Token válido):**
```json
{
    "valido": true,
    "email": "joaovitorvlb@hotmail.com",
    "tempo_restante": "25 minutos"
}
```

**Response (Token inválido):**
```json
{
    "valido": false,
    "erro": "Token inválido ou expirado"
}
```

### **3. POST /redefinir-senha**
Redefine a senha usando token válido

**Request:**
```json
{
    "token": "abc123def456...",
    "nova_senha": "minha_nova_senha_123"
}
```

**Response (Sucesso):**
```json
{
    "mensagem": "Senha redefinida com sucesso!",
    "status": "sucesso",
    "email": "joaovitorvlb@hotmail.com"
}
```

### **4. GET /redefinir-senha?token=...**
Página web para redefinir senha

Acessa: `http://localhost:5001/redefinir-senha?token=abc123def456...`

Retorna uma página HTML com formulário para redefinir senha.

### **5. GET /recovery-status**
Status dos tokens ativos (apenas para debug)

**Response:**
```json
{
    "tokens_ativos": 2,
    "tokens_expirados_removidos": 1,
    "detalhes": [
        {
            "token": "abc123def4...",
            "email": "user@example.com",
            "tempo_restante": "0:25:30",
            "usado": false,
            "expira_em": "2025-11-03 15:30:00"
        }
    ]
}
```

---

## 🐍 Exemplos de Uso em Python

### **1. Cliente Simples para Recuperação**
```python
import requests
import time

class RecuperacaoSenhaClient:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url.rstrip('/')
    
    def solicitar_recuperacao(self, email):
        """Solicita recuperação de senha"""
        url = f"{self.base_url}/esqueci-senha"
        data = {"email": email}
        
        try:
            response = requests.post(url, json=data)
            resultado = response.json()
            
            if response.status_code == 200:
                print(f"✅ {resultado['mensagem']}")
                if 'token_debug' in resultado:
                    print(f"🔑 Token (debug): {resultado['token_debug']}")
                return resultado.get('token_debug')
            else:
                print(f"❌ Erro: {resultado.get('erro')}")
                return None
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return None
    
    def validar_token(self, token):
        """Valida um token de recuperação"""
        url = f"{self.base_url}/validar-token-recuperacao"
        data = {"token": token}
        
        try:
            response = requests.post(url, json=data)
            resultado = response.json()
            
            if response.status_code == 200 and resultado.get('valido'):
                print(f"✅ Token válido para: {resultado['email']}")
                print(f"⏰ Tempo restante: {resultado['tempo_restante']}")
                return True
            else:
                print(f"❌ Token inválido: {resultado.get('erro')}")
                return False
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False
    
    def redefinir_senha(self, token, nova_senha):
        """Redefine senha usando token"""
        url = f"{self.base_url}/redefinir-senha"
        data = {
            "token": token,
            "nova_senha": nova_senha
        }
        
        try:
            response = requests.post(url, json=data)
            resultado = response.json()
            
            if response.status_code == 200:
                print(f"✅ {resultado['mensagem']}")
                return True
            else:
                print(f"❌ Erro: {resultado.get('erro')}")
                return False
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False

# Exemplo de uso completo
if __name__ == "__main__":
    client = RecuperacaoSenhaClient()
    
    # 1. Solicitar recuperação
    email = "joaovitorvlb@hotmail.com"
    token = client.solicitar_recuperacao(email)
    
    if token:
        # 2. Validar token
        if client.validar_token(token):
            # 3. Redefinir senha
            nova_senha = "minha_nova_senha_segura"
            client.redefinir_senha(token, nova_senha)
```

### **2. Exemplo Completo de Fluxo**
```python
def fluxo_recuperacao_completo():
    """Demonstra o fluxo completo de recuperação de senha"""
    
    client = RecuperacaoSenhaClient()
    
    print("🔐 SISTEMA DE RECUPERAÇÃO DE SENHA")
    print("=" * 50)
    
    # Passo 1: Solicitar recuperação
    email = input("📧 Digite seu email: ")
    
    print(f"\n1️⃣ Solicitando recuperação para {email}...")
    token = client.solicitar_recuperacao(email)
    
    if not token:
        print("❌ Falha na solicitação de recuperação")
        return
    
    # Passo 2: Simular tempo de recebimento do email
    print("\n📧 Simulando recebimento de email...")
    print(f"🔗 Link de recuperação: http://localhost:5001/redefinir-senha?token={token}")
    
    # Passo 3: Validar token
    print(f"\n2️⃣ Validando token...")
    if not client.validar_token(token):
        print("❌ Token inválido")
        return
    
    # Passo 4: Redefinir senha
    nova_senha = input("\n🔑 Digite a nova senha: ")
    
    print(f"\n3️⃣ Redefinindo senha...")
    sucesso = client.redefinir_senha(token, nova_senha)
    
    if sucesso:
        print("\n🎉 Recuperação concluída com sucesso!")
        print("✅ Agora você pode fazer login com a nova senha")
    else:
        print("\n❌ Falha na redefinição de senha")

# Executar fluxo
fluxo_recuperacao_completo()
```

---

## 🌐 Integração com Frontend

### **JavaScript/Web**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Recuperação de Senha</title>
</head>
<body>
    <h2>Esqueceu sua senha?</h2>
    
    <form id="recoveryForm">
        <input type="email" id="email" placeholder="Seu email" required>
        <button type="submit">Enviar link de recuperação</button>
    </form>
    
    <div id="message"></div>
    
    <script>
    document.getElementById('recoveryForm').onsubmit = async function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const messageDiv = document.getElementById('message');
        
        try {
            const response = await fetch('/esqueci-senha', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email: email})
            });
            
            const data = await response.json();
            
            if (response.ok) {
                messageDiv.innerHTML = `
                    <div style="color: green;">
                        ✅ ${data.mensagem}
                    </div>
                `;
                
                // Se tiver token debug, mostrar link direto
                if (data.token_debug) {
                    messageDiv.innerHTML += `
                        <p><a href="/redefinir-senha?token=${data.token_debug}" target="_blank">
                            🔗 Link direto (desenvolvimento)
                        </a></p>
                    `;
                }
            } else {
                messageDiv.innerHTML = `
                    <div style="color: red;">
                        ❌ ${data.erro}
                    </div>
                `;
            }
        } catch (error) {
            messageDiv.innerHTML = `
                <div style="color: red;">
                    ❌ Erro de conexão
                </div>
            `;
        }
    };
    </script>
</body>
</html>
```

---

## 🔧 Configurações e Segurança

### **Variáveis de Ambiente**
```bash
# Tempo de expiração dos tokens (em minutos)
export RECOVERY_TOKEN_EXPIRY=30

# Configurações de email (para produção)
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=seu_email@gmail.com
export SMTP_PASSWORD=sua_senha_app

# URL base da aplicação
export BASE_URL=https://sua-aplicacao.com
```

### **Integração com Email Real**
Para produção, substituir a função `send_recovery_email()`:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_recovery_email_real(email, token):
    """Envia email real usando SMTP"""
    
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    base_url = os.environ.get('BASE_URL', 'http://localhost:5001')
    
    if not all([smtp_user, smtp_password]):
        print("❌ Configurações de SMTP não encontradas")
        return False
    
    # Criar mensagem
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email
    msg['Subject'] = "🔐 Recuperação de Senha"
    
    recovery_link = f"{base_url}/redefinir-senha?token={token}"
    
    body = f"""
    <html>
    <body>
        <h2>🔐 Recuperação de Senha</h2>
        <p>Olá!</p>
        <p>Você solicitou a recuperação de sua senha.</p>
        <p><a href="{recovery_link}" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
            Redefinir Senha
        </a></p>
        <p><small>Este link é válido por 30 minutos.</small></p>
        <p><small>Se você não solicitou esta recuperação, ignore este email.</small></p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        # Conectar e enviar
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        text = msg.as_string()
        server.sendmail(smtp_user, email, text)
        server.quit()
        
        print(f"📧 Email enviado com sucesso para: {email}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False
```

---

## 🛡️ Medidas de Segurança

### **Implementadas**
✅ **Tokens seguros** usando `secrets.token_urlsafe()`  
✅ **Expiração automática** em 30 minutos  
✅ **Tokens de uso único** (não podem ser reutilizados)  
✅ **Não revelação** de existência de email  
✅ **Validação de entrada** em todos os endpoints  
✅ **Limpeza automática** de tokens expirados  

### **Recomendadas para Produção**
🔧 **Rate limiting** para evitar spam  
🔧 **Logs de auditoria** para tentativas de recuperação  
🔧 **HTTPS obrigatório** para proteção dos tokens  
🔧 **Hash das senhas** no banco de dados  
🔧 **Captcha** para formulários públicos  
🔧 **Notificação** de alteração de senha  

---

## 🧪 Testando o Sistema

### **1. Teste Básico via curl**
```bash
# 1. Solicitar recuperação
curl -X POST http://localhost:5001/esqueci-senha \
  -H "Content-Type: application/json" \
  -d '{"email":"joaovitorvlb@hotmail.com"}'

# 2. Usar token retornado para redefinir
curl -X POST http://localhost:5001/redefinir-senha \
  -H "Content-Type: application/json" \
  -d '{"token":"TOKEN_AQUI","nova_senha":"nova_senha_123"}'
```

### **2. Teste via Interface Web**
1. Acesse: `http://localhost:5001/esqueci-senha` (POST)
2. Copie o token do log do servidor
3. Acesse: `http://localhost:5001/redefinir-senha?token=TOKEN_AQUI`
4. Preencha o formulário

### **3. Verificar Status**
```bash
curl http://localhost:5001/recovery-status
```

---

## 📋 Checklist de Implementação

### **Para Desenvolvimento**
- [x] Endpoints de recuperação funcionando
- [x] Simulação de envio de email
- [x] Interface web básica
- [x] Validação de tokens
- [x] Sistema de expiração

### **Para Produção**
- [ ] Integração com serviço de email real
- [ ] Configuração de HTTPS
- [ ] Rate limiting implementado
- [ ] Logs de auditoria
- [ ] Hash de senhas no banco
- [ ] Testes automatizados
- [ ] Monitoramento de segurança

---

*Sistema implementado em: November 3, 2025*