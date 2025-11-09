#!/usr/bin/env python3
"""
Script para limpar dados de teste no PythonAnywhere
Uso: python scripts/limpar_producao.py

ATENÇÃO: Este script irá:
1. Remover todas as imagens de produtos (exceto README.md)
2. Limpar dados de teste das tabelas
3. Inserir dados padrão iniciais

Execute apenas em ambiente de produção após testes!
"""

import os
import sys

# Adicionar o diretório raiz ao path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

# Carregar variáveis de ambiente do arquivo .env
def load_env_file(env_path):
    """Carrega variáveis de ambiente de um arquivo .env"""
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove aspas se existirem
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value
        print(f"✅ Variáveis de ambiente carregadas de {env_path}")
    else:
        print(f"⚠️  Arquivo .env não encontrado em {env_path}")

# Carregar .env
env_file = os.path.join(BASE_DIR, '.env')
load_env_file(env_file)

def limpar_imagens():
    """Remove todas as imagens de teste do diretório de uploads"""
    print("\n🗑️  Limpando imagens de teste...")
    
    # Caminho absoluto para o diretório de imagens
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    upload_folder = os.path.join(BASE_DIR, 'static', 'images', 'produtos')
    
    if not os.path.exists(upload_folder):
        print(f"⚠️  Diretório não encontrado: {upload_folder}")
        return
    
    removidos = 0
    erros = 0
    
    for filename in os.listdir(upload_folder):
        # Não remover README.md
        if filename == 'README.md':
            continue
        
        filepath = os.path.join(upload_folder, filename)
        
        try:
            if os.path.isfile(filepath):
                os.remove(filepath)
                print(f"  ✅ Removido: {filename}")
                removidos += 1
        except Exception as e:
            print(f"  ❌ Erro ao remover {filename}: {e}")
            erros += 1
    
    print(f"\n📊 Resultado:")
    print(f"  - Arquivos removidos: {removidos}")
    print(f"  - Erros: {erros}")

def resetar_banco_mysql():
    """Reseta o banco de dados MySQL para estado padrão"""
    print("\n🗄️  Resetando banco de dados MySQL...")
    
    try:
        # Carregar variáveis de ambiente do .env (necessário para scripts locais)
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        value = value.strip().strip('"').strip("'")
                        os.environ[key] = value
            print("  ✅ Variáveis de ambiente carregadas do .env")
        
        # Tentar importar DAO do MySQL
        from dao_mysql.db_pythonanywhere import init_db, get_cursor
        
        # Inicializar banco
        init_db()
        
        print("  🔗 Conectado ao MySQL")
        
        with get_cursor() as cur:
            # 1. Limpar todas as tabelas (ordem importante por causa das FKs)
            print("  🗑️  Limpando tabelas...")
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            cur.execute("TRUNCATE TABLE Item_Venda")
            cur.execute("TRUNCATE TABLE Venda")
            cur.execute("TRUNCATE TABLE Produto")
            cur.execute("TRUNCATE TABLE Cliente")
            cur.execute("TRUNCATE TABLE Funcionario")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")
            print("  ✅ Tabelas limpas")
            
            # 2. Inserir dados padrão
            print("  📝 Inserindo dados padrão...")
            
            # Funcionários (para login)
            cur.execute("""
                INSERT INTO Funcionario (nome, cargo, salario, data_contratacao) VALUES
                ('Maria Silva', 'Vendedora', 2500.00, '2023-01-15'),
                ('Admin Sistema', 'Administrador', 4500.00, '2022-06-10'),
                ('Carlos Lima', 'Gerente', 3500.00, '2023-03-20')
            """)
            print("  ✅ Funcionários inseridos")
            
            # Clientes iniciais
            cur.execute("""
                INSERT INTO Cliente (nome, email, telefone, endereco) VALUES
                ('João Silva', 'joao@email.com', '11999999999', 'Rua A, 123'),
                ('Ana Santos', 'ana@email.com', '11888888888', 'Rua B, 456'),
                ('Pedro Oliveira', 'pedro@email.com', '11777777777', 'Rua C, 789')
            """)
            print("  ✅ Clientes inseridos")
            
            # Produtos padrão (AutoPeças)
            cur.execute("""
                INSERT INTO Produto (nome, descricao, preco, estoque, nome_imagem) VALUES
                ('Filtro de Óleo', 'Filtro de óleo para motores 1.0 a 2.0', 29.90, 100, NULL),
                ('Pastilha de Freio', 'Jogo de pastilhas de freio dianteiro', 89.90, 50, NULL),
                ('Amortecedor Dianteiro', 'Amortecedor dianteiro para carros populares', 189.90, 30, NULL),
                ('Vela de Ignição', 'Jogo de velas de ignição NGK', 45.90, 80, NULL),
                ('Correia Dentada', 'Correia dentada para motores 1.0/1.4/1.6', 65.90, 25, NULL)
            """)
            print("  ✅ Produtos inseridos")
        
        print("\n✅ Banco de dados resetado com sucesso!")
        return True
        
    except ImportError:
        print("  ⚠️  DAO MySQL não disponível. Tentando SQLite...")
        return resetar_banco_sqlite()
    except Exception as e:
        print(f"  ❌ Erro ao resetar banco MySQL: {e}")
        return False

