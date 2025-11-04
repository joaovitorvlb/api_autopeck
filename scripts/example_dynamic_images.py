#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do sistema dinâmico de imagens
Demonstra como usar as novas funcionalidades da API
"""

import requests
import json
import os
from typing import Dict, Optional, List

class EcommerceImageClient:
    """Cliente para interagir com o sistema dinâmico de imagens da API"""
    
    def __init__(self, base_url="http://localhost:5001", token=None):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.session = requests.Session()
        
        if token:
            self.session.headers.update({'Authorization': f'Bearer {token}'})
    
    def criar_produto(self, nome: str, preco: float, estoque: int, descricao: str = "") -> Optional[Dict]:
        """Cria um novo produto"""
        url = f"{self.base_url}/produtos"
        data = {
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "estoque": estoque
        }
        
        try:
            response = self.session.post(url, json=data)
            if response.status_code == 201:
                resultado = response.json()
                print(f"✅ Produto criado: ID {resultado['id_produto']}")
                print(f"🖼️ Tem imagens: {resultado.get('tem_imagens', False)}")
                return resultado
            else:
                print(f"❌ Erro ao criar produto: {response.status_code}")
                print(f"📄 Resposta: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
    def fazer_upload_imagem(self, produto_id: int, caminho_imagem: str) -> Optional[Dict]:
        """Faz upload de uma imagem para um produto"""
        if not os.path.exists(caminho_imagem):
            print(f"❌ Arquivo não encontrado: {caminho_imagem}")
            return None
        
        url = f"{self.base_url}/produtos/{produto_id}/upload-image"
        
        try:
            with open(caminho_imagem, 'rb') as arquivo:
                files = {
                    'image': (
                        os.path.basename(caminho_imagem),
                        arquivo,
                        'image/jpeg'
                    )
                }
                
                response = self.session.post(url, files=files)
                
                if response.status_code == 200:
                    resultado = response.json()
                    print(f"✅ Upload realizado com sucesso!")
                    print(f"📁 Total de arquivos criados: {resultado['total_arquivos']}")
                    print(f"🖼️ Resoluções disponíveis:")
                    for resolucao, url_imagem in resultado['resolutions'].items():
                        print(f"   - {resolucao}: {url_imagem}")
                    return resultado
                else:
                    print(f"❌ Erro no upload: {response.status_code}")
                    print(f"📄 Resposta: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"❌ Erro no upload: {e}")
            return None
    
    def obter_urls_imagens(self, produto_id: int) -> Optional[Dict]:
        """Obtém todas as URLs de imagens de um produto de forma dinâmica"""
        url = f"{self.base_url}/produtos/{produto_id}/images"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                resultado = response.json()
                print(f"🖼️ Produto: {resultado['nome_produto']}")
                print(f"📊 Imagens disponíveis: {resultado['imagens_disponiveis']}")
                
                if resultado['urls']:
                    print(f"🔗 URLs dinâmicas:")
                    for resolucao, url_imagem in resultado['urls'].items():
                        print(f"   - {resolucao}: {url_imagem}")
                else:
                    print("📭 Nenhuma imagem encontrada")
                
                return resultado
            else:
                print(f"❌ Erro ao obter URLs: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
    def listar_produtos(self) -> Optional[List[Dict]]:
        """Lista todos os produtos com URLs dinâmicas"""
        url = f"{self.base_url}/produtos"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                produtos = response.json()
                print(f"📋 Total de produtos: {len(produtos)}")
                
                for produto in produtos:
                    print(f"\n🏷️ {produto['nome']} (ID: {produto['id_produto']})")
                    print(f"   💰 Preço: R$ {produto['preco']}")
                    print(f"   📦 Estoque: {produto['estoque']}")
                    print(f"   🖼️ Tem imagens: {'Sim' if produto.get('tem_imagens') else 'Não'}")
                    
                    if produto.get('urls_imagem'):
                        print(f"   🔗 Resoluções: {', '.join(produto['urls_imagem'].keys())}")
                
                return produtos
            else:
                print(f"❌ Erro ao listar produtos: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
    def scan_sistema_imagens(self) -> Optional[Dict]:
        """Faz um scan completo do sistema de imagens"""
        url = f"{self.base_url}/admin/images/scan"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                resultado = response.json()
                print(f"🔍 Scan do sistema de imagens:")
                print(f"📊 Total de arquivos: {resultado['total_arquivos']}")
                print(f"🏷️ Produtos com imagens: {resultado['produtos_com_imagens']}")
                
                print(f"\n📋 Resumo por produto:")
                for produto_id, total in resultado['resumo_por_produto'].items():
                    print(f"   - Produto {produto_id}: {total} arquivos")
                
                return resultado
            else:
                print(f"❌ Erro no scan: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
    def remover_imagens_produto(self, produto_id: int) -> bool:
        """Remove todas as imagens de um produto"""
        url = f"{self.base_url}/produtos/{produto_id}/remove-image"
        
        try:
            response = self.session.delete(url)
            if response.status_code == 200:
                resultado = response.json()
                print(f"🗑️ Imagens removidas com sucesso!")
                print(f"📊 Total removido: {resultado['total_removidos']}")
                print(f"📁 Arquivos: {', '.join(resultado['arquivos_removidos'])}")
                return True
            else:
                print(f"❌ Erro ao remover: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return False


def exemplo_uso_completo():
    """Exemplo de uso completo do sistema dinâmico"""
    print("🚀 Demonstração do Sistema Dinâmico de Imagens\n")
    
    # Fazer login primeiro (se necessário)
    client = EcommerceImageClient()
    
    # 1. Criar um produto
    print("1️⃣ Criando produto...")
    produto = client.criar_produto(
        nome="Mouse Gamer RGB",
        preco=149.90,
        estoque=25,
        descricao="Mouse gamer com iluminação RGB"
    )
    
    if not produto:
        print("❌ Falha ao criar produto. Abortando...")
        return
    
    produto_id = produto['id_produto']
    
    # 2. Fazer upload de imagem (substitua pelo caminho real)
    print(f"\n2️⃣ Fazendo upload de imagem para produto {produto_id}...")
    caminho_imagem = "/path/to/your/image.jpg"  # SUBSTITUA AQUI
    
    if os.path.exists(caminho_imagem):
        upload_result = client.fazer_upload_imagem(produto_id, caminho_imagem)
    else:
        print(f"⚠️ Arquivo {caminho_imagem} não encontrado. Pulando upload...")
        upload_result = None
    
    # 3. Obter URLs dinâmicas
    print(f"\n3️⃣ Obtendo URLs dinâmicas do produto {produto_id}...")
    urls = client.obter_urls_imagens(produto_id)
    
    # 4. Listar todos os produtos
    print(f"\n4️⃣ Listando todos os produtos...")
    produtos = client.listar_produtos()
    
    # 5. Scan do sistema
    print(f"\n5️⃣ Fazendo scan do sistema...")
    scan = client.scan_sistema_imagens()
    
    print(f"\n✅ Demonstração concluída!")


if __name__ == "__main__":
    exemplo_uso_completo()