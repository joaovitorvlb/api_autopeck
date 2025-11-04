#!/usr/bin/env python3
import requests
import json
import time

# Aguardar um pouco para garantir que o servidor está rodando
time.sleep(2)

base_url = "http://127.0.0.1:5001"

def test_produtos(token=None):
    """Testa a API de produtos"""
    try:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
            
        response = requests.get(f"{base_url}/produtos", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Produtos encontrados: {len(data)}")
            
            # Verifica se há produtos com URLs de imagem
            for produto in data:
                if 'urls_imagem' in produto:
                    print(f"Produto {produto['nome']} tem URLs de imagem:")
                    for key, url in produto['urls_imagem'].items():
                        print(f"  {key}: {url}")
                        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Erro ao testar produtos: {e}")
        return False

def test_login():
    """Testa o login"""
    try:
        login_data = {
            "usuario": "admin",
            "senha": "admin"
        }
        
        response = requests.post(f"{base_url}/login", json=login_data)
        print(f"Login Status Code: {response.status_code}")
        print(f"Login Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            return data.get('token')
        return None
        
    except Exception as e:
        print(f"Erro ao testar login: {e}")
        return None

if __name__ == "__main__":
    print("=== Testando API ===")
    
    # Primeiro fazer login para obter token
    print("\n1. Testando POST /login")
    token = test_login()
    
    if token:
        print(f"Token recebido: {token[:50]}...")
        
        # Teste de produtos com token
        print("\n2. Testando GET /produtos (com autenticação)")
        success = test_produtos(token)
        
        if success:
            print("✅ Teste de produtos bem-sucedido!")
        else:
            print("❌ Falha no teste de produtos")
    else:
        print("❌ Falha no login - não é possível testar produtos protegidos")
        
        # Teste de produtos sem token para confirmar proteção
        print("\n2. Testando GET /produtos (sem autenticação)")
        test_produtos()
    
    print("\n=== Fim dos testes ===")