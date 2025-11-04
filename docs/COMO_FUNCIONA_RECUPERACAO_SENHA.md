# 🔐 Como Funciona a Recuperação de Senha

## 📖 Visão Geral

O sistema de recuperação de senha permite que usuários redefinam suas senhas quando esquecem, usando um processo seguro baseado em tokens temporários enviados por email.

---

## 🔄 Fluxo Completo do Processo

### **1. Usuário Esquece a Senha**
```
Usuário tenta fazer login → Senha incorreta → Clica em "Esqueci minha senha"
```

### **2. Solicitação de Recuperação**
```
Usuário informa email → Sistema valida → Gera token seguro → Simula envio de email
```

### **3. Recebimento do Link**
```
Email com link → Usuário clica → Acessa página de redefinição
```

### **4. Redefinição da Senha**
```
Formulário web → Nova senha → Validação do token → Senha atualizada
```

### **5. Confirmação**
```
Sucesso → Token invalidado → Usuário pode fazer login com nova senha
```

---

## 🛠️ Como Funciona Tecnicamente

### **Componentes do Sistema**

#### **1. Geração de Token Seguro**
```python
import secrets

def generate_recovery_token():
    """Gera um token seguro de 32 bytes convertido para URL-safe string"""
    return secrets.token_urlsafe(32)
    # Exemplo: "abc123XYZ789_def456GHI012-jkl345MNO"
```

**Por que é seguro?**
- 32 bytes = 256 bits de entropia
- Impossível de adivinhar
- URL-safe (pode ser usado em links)

#### **2. Armazenamento Temporário**
```python
recovery_tokens = {
    "abc123XYZ789...": {
        "email": "usuario@exemplo.com",
        "expiry": datetime(2025, 11, 3, 15, 30, 0),  # 30 minutos no futuro
        "used": False
    }
}
```

**Estrutura dos dados:**
- **Token**: Chave única e segura
- **Email**: Para qual usuário é o token
- **Expiry**: Quando o token expira automaticamente
- **Used**: Se já foi usado (prevenção de reuso)

#### **3. Validação de Segurança**
```python
def validar_token(token):
    # 1. Token existe?
    if token not in recovery_tokens:
        return False, "Token não encontrado"
    
    # 2. Token já foi usado?
    if recovery_tokens[token]['used']:
        return False, "Token já utilizado"
    
    # 3. Token expirou?
    if datetime.now() > recovery_tokens[token]['expiry']:
        return False, "Token expirado"
    
    # 4. Token válido!
    return True, "Token válido"
```

---

## 📧 Sistema de Email (Simulado)

### **Como Funciona o Email**
```python
def send_recovery_email(email, token):
    """Simula envio de email com link de recuperação"""
    
    # 1. Criar link de recuperação
    recovery_link = f"http://localhost:5001/redefinir-senha?token={token}"
    
    # 2. Preparar conteúdo do email
    email_content = f"""
    🔐 RECUPERAÇÃO DE SENHA
    
    Clique no link para redefinir sua senha:
    {recovery_link}
    
    ⚠️ Válido por 30 minutos
    """
    
    # 3. "Enviar" email (no console para desenvolvimento)
    print(f"📧 Email para: {email}")
    print(f"📧 Conteúdo: {email_content}")
    
    return True
```

**Em produção seria:**
- Integração com SMTP (Gmail, SendGrid, AWS SES)
- Template HTML profissional
- Email real enviado para caixa de entrada

---

## 🌐 Endpoints e Como Usar

### **1. Solicitar Recuperação**

**Endpoint:** `POST /esqueci-senha`

**Como usar:**
```bash
curl -X POST http://localhost:5001/esqueci-senha \
  -H "Content-Type: application/json" \
  -d '{"email":"joaovitorvlb@hotmail.com"}'
```

**O que acontece:**
1. Sistema recebe email
2. Verifica se usuário existe (sem revelar se existe)
3. Gera token seguro
4. Armazena token com expiração
5. Simula envio de email
6. Retorna confirmação

**Resposta:**
```json
{
    "mensagem": "Instruções de recuperação enviadas para seu email.",
    "status": "enviado",
    "validade": "30 minutos",
    "token_debug": "abc123XYZ789..."
}
```

### **2. Validar Token (Opcional)**

**Endpoint:** `POST /validar-token-recuperacao`

**Como usar:**
```bash
curl -X POST http://localhost:5001/validar-token-recuperacao \
  -H "Content-Type: application/json" \
  -d '{"token":"abc123XYZ789..."}'
```

**Para que serve:**
- Frontend pode verificar se token é válido
- Mostrar tempo restante
- Evitar mostrar formulário para token inválido

