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
import hashlib

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
            # 1. Criar tabelas se não existirem
            print("  🔧 Verificando/criando estrutura do banco...")
            
            # Criar tabela nivel_acesso
            cur.execute("""
                CREATE TABLE IF NOT EXISTS nivel_acesso (
                    id_nivel_acesso INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(50) NOT NULL UNIQUE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Criar tabela usuario
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    senha_hash VARCHAR(255) NOT NULL,
                    telefone VARCHAR(20),
                    ativo BOOLEAN DEFAULT 1,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    id_nivel_acesso INT NOT NULL,
                    CONSTRAINT fk_usuario_nivel
                        FOREIGN KEY (id_nivel_acesso) 
                        REFERENCES nivel_acesso(id_nivel_acesso)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Criar tabela Cliente
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Cliente (
                    id_cliente INT NOT NULL AUTO_INCREMENT,
                    nome VARCHAR(255) NOT NULL,
                    email VARCHAR(255),
                    telefone VARCHAR(20),
                    endereco TEXT,
                    PRIMARY KEY (id_cliente),
                    UNIQUE KEY unique_email (email),
                    KEY idx_cliente_email (email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Criar tabela Funcionario
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Funcionario (
                    id_funcionario INT NOT NULL AUTO_INCREMENT,
                    nome VARCHAR(255) NOT NULL,
                    cargo VARCHAR(100),
                    salario DECIMAL(10,2),
                    data_contratacao DATE,
                    PRIMARY KEY (id_funcionario)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Criar tabela Produto
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Produto (
                    id_produto INT NOT NULL AUTO_INCREMENT,
                    nome VARCHAR(255) NOT NULL,
                    descricao TEXT,
                    preco DECIMAL(10,2) NOT NULL,
                    estoque INT DEFAULT 0,
                    nome_imagem VARCHAR(255),
                    url VARCHAR(255),
                    PRIMARY KEY (id_produto)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Criar tabela Venda
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Venda (
                    id_venda INT NOT NULL AUTO_INCREMENT,
                    id_cliente INT,
                    id_funcionario INT,
                    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total DECIMAL(10,2) NOT NULL,
                    PRIMARY KEY (id_venda),
                    KEY idx_venda_cliente (id_cliente),
                    KEY idx_venda_funcionario (id_funcionario),
                    KEY idx_venda_data (data_venda),
                    CONSTRAINT fk_venda_cliente 
                        FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente) ON DELETE SET NULL,
                    CONSTRAINT fk_venda_funcionario 
                        FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Criar tabela Item_Venda
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Item_Venda (
                    id_item INT NOT NULL AUTO_INCREMENT,
                    id_venda INT NOT NULL,
                    id_produto INT NOT NULL,
                    quantidade INT NOT NULL DEFAULT 1,
                    preco_unitario DECIMAL(10,2) NOT NULL,
                    PRIMARY KEY (id_item),
                    KEY idx_item_venda (id_venda),
                    KEY idx_item_produto (id_produto),
                    CONSTRAINT fk_item_venda 
                        FOREIGN KEY (id_venda) REFERENCES Venda(id_venda) ON DELETE CASCADE,
                    CONSTRAINT fk_item_produto 
                        FOREIGN KEY (id_produto) REFERENCES Produto(id_produto) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            print("  ✅ Estrutura do banco verificada/criada")
            
            # 2. Limpar todas as tabelas (ordem importante por causa das FKs)
            print("  🗑️  Limpando dados das tabelas...")
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            cur.execute("TRUNCATE TABLE Item_Venda")
            cur.execute("TRUNCATE TABLE Venda")
            cur.execute("TRUNCATE TABLE Produto")
            cur.execute("TRUNCATE TABLE Cliente")
            cur.execute("TRUNCATE TABLE Funcionario")
            cur.execute("TRUNCATE TABLE usuario")
            cur.execute("TRUNCATE TABLE nivel_acesso")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")
            print("  ✅ Tabelas limpas")
            
            # 3. Inserir apenas dados padrão de nivel_acesso
            print("  📝 Inserindo dados padrão...")
            
            # Níveis de acesso (único dado padrão)
            cur.execute("""
                INSERT INTO nivel_acesso (nome) VALUES
                ('admin'),
                ('funcionario'),
                ('cliente')
            """)
            print("  ✅ Níveis de acesso inseridos")
            
            # Criar usuário admin padrão
            senha_padrao = "admin123"  # Senha padrão
            senha_hash = hashlib.sha256(senha_padrao.encode()).hexdigest()
            
            cur.execute("""
                INSERT INTO usuario (nome, email, senha_hash, telefone, ativo, id_nivel_acesso)
                VALUES ('Administrador', 'admin@autopeck.com', %s, '11999999999', 1, 
                        (SELECT id_nivel_acesso FROM nivel_acesso WHERE nome = 'admin'))
            """, (senha_hash,))
            print("  ✅ Usuário admin criado (email: admin@autopeck.com, senha: admin123)")
            print("  ⚠️  IMPORTANTE: Altere a senha do admin após o primeiro login!")
            print("  ℹ️  Todas as outras tabelas estão vazias")
        
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
            cur.execute("DELETE FROM usuario")
            cur.execute("DELETE FROM nivel_acesso")
            print("  ✅ Tabelas limpas")
            
            # 2. Resetar auto-increment
            cur.execute("DELETE FROM sqlite_sequence")
            
            # 3. Inserir apenas dados padrão de nivel_acesso
            print("  📝 Inserindo dados padrão...")
            
            cur.execute("""
                INSERT INTO nivel_acesso (nome) VALUES
                ('admin'),
                ('funcionario'),
                ('cliente')
            """)
            
            print("  ✅ Níveis de acesso inseridos")
            
            # Criar usuário admin padrão
            senha_padrao = "admin123"  # Senha padrão
            senha_hash = hashlib.sha256(senha_padrao.encode()).hexdigest()
            
            cur.execute("""
                INSERT INTO usuario (nome, email, senha_hash, telefone, ativo, id_nivel_acesso)
                VALUES ('Administrador', 'admin@autopeck.com', ?, '11999999999', 1, 
                        (SELECT id_nivel_acesso FROM nivel_acesso WHERE nome = 'admin'))
            """, (senha_hash,))
            
            print("  ✅ Usuário admin criado (email: admin@autopeck.com, senha: admin123)")
            print("  ⚠️  IMPORTANTE: Altere a senha do admin após o primeiro login!")
            print("  ℹ️  Todas as outras tabelas estão vazias")
        
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
