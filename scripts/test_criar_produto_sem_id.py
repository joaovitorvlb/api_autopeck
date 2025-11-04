#!/usr/bin/env python3
"""
Teste para verificar se o cadastro de produto funciona sem ID
"""

import requests
import json

BASE_URL = "http://localhost:5001"

def test_login():
    """Faz login e retorna token"""
    login_data = {
        "usuario": "admin",
        "senha": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    if response.status_code == 200:
        return response.json().get('token')
    return None

def test_criar_produto(token):
    """Testa criação de produto sem ID"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    produto_data = {
        "nome": "Produto Teste Tkinter",
        "preco": 99.90,
        "estoque": 50,
        "descricao": "Produto criado para testar a correção do Tkinter"
    }
    
    print("📤 Enviando dados do produto:")
    print(json.dumps(produto_data, indent=2, ensure_ascii=False))
    
    response = requests.post(f"{BASE_URL}/produtos", json=produto_data, headers=headers)
    
    print(f"\n📥 Resposta da API:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        produto_criado = response.json()
        print(f"\n✅ Produto criado com sucesso!")
        print(f"ID gerado: {produto_criado.get('id_produto')}")
        return produto_criado.get('id_produto')
    else:
        print(f"\n❌ Erro ao criar produto")
        return None

def main():
    print("🧪 Testando criação de produto sem ID")
    print("=" * 50)
    
    # Fazer login
    print("1. Fazendo login...")
    token = test_login()
    
    if not token:
        print("❌ Falha no login")
        return
    
    print(f"✅ Login OK - Token: {token[:30]}...")
    
    # Testar criação de produto
    print("\n2. Testando criação de produto...")
    produto_id = test_criar_produto(token)
    
    if produto_id:
        print(f"\n🎉 Teste bem-sucedido! Produto criado com ID: {produto_id}")
        print("💡 Agora o Tkinter deve funcionar corretamente!")
    else:
        print("\n💥 Teste falhou - verificar logs do servidor")

if __name__ == "__main__":
    main()