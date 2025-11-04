#!/usr/bin/env python3
"""
Exemplo de uso do DAO MySQL
"""

import sys
import os

# Adicionar o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dao_mysql.db import init_db, close_pool
from dao_mysql.cliente_dao import ClienteDAO
from dao_mysql.produto_dao import ProdutoDAO
from dao_mysql.funcionario_dao import FuncionarioDAO
from dao_mysql.venda_dao import VendaDAO
from dao_mysql.item_venda_dao import ItemVendaDAO

def exemplo_uso_mysql():
    """Demonstra o uso básico do DAO MySQL"""
    
    print("🔄 Inicializando conexão MySQL...")
    
    # Configuração do banco (ajuste conforme necessário)
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123456',  # Ajuste para sua senha
        'database': 'e_comerce_flask'  # Ajuste para seu banco
    }
    
    try:
        # Inicializar o banco
        init_db(db_config)
        print("✅ Conexão MySQL inicializada com sucesso!")
        
        # Exemplo com Cliente DAO
        print("\n📝 Testando Cliente DAO...")
        cliente_dao = ClienteDAO()
        
        # Listar clientes
        clientes = cliente_dao.listar_clientes()
        print(f"📋 Clientes encontrados: {len(clientes)}")
        for cliente in clientes:
            print(f"   - {cliente}")
        
        # Exemplo com Produto DAO
        print("\n🛍️ Testando Produto DAO...")
        produto_dao = ProdutoDAO()
        
        # Listar produtos
        produtos = produto_dao.listar_produtos()
        print(f"📋 Produtos encontrados: {len(produtos)}")
        for produto in produtos:
            print(f"   - {produto}")
        
        # Exemplo com Funcionario DAO
        print("\n👥 Testando Funcionario DAO...")
        funcionario_dao = FuncionarioDAO()
        
        # Listar funcionários
        funcionarios = funcionario_dao.listar_funcionarios()
        print(f"📋 Funcionários encontrados: {len(funcionarios)}")
        for funcionario in funcionarios:
            print(f"   - {funcionario}")
        
        print("\n✅ Todos os testes concluídos com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Fechar o pool de conexões
        close_pool()
        print("🔒 Pool de conexões fechado.")

if __name__ == "__main__":
    exemplo_uso_mysql()