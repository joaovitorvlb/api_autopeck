#!/usr/bin/env python3
"""
Teste específico para debug do timeout na listagem de produtos
"""

import requests
import time

BASE_URL = "http://localhost:5001"

def test_login():
    """Faz login e retorna token"""
    print("🔐 Fazendo login...")
    start_time = time.time()
    
    login_data = {"usuario": "admin", "senha": "admin"}
    response = requests.post(f"{BASE_URL}/login", json=login_data, timeout=30)
    
    end_time = time.time()
    print(f"⏱️ Login levou {end_time - start_time:.2f} segundos")
    
    if response.status_code == 200:
        token = response.json().get('token')
        print(f"✅ Login OK - Token: {token[:30]}...")
        return token
    else:
        print(f"❌ Login falhou: {response.status_code}")
        return None

def test_produtos_com_timeout(token):
    """Testa listagem de produtos com timeout maior"""
    print("\n📋 Testando listagem de produtos...")
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = time.time()
    
    try:
        # Timeout maior para debug
        response = requests.get(f"{BASE_URL}/produtos", headers=headers, timeout=60)
        end_time = time.time()
        
        print(f"⏱️ Listagem levou {end_time - start_time:.2f} segundos")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            produtos = response.json()
            print(f"✅ Sucesso! Encontrados {len(produtos)} produtos")
            
            # Mostrar primeiro produto como exemplo
            if produtos:
                primeiro = produtos[0]
                print(f"📦 Primeiro produto: {primeiro.get('nome', 'N/A')}")
                print(f"🖼️ URLs de imagem: {primeiro.get('urls_imagem', 'Nenhuma')}")
            
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"📝 Resposta: {response.text[:200]}...")
            return False
            
    except requests.exceptions.Timeout:
        end_time = time.time()
        print(f"⏱️ TIMEOUT após {end_time - start_time:.2f} segundos")
        print("❌ Servidor não respondeu a tempo")
        return False
    except Exception as e:
        end_time = time.time()
        print(f"⏱️ Erro após {end_time - start_time:.2f} segundos")
        print(f"❌ Erro: {e}")
        return False

def test_health():
    """Testa se servidor está respondendo"""
    print("🏥 Testando saúde do servidor...")
    
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/", timeout=10)
        end_time = time.time()
        
        print(f"⏱️ Health check levou {end_time - start_time:.2f} segundos")
        print(f"📊 Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Servidor não responde: {e}")
        return False

def main():
    print("🔍 DIAGNÓSTICO DE TIMEOUT - Listagem de Produtos")
    print("=" * 60)
    
    # 1. Testar saúde do servidor
    if not test_health():
        print("💥 Servidor não está respondendo - verifique se está rodando")
        return
    
    # 2. Fazer login
    token = test_login()
    if not token:
        print("💥 Não foi possível fazer login")
        return
    
    # 3. Testar listagem com timeout maior
    success = test_produtos_com_timeout(token)
    
    if success:
        print("\n🎉 SUCESSO! O problema pode ter sido timeout muito baixo")
        print("💡 Sugestão: Aumentar timeout no cliente Tkinter")
    else:
        print("\n💥 PROBLEMA CONFIRMADO!")
        print("💡 Verifique logs do servidor Flask para mais detalhes")
        print("💡 Possíveis causas:")
        print("   - Consulta lenta no banco de dados")
        print("   - Processamento de imagens demorado") 
        print("   - Loop infinito no código")
        print("   - Deadlock na conexão do banco")

if __name__ == "__main__":
    main()