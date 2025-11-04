from .db import get_cursor

class VendaDAO:
    def __init__(self):
        pass

    def listar_vendas(self):
        with get_cursor() as cur:
            cur.execute("SELECT id_venda, id_cliente, id_funcionario, data_venda, total FROM Venda;")
            return cur.fetchall()

    def inserir_venda(self, id_venda, id_cliente, id_funcionario, data_venda, total):
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO Venda (id_venda, id_cliente, id_funcionario, data_venda, total)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id_venda, id_cliente, id_funcionario, data_venda, total),
            )

    def buscar_venda(self, id_venda):
        with get_cursor() as cur:
            cur.execute(
                "SELECT id_venda, id_cliente, id_funcionario, data_venda, total FROM Venda WHERE id_venda = %s;",
                (id_venda,),
            )
            row = cur.fetchone()
            return row

    def atualizar_venda(self, id_venda, id_cliente, id_funcionario, data_venda, total):
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE Venda SET id_cliente = %s, id_funcionario = %s, data_venda = %s, total = %s
                WHERE id_venda = %s
                """,
                (id_cliente, id_funcionario, data_venda, total, id_venda),
            )

    def deletar_venda(self, id_venda):
        with get_cursor() as cur:
            cur.execute("DELETE FROM Venda WHERE id_venda = %s;", (id_venda,))

    def inserir_venda_obj(self, venda):
        return self.inserir_venda(
            venda.id_venda,
            venda.id_cliente,
            venda.id_funcionario,
            venda.data_venda,
            venda.total,
        )