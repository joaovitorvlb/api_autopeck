from .db import get_cursor

class NivelAcessoDAO:
    """DAO para operações de leitura da tabela nivel_acesso"""
    
    def __init__(self):
        pass

    def listar_niveis_acesso(self):
        """Lista todos os níveis de acesso disponíveis"""
        with get_cursor() as cur:
            cur.execute("SELECT id_nivel_acesso, nome FROM nivel_acesso ORDER BY nome;")
            return cur.fetchall()

    def buscar_nivel_acesso(self, id_nivel_acesso):
        """Busca um nível de acesso específico por ID"""
        with get_cursor() as cur:
            cur.execute(
                "SELECT id_nivel_acesso, nome FROM nivel_acesso WHERE id_nivel_acesso = %s;",
                (id_nivel_acesso,),
            )
            row = cur.fetchone()
            return row

    def buscar_nivel_acesso_por_nome(self, nome):
        """Busca um nível de acesso específico por nome"""
        with get_cursor() as cur:
            cur.execute(
                "SELECT id_nivel_acesso, nome FROM nivel_acesso WHERE nome = %s;",
                (nome,),
            )
            row = cur.fetchone()
            return row
