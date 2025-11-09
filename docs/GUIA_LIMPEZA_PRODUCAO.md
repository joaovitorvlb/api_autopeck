# 🧹 Guia de Limpeza e Reset - Produção PythonAnywhere

Este guia explica como limpar dados de teste e resetar o ambiente de produção para o estado inicial padrão.

---

## ⚠️ IMPORTANTE

> **ATENÇÃO:** Estas operações são **DESTRUTIVAS** e **NÃO PODEM SER DESFEITAS**!  
> Certifique-se de fazer backup antes de executar.

---

## 📋 O que será feito:

- ❌ **Remover** todas as imagens de teste de produtos
- ❌ **Apagar** todos os dados de teste do banco de dados
- ✅ **Inserir** apenas dados padrão iniciais
- ✅ **Manter** estrutura das tabelas intacta

---

## Método 1: Script Python Automatizado (Recomendado)

### Passo 1: Acessar o Bash Console

No PythonAnywhere:
1. Dashboard → **Consoles** → **Bash**

### Passo 2: Executar o Script

```bash
# Navegar para o projeto
cd ~/api_autopeck

# Ativar ambiente virtual
source venv/bin/activate

# Executar script de limpeza
python scripts/limpar_producao.py
```

### Passo 3: Confirmar a Operação

O script irá pedir confirmação:
```
⚠️  ATENÇÃO: OPERAÇÃO DESTRUTIVA ⚠️

Este script irá:
  1. ❌ Remover TODAS as imagens de produtos
  2. ❌ Apagar TODOS os dados de teste do banco
  3. ✅ Inserir apenas dados padrão iniciais

⚠️  Esta ação NÃO PODE SER DESFEITA!

Deseja continuar? Digite 'SIM' para confirmar:
```

Digite: **`SIM`** (em maiúsculas) e pressione Enter.

### Passo 4: Verificar Resultado

O script mostrará o progresso:
```
🗑️  Limpando imagens de teste...
  ✅ Removido: produto_11_271086f29aff41408bd3a8e61352c804.png
  ✅ Removido: produto_12_thumbnail.jpg
  ...

🗄️  Resetando banco de dados MySQL...
  🔗 Conectado ao MySQL
  🗑️  Limpando tabelas...
  ✅ Tabelas limpas
  📝 Inserindo dados padrão...
  ✅ Funcionários inseridos
  ✅ Clientes inseridos
  ✅ Produtos inseridos

✅ LIMPEZA CONCLUÍDA COM SUCESSO!
```

---

## Método 2: Limpeza Manual (Passo a Passo)

### 2.1 Remover Imagens de Teste

```bash
# Acessar o diretório de imagens
cd ~/api_autopeck/static/images/produtos

# Listar imagens (para conferir)
ls -lh

# Remover todas as imagens (EXCETO README.md)
find . -type f ! -name 'README.md' -delete

# Verificar se foi limpo
ls -lh
```

### 2.2 Resetar Banco de Dados MySQL

**Opção A - Console MySQL (Interface Web):**

1. Dashboard → **Databases** → **Open MySQL console**
2. Copiar e colar o conteúdo do arquivo `scripts/reset_banco_producao.sql`
3. **IMPORTANTE**: Substituir `seu_usuario$default` pelo seu banco real
4. Executar o script completo

**Opção B - Bash Console:**

```bash
cd ~/api_autopeck

# Executar script SQL direto
mysql -u SEU_USUARIO -p'SUA_SENHA' \
  -h SEU_USUARIO.mysql.pythonanywhere-services.com \
  SEU_USUARIO$default < scripts/reset_banco_producao.sql
```

### 2.3 Verificar Dados Inseridos

```bash
# Conectar ao MySQL
mysql -u SEU_USUARIO -p'SUA_SENHA' \
  -h SEU_USUARIO.mysql.pythonanywhere-services.com \
  SEU_USUARIO$default

# No console MySQL, verificar:
SELECT COUNT(*) as total FROM Funcionario;  -- Deve retornar 3
SELECT COUNT(*) as total FROM Cliente;      -- Deve retornar 3
SELECT COUNT(*) as total FROM Produto;      -- Deve retornar 5
SELECT COUNT(*) as total FROM Venda;        -- Deve retornar 0

# Sair do MySQL
exit;
```

---

## Método 3: Limpeza Seletiva (Apenas Imagens)

Se quiser **apenas remover imagens** sem mexer no banco:

```bash
cd ~/api_autopeck/static/images/produtos

# Listar arquivos por data (mais recentes primeiro)
ls -lt

# Remover apenas imagens específicas
rm produto_11_*.png
rm produto_12_*.jpg

# Ou remover todas de uma vez
rm *.jpg *.png *.jpeg *.gif *.webp
```

---

## Método 4: Limpeza Seletiva (Apenas Banco)

Se quiser **apenas limpar banco** sem remover imagens:

```sql
-- No console MySQL
USE seu_usuario$default;

-- Limpar apenas dados de teste (mantém produtos sem imagem)
DELETE FROM Item_Venda;
DELETE FROM Venda WHERE id_venda > 0;
DELETE FROM Produto WHERE id_produto > 5;  -- Mantém os 5 produtos padrão
DELETE FROM Cliente WHERE id_cliente > 3;  -- Mantém os 3 clientes padrão

-- Verificar
SELECT * FROM Produto;
SELECT * FROM Cliente;
```

---

## 📊 Dados Padrão Inseridos

