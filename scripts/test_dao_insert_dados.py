#!/usr/bin/env python3
"""
Script para inserir dados de teste no banco SQLite usando os DAOs.
Insere funcionários, clientes e produtos para testar os SELECTs.
Não insere vendas nem itens de venda.
"""
import sys
import os

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao_sqlite.db import init_db, close_pool
from dao_sqlite.funcionario_dao import FuncionarioDAO
from dao_sqlite.cliente_dao import ClienteDAO
from dao_sqlite.produto_dao import ProdutoDAO
from dao_sqlite.venda_dao import VendaDAO

def main():
    print("=" * 60)
    print("TESTE DE INSERÇÃO - SQLite")
    print("=" * 60)
    
    # Inicializar banco
    init_db({'database': 'banco_api.sqlite'})
    print("✓ Banco SQLite inicializado\n")
    
    # DAOs
    dao_func = FuncionarioDAO()
    dao_cli = ClienteDAO()
    dao_prod = ProdutoDAO()
    
    # ============================================
    # INSERIR FUNCIONÁRIOS
    # ============================================
    print("📝 Inserindo Funcionários...")
    funcionarios = [
        (1, 'João Silva', 'Gerente', 5000.00, '2022-01-15'),
        (2, 'Maria Oliveira', 'Vendedor', 3000.00, '2022-03-22'),
        (3, 'Carlos Santos', 'Vendedor', 3200.00, '2023-05-10'),
        (4, 'Ana Costa', 'Supervisor', 4500.00, '2021-11-05'),
    ]
    
    for f in funcionarios:
        try:
            dao_func.inserir_funcionario(*f)
            print(f"  ✓ Inserido: {f[1]} ({f[2]})")
        except Exception as e:
            print(f"  ✗ Erro ao inserir {f[1]}: {e}")
    
    # ============================================
    # INSERIR CLIENTES
    # ============================================
    print("\n📝 Inserindo Clientes...")
    clientes = [
        (1, 'Ana Souza', 'ana.souza@example.com', '+55 11 99999-0001', 'Rua das Flores, 123, São Paulo, SP'),
        (2, 'Carlos Pereira', 'carlos.pereira@example.com', '+55 21 98888-0002', 'Av. Brasil, 456, Rio de Janeiro, RJ'),
        (3, 'Mariana Costa', 'mariana.costa@example.com', '+55 31 97777-0003', 'Praça Sete, 789, Belo Horizonte, MG'),
        (4, 'Roberto Lima', 'roberto.lima@example.com', '+55 41 96666-0004', 'Rua XV de Novembro, 101, Curitiba, PR'),
        (5, 'Luciana Ramos', 'luciana.ramos@example.com', '+55 51 95555-0005', 'Av. Ipiranga, 202, Porto Alegre, RS'),
    ]
    
    for c in clientes:
        try:
            dao_cli.inserir_cliente(*c)
            print(f"  ✓ Inserido: {c[1]} ({c[2]})")
        except Exception as e:
            print(f"  ✗ Erro ao inserir {c[1]}: {e}")
    
    # ============================================
    # INSERIR PRODUTOS
    # ============================================
    print("\n📝 Inserindo Produtos...")
    
    # Obter URL base do servidor local
    base_url = "http://192.168.1.100:5000"  # Ajuste para seu IP
    
    produtos = [
        (1, 'Filtro de Óleo', 'Filtro de óleo para motores 1.0 a 2.0', 29.90, 100, f'{base_url}/images/produtos/filtro-oleo.jpg'),
        (2, 'Pastilha de Freio', 'Jogo de pastilhas de freio dianteiro', 89.90, 50, f'{base_url}/images/produtos/pastilha-freio.jpg'),
        (3, 'Amortecedor', 'Amortecedor dianteiro universal', 199.90, 30, f'{base_url}/images/produtos/amortecedor.jpg'),
        (4, 'Correia Dentada', 'Correia de distribuição para motores flex', 45.90, 80, f'{base_url}/images/produtos/correia-dentada.jpg'),
        (5, 'Vela de Ignição', 'Jogo com 4 velas de ignição', 69.90, 60, f'{base_url}/images/produtos/vela-ignicao.jpg'),
        (6, 'Óleo de Motor', 'Óleo sintético 5W30 1L', 35.90, 150, f'{base_url}/images/produtos/oleo-motor.jpg'),
        (7, 'Bateria Automotiva', 'Bateria 60Ah', 359.90, 25, f'{base_url}/images/produtos/bateria.jpg'),
        (8, 'Filtro de Ar', 'Filtro de ar motor 1.0 a 2.0', 25.90, 90, f'{base_url}/images/produtos/filtro-ar.jpg'),
        (9, 'Radiador', 'Radiador de água universal', 299.90, 20, f'{base_url}/images/produtos/radiador.jpg'),
        (10, 'Kit Embreagem', 'Kit completo de embreagem', 459.90, 15, f'{base_url}/images/produtos/kit-embreagem.jpg'),
    ]
    
    for p in produtos:
        try:
            dao_prod.inserir_produto(*p)
            print(f"  ✓ Inserido: {p[1]} - R$ {p[3]:.2f} (estoque: {p[4]})")
            print(f"    🖼️  URL: {p[5]}")
        except Exception as e:
            print(f"  ✗ Erro ao inserir {p[1]}: {e}")
    
    # ============================================
    # TESTAR SELECTS
    # ============================================
    print("\n" + "=" * 60)
    print("📊 TESTANDO SELECTS")
    print("=" * 60)
    
    print("\n🧑‍💼 Funcionários cadastrados:")
    funcionarios_db = dao_func.listar_funcionarios()
    for func in funcionarios_db:
        print(f"  [{func['id_funcionario']}] {func['nome']} - {func['cargo']} - R$ {func['salario']}")
    
    print(f"\n👥 Clientes cadastrados: {len(dao_cli.listar_clientes())} registros")
    for cli in dao_cli.listar_clientes()[:3]:  # Mostrar apenas 3
        print(f"  [{cli['id_cliente']}] {cli['nome']} - {cli['email']}")
    
    print(f"\n📦 Produtos cadastrados: {len(dao_prod.listar_produtos())} registros")
    for prod in dao_prod.listar_produtos()[:5]:  # Mostrar apenas 5
        print(f"  [{prod['id_produto']}] {prod['nome']} - R$ {prod['preco']:.2f}")
    
    # ============================================
    # TESTAR BUSCA POR ID
    # ============================================
    print("\n" + "=" * 60)
    print("🔍 TESTANDO BUSCA POR ID")
    print("=" * 60)
    
    func = dao_func.buscar_funcionario(1)
    if func:
        print(f"\n✓ Funcionário ID 1: {func['nome']} ({func['cargo']})")
    
    cli = dao_cli.buscar_cliente(2)
    if cli:
        print(f"✓ Cliente ID 2: {cli['nome']} ({cli['email']})")
    
    prod = dao_prod.buscar_produto(3)
    if prod:
        print(f"✓ Produto ID 3: {prod['nome']} - R$ {prod['preco']:.2f}")
    
    # Fechar pool
    print("\n" + "=" * 60)
    close_pool()
    print("✓ Pool fechado. Testes concluídos!")
    print("=" * 60)

if __name__ == "__main__":
    main()
