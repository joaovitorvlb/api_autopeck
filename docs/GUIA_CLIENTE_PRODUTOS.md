# 📱 Guia do Cliente - Como Trabalhar com Produtos e Imagens

## 📋 Sumário
1. [Estrutura de um Produto](#-estrutura-de-um-produto)
2. [Reconhecendo Produtos na Resposta](#-reconhecendo-produtos-na-resposta)
3. [Capturando Parâmetros](#-capturando-parâmetros)
4. [Trabalhando com URLs de Imagens](#-trabalhando-com-urls-de-imagens)
5. [Exemplos Práticos em Python](#-exemplos-práticos-em-python)
6. [Cenários de Uso](#-cenários-de-uso)
7. [Tratamento de Erros](#-tratamento-de-erros)

---

## 🏷️ Estrutura de um Produto

### **Formato Padrão da Resposta**
```json
{
    "id_produto": 6,
    "nome": "terminal",
    "descricao": "terminal do corsa",
    "preco": 45.5,
    "estoque": 6,
    "urls_imagem": {
        "large": "http://127.0.0.1:5001/images/produtos/produto_6_abc123_large.png",
        "medium": "http://127.0.0.1:5001/images/produtos/produto_6_abc123_medium.png",
        "thumbnail": "http://127.0.0.1:5001/images/produtos/produto_6_abc123_thumbnail.png"
    }
}
```

### **Campos Obrigatórios**
- **`id_produto`** (int): Identificador único do produto
- **`nome`** (str): Nome do produto
- **`preco`** (float): Preço unitário
- **`estoque`** (int): Quantidade disponível

### **Campos Opcionais**
- **`descricao`** (str): Descrição detalhada (pode ser vazia)
- **`urls_imagem`** (dict|null): URLs das imagens em diferentes resoluções

---

## 🔍 Reconhecendo Produtos na Resposta

### **1. Produto com Imagens**
```json
{
    "id_produto": 6,
    "nome": "Terminal Automotivo",
    "descricao": "Terminal do corsa modelo 2020",
    "preco": 45.5,
    "estoque": 12,
    "urls_imagem": {
        "thumbnail": "http://localhost:5001/images/produtos/produto_6_uuid_thumbnail.png",
        "medium": "http://localhost:5001/images/produtos/produto_6_uuid_medium.png",
        "large": "http://localhost:5001/images/produtos/produto_6_uuid_large.png"
    }
}
```

### **2. Produto sem Imagens**
```json
{
    "id_produto": 7,
    "nome": "Cabo USB",
    "descricao": "Cabo USB-C 2 metros",
    "preco": 25.0,
    "estoque": 50,
    "urls_imagem": null
}
```

### **3. Lista de Produtos**
```json
[
    {
        "id_produto": 1,
        "nome": "Mouse Gamer",
        "descricao": "Mouse RGB",
        "preco": 149.90,
        "estoque": 25,
        "urls_imagem": null
    },
    {
        "id_produto": 2,
        "nome": "Teclado Mecânico",
        "descricao": "Teclado switch blue",
        "preco": 299.90,
        "estoque": 15,
        "urls_imagem": {
            "thumbnail": "http://localhost:5001/images/produtos/produto_2_xyz789_thumbnail.jpg",
            "medium": "http://localhost:5001/images/produtos/produto_2_xyz789_medium.jpg",
            "large": "http://localhost:5001/images/produtos/produto_2_xyz789_large.jpg"
        }
    }
]
```

---

## 📝 Capturando Parâmetros

### **Python - Captura Básica**
```python
import requests

def capturar_produto(produto_id):
    """Captura e processa dados de um produto específico"""
    
    url = f"http://localhost:5001/produtos/{produto_id}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            produto = response.json()
            
            # Capturar parâmetros básicos
            id_produto = produto['id_produto']
            nome = produto['nome']
            preco = produto['preco']
            estoque = produto['estoque']
            descricao = produto.get('descricao', 'Sem descrição')
            
            print(f"🏷️ Produto: {nome} (ID: {id_produto})")
            print(f"💰 Preço: R$ {preco:.2f}")
            print(f"📦 Estoque: {estoque} unidades")
            print(f"📝 Descrição: {descricao}")
            
            # Verificar se tem imagens
            urls_imagem = produto.get('urls_imagem')
            if urls_imagem:
                print(f"🖼️ Possui {len(urls_imagem)} resoluções de imagem")
                return produto, True  # tem imagens
            else:
                print("📭 Produto sem imagens")
                return produto, False  # sem imagens
                
        else:
            print(f"❌ Erro: {response.status_code}")
            return None, False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None, False

# Exemplo de uso
produto, tem_imagens = capturar_produto(6)
```

### **Python - Captura com Validação**
```python
def capturar_produto_seguro(produto_id):
    """Captura produto com validação completa dos dados"""
    
    url = f"http://localhost:5001/produtos/{produto_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança exceção se status != 200
        
        produto = response.json()
        
        # Validar campos obrigatórios
        campos_obrigatorios = ['id_produto', 'nome', 'preco', 'estoque']
        for campo in campos_obrigatorios:
            if campo not in produto:
                raise ValueError(f"Campo obrigatório '{campo}' não encontrado")
        
        # Validar tipos
        if not isinstance(produto['id_produto'], int):
            raise TypeError("id_produto deve ser inteiro")
        if not isinstance(produto['preco'], (int, float)):
            raise TypeError("preco deve ser numérico")
        if not isinstance(produto['estoque'], int):
            raise TypeError("estoque deve ser inteiro")
        
        # Capturar dados validados
        dados_produto = {
            'id': produto['id_produto'],
            'nome': produto['nome'].strip(),
            'preco': float(produto['preco']),
            'estoque': int(produto['estoque']),
            'descricao': produto.get('descricao', '').strip(),
            'tem_imagens': produto.get('urls_imagem') is not None,
            'urls_imagem': produto.get('urls_imagem', {})
        }
        
        print(f"✅ Produto capturado com sucesso: {dados_produto['nome']}")
        return dados_produto
        
    except requests.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return None
    except (ValueError, TypeError) as e:
        print(f"❌ Erro de validação: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None
```

---

## 🖼️ Trabalhando com URLs de Imagens

### **1. Identificando Resoluções Disponíveis**
```python
def identificar_resolucoes(produto):
    """Identifica quais resoluções de imagem estão disponíveis"""
    
    urls_imagem = produto.get('urls_imagem')
    
    if not urls_imagem:
        print("📭 Produto não possui imagens")
        return []
    
    resolucoes_disponiveis = list(urls_imagem.keys())
    print(f"🖼️ Resoluções disponíveis: {', '.join(resolucoes_disponiveis)}")
    
    # Verificar cada resolução
    for resolucao, url in urls_imagem.items():
        print(f"   📸 {resolucao}: {url}")
    
    return resolucoes_disponiveis

# Exemplo de uso
produto = capturar_produto_seguro(6)
if produto:
    resolucoes = identificar_resolucoes(produto)
```

### **2. Baixando Imagens por Resolução**
```python
import os
from urllib.parse import urlparse

def baixar_imagem(url, pasta_destino="./imagens"):
    """Baixa uma imagem da URL fornecida"""
    
    try:
        # Criar pasta se não existir
        os.makedirs(pasta_destino, exist_ok=True)
        
        # Extrair nome do arquivo da URL
        parsed_url = urlparse(url)
        nome_arquivo = os.path.basename(parsed_url.path)
        caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
        
        # Baixar imagem
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(caminho_arquivo, 'wb') as arquivo:
            for chunk in response.iter_content(chunk_size=8192):
                arquivo.write(chunk)
        
        print(f"✅ Imagem baixada: {caminho_arquivo}")
        return caminho_arquivo
        
    except Exception as e:
        print(f"❌ Erro ao baixar imagem: {e}")
        return None

def baixar_todas_resolucoes(produto, pasta_destino="./imagens"):
    """Baixa todas as resoluções de imagem de um produto"""
    
    urls_imagem = produto.get('urls_imagem')
    if not urls_imagem:
        print("📭 Produto não possui imagens para baixar")
        return {}
    
    arquivos_baixados = {}
    
    for resolucao, url in urls_imagem.items():
        print(f"📥 Baixando resolução '{resolucao}'...")
        arquivo = baixar_imagem(url, pasta_destino)
        if arquivo:
            arquivos_baixados[resolucao] = arquivo
    
    print(f"🎉 Total baixado: {len(arquivos_baixados)} imagens")
    return arquivos_baixados

# Exemplo de uso
produto = capturar_produto_seguro(6)
if produto and produto['tem_imagens']:
    arquivos = baixar_todas_resolucoes(produto)
```

### **3. Escolhendo Resolução Adequada**
```python
def escolher_resolucao(urls_imagem, preferencia=['large', 'medium', 'thumbnail']):
    """Escolhe a melhor resolução disponível baseada na preferência"""
    
    if not urls_imagem:
        return None, None
    
    # Tentar cada resolução em ordem de preferência
    for resolucao_preferida in preferencia:
        if resolucao_preferida in urls_imagem:
            url = urls_imagem[resolucao_preferida]
            print(f"🎯 Resolução escolhida: {resolucao_preferida}")
            return resolucao_preferida, url
    
    # Se nenhuma preferência foi encontrada, usar a primeira disponível
    resolucao_disponivel = list(urls_imagem.keys())[0]
    url = urls_imagem[resolucao_disponivel]
    print(f"⚠️ Usando resolução disponível: {resolucao_disponivel}")
    return resolucao_disponivel, url

# Exemplos de uso
produto = capturar_produto_seguro(6)
if produto and produto['tem_imagens']:
    
    # Para exibição em lista (preferir thumbnail)
    resolucao, url = escolher_resolucao(produto['urls_imagem'], ['thumbnail', 'medium'])
    
    # Para visualização detalhada (preferir large)
    resolucao, url = escolher_resolucao(produto['urls_imagem'], ['large', 'medium'])
    
    # Para exibição em card (preferir medium)
    resolucao, url = escolher_resolucao(produto['urls_imagem'], ['medium', 'large', 'thumbnail'])
```

---

## 📱 Exemplos Práticos em Python

### **1. Cliente Completo para Produtos**
```python
import requests
import json
from typing import Dict, List, Optional, Tuple

class ProdutoClient:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def listar_produtos(self) -> List[Dict]:
        """Lista todos os produtos"""
        try:
            response = self.session.get(f"{self.base_url}/produtos")
            response.raise_for_status()
            produtos = response.json()
            
            print(f"📋 {len(produtos)} produtos encontrados")
            return produtos
            
        except Exception as e:
            print(f"❌ Erro ao listar produtos: {e}")
            return []
    
    def obter_produto(self, produto_id: int) -> Optional[Dict]:
        """Obtém um produto específico"""
        try:
            response = self.session.get(f"{self.base_url}/produtos/{produto_id}")
            response.raise_for_status()
            produto = response.json()
            
            print(f"✅ Produto obtido: {produto['nome']}")
            return produto
            
        except Exception as e:
            print(f"❌ Erro ao obter produto {produto_id}: {e}")
            return None
    
    def verificar_disponibilidade(self, produto_id: int, quantidade: int) -> bool:
        """Verifica se há estoque suficiente"""
        produto = self.obter_produto(produto_id)
        if not produto:
            return False
        
        estoque_disponivel = produto['estoque']
        disponivel = estoque_disponivel >= quantidade
        
        if disponivel:
            print(f"✅ Estoque OK: {estoque_disponivel} disponível, {quantidade} solicitado")
        else:
            print(f"❌ Estoque insuficiente: {estoque_disponivel} disponível, {quantidade} solicitado")
        
        return disponivel
    
    def obter_url_imagem(self, produto_id: int, resolucao: str = 'medium') -> Optional[str]:
        """Obtém URL de uma resolução específica"""
        produto = self.obter_produto(produto_id)
        if not produto or not produto.get('urls_imagem'):
            print(f"📭 Produto {produto_id} não possui imagens")
            return None
        
        urls_imagem = produto['urls_imagem']
        if resolucao in urls_imagem:
            return urls_imagem[resolucao]
        else:
            print(f"⚠️ Resolução '{resolucao}' não disponível. Disponíveis: {list(urls_imagem.keys())}")
            return None
    
    def formatar_produto_para_exibicao(self, produto: Dict) -> str:
        """Formata produto para exibição amigável"""
        nome = produto['nome']
        preco = produto['preco']
        estoque = produto['estoque']
        descricao = produto.get('descricao', 'Sem descrição')
        tem_imagens = "Sim" if produto.get('urls_imagem') else "Não"
        
        return f"""
🏷️ {nome} (ID: {produto['id_produto']})
💰 Preço: R$ {preco:.2f}
📦 Estoque: {estoque} unidades
📝 Descrição: {descricao}
🖼️ Imagens: {tem_imagens}
        """.strip()

# Exemplo de uso da classe
if __name__ == "__main__":
    client = ProdutoClient()
    
    # Listar todos os produtos
    produtos = client.listar_produtos()
    
    # Mostrar detalhes de cada produto
    for produto in produtos[:3]:  # Mostrar apenas os 3 primeiros
        print(client.formatar_produto_para_exibicao(produto))
        print("-" * 50)
    
    # Verificar disponibilidade
    if produtos:
        primeiro_produto = produtos[0]
        client.verificar_disponibilidade(primeiro_produto['id_produto'], 2)
        
        # Obter URL de imagem
        url_thumbnail = client.obter_url_imagem(primeiro_produto['id_produto'], 'thumbnail')
        if url_thumbnail:
            print(f"🔗 URL thumbnail: {url_thumbnail}")
```

### **2. Exemplo de Interface de Lista de Produtos**
```python
def exibir_lista_produtos():
    """Simula uma interface de lista de produtos"""
    
    client = ProdutoClient()
    produtos = client.listar_produtos()
    
    if not produtos:
        print("📭 Nenhum produto encontrado")
        return
    
    print("🛒 LISTA DE PRODUTOS")
    print("=" * 60)
    
    for i, produto in enumerate(produtos, 1):
        # Informações básicas
        nome = produto['nome']
        preco = produto['preco']
        estoque = produto['estoque']
        
        # URL da imagem (preferir thumbnail para lista)
        url_imagem = None
        if produto.get('urls_imagem'):
            urls = produto['urls_imagem']
            # Preferência: thumbnail > medium > large
            for resolucao in ['thumbnail', 'medium', 'large']:
                if resolucao in urls:
                    url_imagem = urls[resolucao]
                    break
        
        # Status do estoque
        status_estoque = "✅ Disponível" if estoque > 0 else "❌ Esgotado"
        
        print(f"{i:2d}. {nome}")
        print(f"    💰 R$ {preco:.2f}")
        print(f"    📦 {status_estoque} ({estoque} unidades)")
        if url_imagem:
            print(f"    🖼️ Imagem: {url_imagem}")
        else:
            print(f"    📭 Sem imagem")
        print()

# Exemplo de uso
exibir_lista_produtos()
```

### **3. Exemplo de Carrinho de Compras**
```python
class CarrinhoCompras:
    def __init__(self):
        self.client = ProdutoClient()
        self.itens = []  # Lista de {'produto_id': int, 'quantidade': int, 'produto': dict}
    
    def adicionar_item(self, produto_id: int, quantidade: int) -> bool:
        """Adiciona item ao carrinho"""
        
        # Verificar se produto existe
        produto = self.client.obter_produto(produto_id)
        if not produto:
            print(f"❌ Produto {produto_id} não encontrado")
            return False
        
        # Verificar estoque
        if not self.client.verificar_disponibilidade(produto_id, quantidade):
            return False
        
        # Verificar se já existe no carrinho
        for item in self.itens:
            if item['produto_id'] == produto_id:
                nova_quantidade = item['quantidade'] + quantidade
                if self.client.verificar_disponibilidade(produto_id, nova_quantidade):
                    item['quantidade'] = nova_quantidade
                    print(f"✅ Quantidade atualizada: {produto['nome']} x{nova_quantidade}")
                    return True
                else:
                    return False
        
        # Adicionar novo item
        self.itens.append({
            'produto_id': produto_id,
            'quantidade': quantidade,
            'produto': produto
        })
        
        print(f"✅ Adicionado ao carrinho: {produto['nome']} x{quantidade}")
        return True
    
    def calcular_total(self) -> float:
        """Calcula total do carrinho"""
        total = 0.0
        for item in self.itens:
            preco = item['produto']['preco']
            quantidade = item['quantidade']
            total += preco * quantidade
        return total
    
    def exibir_carrinho(self):
        """Exibe conteúdo do carrinho"""
        if not self.itens:
            print("🛒 Carrinho vazio")
            return
        
        print("🛒 CARRINHO DE COMPRAS")
        print("=" * 50)
        
        for i, item in enumerate(self.itens, 1):
            produto = item['produto']
            quantidade = item['quantidade']
            preco_unitario = produto['preco']
            subtotal = preco_unitario * quantidade
            
            print(f"{i}. {produto['nome']}")
            print(f"   💰 R$ {preco_unitario:.2f} x {quantidade} = R$ {subtotal:.2f}")
            
            # Mostrar thumbnail se disponível
            urls_imagem = produto.get('urls_imagem')
            if urls_imagem and 'thumbnail' in urls_imagem:
                print(f"   🖼️ {urls_imagem['thumbnail']}")
            print()
        
        total = self.calcular_total()
        print(f"💰 TOTAL: R$ {total:.2f}")

# Exemplo de uso do carrinho
carrinho = CarrinhoCompras()
carrinho.adicionar_item(6, 2)  # 2x Terminal
carrinho.adicionar_item(1, 1)  # 1x Mouse Gamer
carrinho.exibir_carrinho()
```

---

## 🎯 Cenários de Uso

### **1. Interface de E-commerce**
- **Lista de produtos**: Usar `thumbnail` para performance
- **Página de produto**: Usar `large` para visualização detalhada
- **Carrinho**: Usar `medium` para balanço entre qualidade e tamanho

### **2. App Mobile**
- **Lista**: `thumbnail` (150x150) para economia de dados
- **Detalhes**: `medium` (400x400) adequado para telas mobile
- **Zoom**: `large` (800x800) para visualização ampliada

### **3. Sistema de Gestão**
- **Relatórios**: Apenas dados sem imagens
- **Catálogo**: `medium` para visualização administrativa
- **Impressão**: `large` para qualidade de impressão

### **4. API Integration**
- **Cache**: Baixar `thumbnail` para cache local
- **Lazy Loading**: Carregar `medium` quando necessário
- **Full Quality**: `large` apenas quando solicitado

---

## 🛡️ Tratamento de Erros

### **1. Produto Não Encontrado**
```python
def tratar_produto_nao_encontrado(produto_id):
    """Exemplo de tratamento quando produto não existe"""
    
    response = requests.get(f"http://localhost:5001/produtos/{produto_id}")
    
    if response.status_code == 404:
        print(f"❌ Produto {produto_id} não encontrado")
        # Sugerir produtos similares, voltar para lista, etc.
        return None
    elif response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro inesperado: {response.status_code}")
        return None
```

### **2. Imagem Não Disponível**
```python
def tratar_imagem_indisponivel(produto):
    """Tratamento quando produto não tem imagem"""
    
    urls_imagem = produto.get('urls_imagem')
    
    if not urls_imagem:
        # Usar imagem placeholder
        placeholder_url = "http://localhost:5001/images/placeholder.png"
        return {
            'thumbnail': placeholder_url,
            'medium': placeholder_url,
            'large': placeholder_url
        }
    
    return urls_imagem
```

### **3. Falha de Conexão**
```python
def requisicao_com_retry(url, max_tentativas=3):
    """Faz requisição com retry automático"""
    
    for tentativa in range(max_tentativas):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout na tentativa {tentativa + 1}")
        except requests.exceptions.ConnectionError:
            print(f"🔌 Erro de conexão na tentativa {tentativa + 1}")
        except Exception as e:
            print(f"❌ Erro na tentativa {tentativa + 1}: {e}")
        
        if tentativa < max_tentativas - 1:
            print(f"🔄 Tentando novamente em 2 segundos...")
            time.sleep(2)
    
    print(f"❌ Falha após {max_tentativas} tentativas")
    return None
```

---

## 📚 Resumo das Melhores Práticas

### ✅ **Sempre Fazer**
1. **Validar dados** recebidos da API
2. **Tratar erros** de conexão e timeout
3. **Verificar se URLs de imagem existem** antes de usar
4. **Escolher resolução adequada** para cada contexto
5. **Implementar cache local** para melhor performance

### ❌ **Evitar**
1. **Assumir que produto sempre tem imagem**
2. **Usar apenas uma resolução** para todos os casos
3. **Não tratar erros de conexão**
4. **Baixar imagens desnecessariamente**
5. **Fazer muitas requisições seguidas** sem controle

### 🎯 **Dicas de Performance**
- Use `thumbnail` para listas
- Use `medium` para detalhes
- Use `large` apenas quando necessário
- Implemente lazy loading
- Cache imagens localmente
- Use timeout nas requisições

---

*Guia criado em: November 3, 2025*