### **3. Redefinir Senha**

**Endpoint:** `POST /redefinir-senha`

**Como usar:**
```bash
curl -X POST http://localhost:5001/redefinir-senha \
  -H "Content-Type: application/json" \
  -d '{"token":"abc123XYZ789...","nova_senha":"minha_nova_senha"}'
```

**O que acontece:**
1. Sistema recebe token e nova senha
2. Valida token (existe, não usado, não expirado)
3. Atualiza senha do usuário
4. Marca token como usado
5. Retorna confirmação

### **4. Interface Web**

**Endpoint:** `GET /redefinir-senha?token=abc123...`

**Como funciona:**
1. Usuário clica no link do email
2. Sistema valida token automaticamente
3. Se válido: mostra formulário
4. Se inválido: mostra erro
5. Usuário preenche nova senha
6. JavaScript envia para API

---

## 🔒 Medidas de Segurança

### **1. Token Seguro**
```python
# ❌ INSEGURO (não fazer)
token = str(random.randint(100000, 999999))  # 123456

# ✅ SEGURO (implementado)
token = secrets.token_urlsafe(32)  # abc123XYZ789_def456...
```

### **2. Expiração Automática**
```python
# Token expira em 30 minutos
expiry_time = datetime.now() + timedelta(minutes=30)

# Verificação automática
if datetime.now() > expiry_time:
    # Token expirado - rejeitar
```

### **3. Uso Único**
```python
# Após usar o token
recovery_tokens[token]['used'] = True

# Próxima tentativa será rejeitada
if recovery_tokens[token]['used']:
    return "Token já utilizado"
```

### **4. Não Revelação de Informações**
```python
# ❌ INSEGURO (revela se email existe)
if email not in users:
    return "Email não encontrado"

# ✅ SEGURO (não revela informação)
return "Se o email estiver cadastrado, você receberá instruções"
```

### **5. Limpeza Automática**
```python
# Remove tokens expirados automaticamente
current_time = datetime.now()
expired_tokens = [
    token for token, data in recovery_tokens.items() 
    if current_time > data['expiry']
]

for token in expired_tokens:
    del recovery_tokens[token]
```

---

## 🎯 Casos de Uso Práticos

### **Cenário 1: Recuperação Bem-Sucedida**

1. **João esquece a senha**
   ```
   João tenta: joao@email.com / senha123 → ❌ Erro
   ```

2. **Solicita recuperação**
   ```
   POST /esqueci-senha
   {"email": "joao@email.com"}
   ```

3. **Sistema processa**
   ```
   ✅ Email existe
   🔑 Token gerado: "xYz789AbC123..."
   ⏰ Expira em: 2025-11-03 15:30:00
   📧 Email enviado (simulado)
   ```

4. **João acessa link**
   ```
   http://localhost:5001/redefinir-senha?token=xYz789AbC123...
   ```

5. **Redefine senha**
   ```
   Formulário: Nova senha = "minhaNovaSenh@123"
   POST /redefinir-senha
   ```

6. **Sucesso!**
   ```
   ✅ Senha atualizada
   🔒 Token invalidado
   🎉 João pode fazer login
   ```

### **Cenário 2: Token Expirado**

1. **Maria solicita recuperação**
   ```
   Token gerado às 14:00, expira às 14:30
   ```

2. **Maria esquece do email**
   ```
   Tenta usar link às 15:00 (30 min depois)
   ```

3. **Sistema rejeita**
   ```
   ❌ "Token expirado"
   🗑️ Token removido automaticamente
   💡 "Solicite nova recuperação"
   ```

### **Cenário 3: Email Não Cadastrado**

1. **Pedro tenta recuperar**
   ```
   POST /esqueci-senha
   {"email": "pedro.nao.cadastrado@email.com"}
   ```

2. **Sistema não revela informação**
   ```
   ✅ "Se o email estiver cadastrado, você receberá instruções"
   🛡️ Não revela que email não existe
   ```

3. **Pedro não recebe email**
   ```
   Pedro percebe que precisa se cadastrar primeiro
   ```

---

## 🧪 Como Testar

### **Teste 1: Fluxo Completo**
```bash
# 1. Solicitar recuperação
curl -X POST http://localhost:5001/esqueci-senha \
  -H "Content-Type: application/json" \
  -d '{"email":"joaovitorvlb@hotmail.com"}'

# 2. Copiar token do console do servidor

# 3. Redefinir senha
curl -X POST http://localhost:5001/redefinir-senha \
  -H "Content-Type: application/json" \
  -d '{"token":"SEU_TOKEN_AQUI","nova_senha":"nova123"}'

# 4. Testar login com nova senha
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"joaovitorvlb@hotmail.com","senha":"nova123"}'
```

