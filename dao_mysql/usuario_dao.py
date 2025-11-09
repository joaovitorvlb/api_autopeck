from .db import get_cursor

class UsuarioDAO:
    """DAO para operações de leitura da tabela usuario"""
    
    def __init__(self):
        pass

    def listar_usuarios(self):
        """Lista todos os usuários com seus dados básicos (sem senha_hash)"""
        with get_cursor() as cur:
            cur.execute("""
                SELECT u.id_usuario, u.nome, u.email, u.telefone, u.ativo, 
                       u.data_criacao, u.id_nivel_acesso, n.nome as nivel_acesso_nome
                FROM usuario u
                INNER JOIN nivel_acesso n ON u.id_nivel_acesso = n.id_nivel_acesso
                ORDER BY u.nome;
            """)
            return cur.fetchall()

    def buscar_usuario(self, id_usuario):
        """Busca um usuário específico por ID (sem senha_hash)"""
        with get_cursor() as cur:
            cur.execute("""
                SELECT u.id_usuario, u.nome, u.email, u.telefone, u.ativo, 
                       u.data_criacao, u.id_nivel_acesso, n.nome as nivel_acesso_nome
                FROM usuario u
                INNER JOIN nivel_acesso n ON u.id_nivel_acesso = n.id_nivel_acesso
                WHERE u.id_usuario = %s;
            """, (id_usuario,))
            row = cur.fetchone()
            return row

    def buscar_usuario_por_email(self, email):
        """Busca um usuário específico por email (sem senha_hash)"""
        with get_cursor() as cur:
            cur.execute("""
                SELECT u.id_usuario, u.nome, u.email, u.telefone, u.ativo, 
                       u.data_criacao, u.id_nivel_acesso, n.nome as nivel_acesso_nome
                FROM usuario u
                INNER JOIN nivel_acesso n ON u.id_nivel_acesso = n.id_nivel_acesso
                WHERE u.email = %s;
            """, (email,))
            row = cur.fetchone()
            return row

    def listar_usuarios_por_nivel(self, id_nivel_acesso):
        """Lista todos os usuários de um nível de acesso específico"""
        with get_cursor() as cur:
            cur.execute("""
                SELECT u.id_usuario, u.nome, u.email, u.telefone, u.ativo, 
                       u.data_criacao, u.id_nivel_acesso, n.nome as nivel_acesso_nome
                FROM usuario u
                INNER JOIN nivel_acesso n ON u.id_nivel_acesso = n.id_nivel_acesso
                WHERE u.id_nivel_acesso = %s
                ORDER BY u.nome;
            """, (id_nivel_acesso,))
            return cur.fetchall()

    def listar_usuarios_ativos(self):
        """Lista apenas usuários ativos"""
        with get_cursor() as cur:
            cur.execute("""
                SELECT u.id_usuario, u.nome, u.email, u.telefone, u.ativo, 
                       u.data_criacao, u.id_nivel_acesso, n.nome as nivel_acesso_nome
                FROM usuario u
                INNER JOIN nivel_acesso n ON u.id_nivel_acesso = n.id_nivel_acesso
                WHERE u.ativo = 1
                ORDER BY u.nome;
            """)
            return cur.fetchall()
