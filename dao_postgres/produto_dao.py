from dao.db import get_cursor
from models.produto import Produto

class ProdutoDAO:
    def __init__(self):
        pass

    def listar_produtos(self):
        with get_cursor() as cur:
            cur.execute("SELECT id_produto, nome, descricao, preco, estoque FROM Produto;")
            return [Produto(*row) for row in cur.fetchall()]

    def inserir_produto(self, id_produto, nome, descricao=None, preco=0.0, estoque=0):
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO Produto (id_produto, nome, descricao, preco, estoque)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id_produto, nome, descricao, preco, estoque),
            )

    def buscar_produto(self, id_produto):
        with get_cursor() as cur:
            cur.execute(
                "SELECT id_produto, nome, descricao, preco, estoque FROM Produto WHERE id_produto = %s;",
                (id_produto,),
            )
            row = cur.fetchone()
            return Produto(*row) if row else None

    def atualizar_produto(self, id_produto, nome, descricao=None, preco=0.0, estoque=0):
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE Produto SET nome = %s, descricao = %s, preco = %s, estoque = %s
                WHERE id_produto = %s
                """,
                (nome, descricao, preco, estoque, id_produto),
            )

    def deletar_produto(self, id_produto):
        with get_cursor() as cur:
            cur.execute("DELETE FROM Produto WHERE id_produto = %s;", (id_produto,))

    def inserir_produto_obj(self, produto: Produto):
        """Convenience: insere usando um modelo Produto"""
        return self.inserir_produto(
            produto.id_produto,
            produto.nome,
            produto.descricao,
            produto.preco,
            produto.estoque,
        )