def resetar_banco_sqlite():
    """Reseta o banco de dados SQLite para estado padrão"""
    print("\n🗄️  Resetando banco de dados SQLite...")
    
    try:
        from dao_sqlite.db import init_db, get_cursor
        
        # Inicializar banco
        init_db()
        
        print("  🔗 Conectado ao SQLite")
        
        with get_cursor() as cur:
            # 1. Limpar todas as tabelas
            print("  🗑️  Limpando tabelas...")
            cur.execute("DELETE FROM Item_Venda")
            cur.execute("DELETE FROM Venda")
            cur.execute("DELETE FROM Produto")
            cur.execute("DELETE FROM Cliente")
            cur.execute("DELETE FROM Funcionario")
            print("  ✅ Tabelas limpas")
            
            # 2. Resetar auto-increment
            cur.execute("DELETE FROM sqlite_sequence")
            
            # 3. Inserir dados padrão (mesmo que MySQL)
            print("  📝 Inserindo dados padrão...")
            
            cur.execute("""
                INSERT INTO Funcionario (nome, cargo, salario, data_contratacao) VALUES
                ('Maria Silva', 'Vendedora', 2500.00, '2023-01-15'),
                ('Admin Sistema', 'Administrador', 4500.00, '2022-06-10'),
                ('Carlos Lima', 'Gerente', 3500.00, '2023-03-20')
            """)
            
            cur.execute("""
                INSERT INTO Cliente (nome, email, telefone, endereco) VALUES
                ('João Silva', 'joao@email.com', '11999999999', 'Rua A, 123'),
                ('Ana Santos', 'ana@email.com', '11888888888', 'Rua B, 456'),
                ('Pedro Oliveira', 'pedro@email.com', '11777777777', 'Rua C, 789')
            """)
            
            cur.execute("""
                INSERT INTO Produto (nome, descricao, preco, estoque, nome_imagem) VALUES
                ('Filtro de Óleo', 'Filtro de óleo para motores 1.0 a 2.0', 29.90, 100, NULL),
                ('Pastilha de Freio', 'Jogo de pastilhas de freio dianteiro', 89.90, 50, NULL),
                ('Amortecedor Dianteiro', 'Amortecedor dianteiro para carros populares', 189.90, 30, NULL),
                ('Vela de Ignição', 'Jogo de velas de ignição NGK', 45.90, 80, NULL),
                ('Correia Dentada', 'Correia dentada para motores 1.0/1.4/1.6', 65.90, 25, NULL)
            """)
            
            print("  ✅ Dados padrão inseridos")
        
        print("\n✅ Banco de dados resetado com sucesso!")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao resetar banco SQLite: {e}")
        return False

def confirmar_acao():
    """Solicita confirmação do usuário antes de executar"""
    print("\n" + "="*60)
    print("⚠️  ATENÇÃO: OPERAÇÃO DESTRUTIVA ⚠️")
    print("="*60)
    print("\nEste script irá:")
    print("  1. ❌ Remover TODAS as imagens de produtos")
    print("  2. ❌ Apagar TODOS os dados de teste do banco")
    print("  3. ✅ Inserir apenas dados padrão iniciais")
    print("\n⚠️  Esta ação NÃO PODE SER DESFEITA!")
    print("="*60)
    
    resposta = input("\nDeseja continuar? Digite 'SIM' para confirmar: ")
    
    return resposta.strip().upper() == 'SIM'

def main():
    """Função principal"""
    print("\n🧹 Script de Limpeza - Ambiente de Produção")
    print("="*60)
    
    # Confirmar ação
    if not confirmar_acao():
        print("\n❌ Operação cancelada pelo usuário.")
        print("   Nenhuma alteração foi feita.")
        sys.exit(0)
    
    print("\n🚀 Iniciando limpeza...")
    
    # 1. Limpar imagens
    limpar_imagens()
    
    # 2. Resetar banco
    sucesso = resetar_banco_mysql()
    
    if sucesso:
        print("\n" + "="*60)
        print("✅ LIMPEZA CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print("\n📋 Próximos passos:")
        print("  1. Fazer reload da aplicação no PythonAnywhere")
        print("  2. Testar login com usuários padrão")
        print("  3. Verificar se produtos estão listando corretamente")
        print("\n💡 Usuários disponíveis para login:")
        print("  - maria / senha: (a definir no sistema)")
        print("  - admin / senha: (a definir no sistema)")
        print("\n")
    else:
        print("\n❌ Erro durante a limpeza.")
        print("   Verifique os logs acima para mais detalhes.")
        sys.exit(1)

if __name__ == "__main__":
    main()
