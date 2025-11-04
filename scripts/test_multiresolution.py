#!/usr/bin/env python3
"""
Script de teste para demonstrar o sistema de múltiplas resoluções de imagem
Atualizado para API atual com JWT e porta 5001
"""

import requests
import json
import os

# Configuração da API
BASE_URL = "http://localhost:5001"

# Credenciais de teste
CREDENTIALS = {
    "usuario": "admin",
    "senha": "admin"
}

def authenticate():
    """Faz login e retorna o token JWT"""
    print("🔐 Fazendo login...")
    
    response = requests.post(f"{BASE_URL}/login", json=CREDENTIALS)
    
    if response.status_code == 200:
        token = response.json().get('token')
        print(f"✅ Login bem-sucedido! Token: {token[:30]}...")
        return token
    else:
        print(f"❌ Erro no login: {response.status_code} - {response.text}")
        return None

def get_headers(token):
    """Retorna headers com autenticação JWT"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def test_multiresolution_system():
    """Testa o sistema completo de múltiplas resoluções"""
    
    print("🔧 Testando Sistema de Múltiplas Resoluções de Imagem")
    print("=" * 60)
    
    # Autenticar primeiro
    token = authenticate()
    if not token:
        return
    
    headers = get_headers(token)
    
    # 1. Verificar se há produtos
    print("\n1. Listando produtos...")
    response = requests.get(f"{BASE_URL}/produtos", headers=headers)
    
    if response.status_code == 200:
        produtos = response.json()
        print(f"✅ Encontrados {len(produtos)} produtos")
        
        for produto in produtos:
            print(f"\n📦 Produto: {produto['nome']} (ID: {produto['id_produto']})")
            
            # Verificar se tem URL de imagem ou URLs de imagem multi-resolução
            if 'urls_imagem' in produto and produto['urls_imagem']:
                print("🖼️  Resoluções disponíveis:")
                for resolution, url in produto['urls_imagem'].items():
                    print(f"   • {resolution}: {url}")
            elif 'url' in produto and produto['url']:
                print(f"🖼️  Imagem única: {produto['url']}")
            else:
                print("   ⚠️  Nenhuma imagem disponível")
    else:
        print(f"❌ Erro ao listar produtos: {response.status_code} - {response.text}")
        return
    
    # 2. Buscar produto específico
    if produtos:
        produto_id = produtos[0]['id_produto']
        print(f"\n2. Buscando produto específico (ID: {produto_id})...")
        
        response = requests.get(f"{BASE_URL}/produtos/{produto_id}", headers=headers)
        if response.status_code == 200:
            produto = response.json()
            print(f"✅ Produto encontrado: {produto['nome']}")
            
            if 'urls_imagem' in produto and produto['urls_imagem']:
                print("🖼️  Detalhes das resoluções:")
                for resolution, url in produto['urls_imagem'].items():
                    # Testar se a imagem está acessível (sem autenticação para imagens)
                    try:
                        img_response = requests.head(url, timeout=5)
                        status = "✅ Acessível" if img_response.status_code == 200 else "❌ Não encontrada"
                    except:
                        status = "❓ Não testável"
                    print(f"   • {resolution.upper()}: {url} - {status}")
            elif 'url' in produto and produto['url']:
                print(f"🖼️  Imagem única: {produto['url']}")
            else:
                print("   ⚠️  Nenhuma imagem configurada")
        else:
            print(f"❌ Erro ao buscar produto: {response.status_code} - {response.text}")
    
    # 3. Testar rota de upload (mostrar como usar)
    if produtos:
        produto_id = produtos[0]['id_produto']
        print(f"\n3. Testando informações de upload para produto {produto_id}...")
        print(f"📤 Para fazer upload de imagem:")
        print(f"   URL: {BASE_URL}/produtos/{produto_id}/upload-image")
        print(f"   Método: POST")
        print(f"   Headers: Authorization: Bearer {token[:30]}...")
        print(f"   Body: multipart/form-data com campo 'image'")
        print(f"   Exemplo curl:")
        print(f'   curl -X POST -H "Authorization: Bearer {token}" \\')
        print(f'        -F "image=@sua_imagem.jpg" \\')
        print(f'        {BASE_URL}/produtos/{produto_id}/upload-image')

def demonstrate_usage():
    """Demonstra como usar o sistema no frontend"""
    
    print("\n" + "=" * 60)
    print("📱 EXEMPLO DE USO NO FRONTEND ANDROID")
    print("=" * 60)
    
    print("""