### 👥 Funcionários (3)
| ID | Nome | Cargo | Salário |
|----|------|-------|---------|
| 1 | Maria Silva | Vendedora | R$ 2.500,00 |
| 2 | Admin Sistema | Administrador | R$ 4.500,00 |
| 3 | Carlos Lima | Gerente | R$ 3.500,00 |

### 👤 Clientes (3)
| ID | Nome | Email | Telefone |
|----|------|-------|----------|
| 1 | João Silva | joao@email.com | 11999999999 |
| 2 | Ana Santos | ana@email.com | 11888888888 |
| 3 | Pedro Oliveira | pedro@email.com | 11777777777 |

### 🛒 Produtos (5)
| ID | Nome | Preço | Estoque | Imagem |
|----|------|-------|---------|--------|
| 1 | Filtro de Óleo | R$ 29,90 | 100 | NULL |
| 2 | Pastilha de Freio | R$ 89,90 | 50 | NULL |
| 3 | Amortecedor Dianteiro | R$ 189,90 | 30 | NULL |
| 4 | Vela de Ignição | R$ 45,90 | 80 | NULL |
| 5 | Correia Dentada | R$ 65,90 | 25 | NULL |

### 🛍️ Vendas e Itens de Venda
- **0** vendas (tabela vazia)
- **0** itens de venda (tabela vazia)

---

## 🔄 Após a Limpeza

### 1. Reload da Aplicação
```
Dashboard → Web → Reload (botão verde)
```

### 2. Testar a API

**Listar produtos:**
```bash
curl https://SEU_USUARIO.pythonanywhere.com/produtos
```

**Resposta esperada:**
```json
[
  {
    "id_produto": 1,
    "nome": "Filtro de Óleo",
    "descricao": "Filtro de óleo para motores 1.0 a 2.0",
    "preco": 29.90,
    "estoque": 100,
    "nome_imagem": null
  },
  ...
]
```

### 3. Testar Upload de Nova Imagem

```bash
# Fazer login primeiro
TOKEN=$(curl -s -X POST https://SEU_USUARIO.pythonanywhere.com/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"maria","senha":"1234"}' | jq -r '.token')

# Fazer upload de imagem para um produto
curl -X POST https://SEU_USUARIO.pythonanywhere.com/produtos/1/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "imagem=@imagem_teste.jpg"
```

---

## 🛡️ Backup Antes de Limpar

### Backup do Banco de Dados

```bash
# Fazer backup completo
mysqldump -u SEU_USUARIO -p'SUA_SENHA' \
  -h SEU_USUARIO.mysql.pythonanywhere-services.com \
  SEU_USUARIO$default > backup_$(date +%Y%m%d_%H%M%S).sql

# Verificar se foi criado
ls -lh backup_*.sql
```

### Backup das Imagens

```bash
# Criar arquivo compactado das imagens
cd ~/api_autopeck
tar -czf backup_imagens_$(date +%Y%m%d_%H%M%S).tar.gz static/images/produtos/

# Verificar
ls -lh backup_imagens_*.tar.gz
```

### Restaurar Backup (se necessário)

```bash
# Restaurar banco
mysql -u SEU_USUARIO -p'SUA_SENHA' \
  -h SEU_USUARIO.mysql.pythonanywhere-services.com \
  SEU_USUARIO$default < backup_20241108_150000.sql

# Restaurar imagens
cd ~/api_autopeck
tar -xzf backup_imagens_20241108_150000.tar.gz
```

---

## ❓ Perguntas Frequentes

### Q: Posso desfazer após executar?
**R:** Não, a menos que tenha feito backup antes. As operações são destrutivas.

### Q: Os IDs dos produtos vão resetar?
**R:** No MySQL, os IDs começam do 1 novamente após TRUNCATE. No SQLite, se você deletar a tabela sqlite_sequence.

### Q: As tabelas serão recriadas?
**R:** Não, apenas os dados são removidos. A estrutura permanece intacta.

### Q: Quanto tempo demora?
**R:** Geralmente menos de 1 minuto para limpar tudo.

### Q: Preciso fazer reload da aplicação?
**R:** Sim, sempre faça reload após modificar banco ou arquivos.

---

## 📝 Checklist de Limpeza

- [ ] Fazer backup do banco de dados
- [ ] Fazer backup das imagens (opcional)
- [ ] Executar script de limpeza OU executar passos manuais
- [ ] Verificar que dados padrão foram inseridos
- [ ] Verificar que imagens foram removidas
- [ ] Fazer reload da aplicação
- [ ] Testar listagem de produtos
- [ ] Testar upload de nova imagem
- [ ] Testar login com usuários padrão

---

## 🎯 Resultado Final

Após a limpeza completa, você terá:

✅ **5 produtos** padrão sem imagens  
✅ **3 clientes** iniciais  
✅ **3 funcionários** para login  
✅ **0 vendas** registradas  
✅ **Diretório de imagens** limpo (apenas README.md)  
✅ **Aplicação** funcionando normalmente  

---

## 📞 Suporte

Se encontrar problemas durante a limpeza:

1. Verificar logs de erro no PythonAnywhere
2. Conferir permissões dos diretórios
3. Testar conexão com o banco MySQL
4. Verificar se as tabelas existem

**Comandos úteis:**
```bash
# Ver logs de erro
tail -50 ~/mysite/error.log

# Verificar conexão MySQL
mysql -u SEU_USUARIO -p -h SEU_USUARIO.mysql.pythonanywhere-services.com

# Verificar permissões
ls -la ~/api_autopeck/static/images/produtos/
```

---

**Boa sorte com a limpeza! 🚀**
