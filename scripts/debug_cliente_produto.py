#!/usr/bin/env python3
"""
Teste específico para debug da criação de produto
Com logs detalhados do cliente
"""

import requests
import json

BASE_URL = "http://localhost:5001"

def test_login():
    """Faz login e retorna token"""
    print("🔐 [CLIENT] Fazendo login...")
    
    login_data = {"usuario": "admin", "senha": "admin"}
    print(f"📤 [CLIENT] Dados de login: {login_data}")
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data, timeout=30)
        print(f"📥 [CLIENT] Resposta login - Status: {response.status_code}")
        print(f"📥 [CLIENT] Resposta login - Headers: {dict(response.headers)}")
        print(f"📥 [CLIENT] Resposta login - Texto: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"✅ [CLIENT] Token obtido: {token[:30]}...")
            return token
        else:
            print(f"❌ [CLIENT] Login falhou")
            return None
            
    except Exception as e:
        print(f"💥 [CLIENT] Erro no login: {e}")
        return None

def test_criar_produto(token):
    """Testa criação de produto com logs detalhados"""
    print("\n📦 [CLIENT] Testando criação de produto...")
    
    # Dados do produto
    produto_data = {
        "nome": "Produto Teste Debug",
        "preco": 99.99,
        "estoque": 10,
        "descricao": "Produto para testar debug do cliente"
    }
    
    print(f"📤 [CLIENT] Dados do produto a enviar:")
    print(f"   - Tipo: {type(produto_data)}")
    print(f"   - Conteúdo: {produto_data}")
    print(f"   - JSON string: {json.dumps(produto_data, indent=2)}")
    
    # Headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print(f"📤 [CLIENT] Headers: {headers}")
    
    try:
        print(f"🌐 [CLIENT] Fazendo POST para: {BASE_URL}/produtos")
        
        response = requests.post(
            f"{BASE_URL}/produtos", 
            json=produto_data, 
            headers=headers, 
            timeout=60
        )
        
        print(f"📥 [CLIENT] Resposta - Status: {response.status_code}")
        print(f"📥 [CLIENT] Resposta - Headers: {dict(response.headers)}")
        print(f"📥 [CLIENT] Resposta - Texto: {response.text}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ [CLIENT] Produto criado com sucesso!")
            print(f"📦 [CLIENT] Dados retornados: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return data.get('id_produto')
        else:
            print(f"❌ [CLIENT] Erro na criação")
            try:
                error_data = response.json()
                print(f"📄 [CLIENT] Erro JSON: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"📄 [CLIENT] Erro não é JSON válido")
            return None
            
    except Exception as e:
        print(f"💥 [CLIENT] Exceção na criação: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_raw_request():
    """Teste com requisição HTTP raw"""
    print("\n🔧 [CLIENT] Testando requisição HTTP raw...")
    
    # Primeiro fazer login para obter token
    token = test_login()
    if not token:
        return
    
    # Dados como string JSON
    json_string = json.dumps({
        "nome": "Produto Raw Test",
        "preco": 19.99,
        "estoque": 5,
        "descricao": "Teste raw HTTP"
    })
    
    print(f"📤 [CLIENT] JSON string raw: {json_string}")
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{BASE_URL}/produtos",
            data=json_string,
            headers=headers,
            timeout=60
        )
        
        print(f"📥 [CLIENT] Resposta raw - Status: {response.status_code}")
        print(f"📥 [CLIENT] Resposta raw - Texto: {response.text}")
        
    except Exception as e:
        print(f"💥 [CLIENT] Erro no teste raw: {e}")

def main():
    print("🔍 DEBUG DETALHADO - Criação de Produto")
    print("=" * 60)
    
    # Teste 1: Login
    token = test_login()
    if not token:
        print("💥 Não foi possível fazer login - parando testes")
        return
    
    # Teste 2: Criar produto normal
    produto_id = test_criar_produto(token)
    
    # Teste 3: Requisição raw
    test_raw_request()
    
    print("\n" + "=" * 60)
    print("🏁 Testes de debug concluídos")
    print("💡 Verifique os logs do servidor Flask para detalhes do lado servidor")

if __name__ == "__main__":
    main()