Para usar no RecyclerView Android, você pode escolher a resolução baseada no contexto:

// Exemplo em Java/Kotlin para RecyclerView
public void bindProduct(Product product) {
    // Para lista (RecyclerView) - usar thumbnail
    Map<String, String> images = product.getUrlsImagem();
    if (images != null && images.containsKey("thumbnail")) {
        String thumbnailUrl = images.get("thumbnail");
        Glide.with(context)
            .load(thumbnailUrl)
            .placeholder(R.drawable.placeholder)
            .into(imageView);
    }
    
    // Para tela de detalhes - usar medium
    String detailUrl = images.get("medium");
    
    // Para zoom/visualização ampliada - usar large
    String largeUrl = images.get("large");
}

// Estrutura JSON atual retornada pela API:
{
    "id_produto": 1,
    "nome": "Produto Exemplo",
    "preco": 29.90,
    "estoque": 100,
    "descricao": "Descrição do produto",
    "url": "url_original_se_existir",
    "urls_imagem": {
        "thumbnail": "http://localhost:5001/images/produtos/thumbs/produto_1_abc123.jpg",
        "medium": "http://localhost:5001/images/produtos/medium/produto_1_abc123.jpg", 
        "large": "http://localhost:5001/images/produtos/full/produto_1_abc123.jpg"
    }
}

📐 RESOLUÇÕES CONFIGURADAS:
• Thumbnail: 150x150px - Para listas e miniaturas (thumbs/)
• Medium: 400x400px - Para cards e detalhes (medium/)
• Large: 800x800px - Para visualização ampliada (full/)

🔄 COMO FAZER UPLOAD (COM AUTENTICAÇÃO JWT):
1. POST /login com {"usuario": "admin", "senha": "admin"}
2. Obter token da resposta
3. POST /produtos/{id}/upload-image
   Headers: Authorization: Bearer {token}
   Content-Type: multipart/form-data
   Body: image=[arquivo]

Resposta do upload:
{
    "mensagem": "Imagem enviada com sucesso",
    "urls": {
        "thumbnail": "http://localhost:5001/images/produtos/thumbs/produto_1_abc123.jpg",
        "medium": "http://localhost:5001/images/produtos/medium/produto_1_abc123.jpg",
        "large": "http://localhost:5001/images/produtos/full/produto_1_abc123.jpg"
    }
}

🔐 AUTENTICAÇÃO ANDROID:
// Login para obter token
JSONObject loginData = new JSONObject();
loginData.put("usuario", "admin");
loginData.put("senha", "admin");

// Fazer requisição de login
// Salvar token recebido
// Incluir em todas as requisições: Authorization: Bearer {token}
""")

def show_test_commands():
    """Mostra comandos para testes manuais"""
    print("\n" + "=" * 60)
    print("🧪 COMANDOS PARA TESTES MANUAIS")
    print("=" * 60)
    
    print("""
Para testar manualmente, execute estes comandos:

# 1. Fazer login e obter token
curl -X POST http://localhost:5001/login \\
     -H "Content-Type: application/json" \\
     -d '{"usuario":"admin","senha":"admin"}'

# 2. Listar produtos (substitua {TOKEN} pelo token obtido)
curl -X GET http://localhost:5001/produtos \\
     -H "Authorization: Bearer {TOKEN}"

# 3. Upload de imagem (substitua {TOKEN} e {ID_PRODUTO})
curl -X POST http://localhost:5001/produtos/{ID_PRODUTO}/upload-image \\
     -H "Authorization: Bearer {TOKEN}" \\
     -F "image=@caminho/para/sua/imagem.jpg"

# 4. Acessar imagem diretamente (sem autenticação)
curl -I http://localhost:5001/images/produtos/thumbs/nome_arquivo.jpg

# 5. Deletar imagem de produto
curl -X DELETE http://localhost:5001/produtos/{ID_PRODUTO}/delete-image \\
     -H "Authorization: Bearer {TOKEN}"
""")

def main():
    """Função principal do teste"""
    try:
        test_multiresolution_system()
        demonstrate_usage()
        show_test_commands()
        
        print("\n" + "=" * 60)
        print("✅ TESTE CONCLUÍDO!")
        print("💡 Para testar upload, use os comandos curl mostrados acima")
        print("� Servidor deve estar rodando em http://localhost:5001")
        print("🔐 Login necessário para todas as operações de produtos")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
        print("💡 Certifique-se de que o servidor Flask está rodando em http://localhost:5001")
        print("🚀 Para iniciar: python app.py")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    main()