### **Teste 2: Interface Web**
```bash
# 1. Solicitar token via API ou interface

# 2. Acessar no navegador
http://localhost:5001/redefinir-senha?token=SEU_TOKEN

# 3. Preencher formulário
# 4. Verificar se senha foi alterada
```

### **Teste 3: Validações de Segurança**
```bash
# Token inexistente
curl -X POST http://localhost:5001/redefinir-senha \
  -d '{"token":"token_falso","nova_senha":"nova123"}'

# Token já usado (executar duas vezes)
curl -X POST http://localhost:5001/redefinir-senha \
  -d '{"token":"token_valido","nova_senha":"nova123"}'

# Esperar 30+ minutos e testar token expirado
```

---

## 🔧 Personalização e Configuração

### **Alterar Tempo de Expiração**
```python
# No código (linha ~1097)
expiry = datetime.now() + timedelta(minutes=30)  # Alterar aqui

# Ou via variável de ambiente
RECOVERY_TOKEN_EXPIRY = int(os.environ.get('RECOVERY_TOKEN_EXPIRY', 30))
expiry = datetime.now() + timedelta(minutes=RECOVERY_TOKEN_EXPIRY)
```

### **Customizar Email**
```python
def send_recovery_email(email, token):
    recovery_link = f"http://localhost:5001/redefinir-senha?token={token}"
    
    # Personalizar conteúdo aqui
    email_content = f"""
    🏢 SEU SISTEMA - Recuperação de Senha
    
    Olá!
    
    Recebemos uma solicitação para redefinir a senha da sua conta.
    
    👆 Clique aqui para redefinir: {recovery_link}
    
    ⚠️ Este link expira em 30 minutos
    ⚠️ Se não foi você, ignore este email
    
    Atenciosamente,
    Equipe de Suporte
    """
```

### **Integrar com Email Real (Produção)**
```python
import smtplib
from email.mime.text import MIMEText

def send_recovery_email_smtp(email, token):
    # Configurações SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "seu_email@gmail.com"
    smtp_password = "sua_senha_de_app"
    
    # Criar mensagem
    recovery_link = f"https://sua-aplicacao.com/redefinir-senha?token={token}"
    
    message = MIMEText(f"""
    Clique aqui para redefinir sua senha:
    {recovery_link}
    
    Este link expira em 30 minutos.
    """)
    
    message['Subject'] = 'Recuperação de Senha'
    message['From'] = smtp_user
    message['To'] = email
    
    # Enviar
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(message)
        server.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False
```

---

## 📋 Checklist de Implementação

### **✅ Já Implementado**
- [x] Geração de tokens seguros
- [x] Sistema de expiração automática
- [x] Validação de tokens
- [x] Interface web funcional
- [x] API completa
- [x] Prevenção de reuso de tokens
- [x] Não revelação de informações sensíveis
- [x] Limpeza automática de tokens expirados

### **🔧 Para Produção**
- [ ] Integração com SMTP real
- [ ] HTTPS obrigatório
- [ ] Rate limiting (evitar spam)
- [ ] Logs de auditoria
- [ ] Hash de senhas no banco
- [ ] Captcha em formulários
- [ ] Notificação de alteração de senha
- [ ] Testes automatizados

---

## 🆘 Solução de Problemas

### **Problema: Token não funciona**
```
🔍 Verificar:
1. Token foi copiado corretamente?
2. Token expirou? (válido por 30 minutos)
3. Token já foi usado?
4. Servidor está rodando?
```

### **Problema: Email não chega**
```
🔍 No desenvolvimento:
- Email aparece no console do servidor
- Procurar por "📧 [EMAIL]" nos logs

🔧 Em produção:
- Verificar configurações SMTP
- Verificar caixa de spam
- Verificar logs de envio
```

### **Problema: Erro de validação**
```
🔍 Verificar:
- Formato do JSON está correto?
- Campos obrigatórios estão presentes?
- Nova senha tem pelo menos 4 caracteres?
```

---

## 🎯 Resumo

O sistema de recuperação de senha implementado é:

- **🛡️ Seguro**: Tokens criptograficamente seguros
- **⏰ Temporário**: Expiração automática em 30 minutos  
- **🔒 Único**: Cada token só pode ser usado uma vez
- **🚫 Privado**: Não revela informações sobre usuários
- **🧹 Limpo**: Remove tokens expirados automaticamente
- **🌐 Completo**: API + Interface web funcional

**Próximo passo:** Integrar com serviço de email real para produção!

---

*Documentação criada em: November 3, 2025*