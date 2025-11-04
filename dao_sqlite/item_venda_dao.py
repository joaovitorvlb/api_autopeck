from .db import get_cursor

class ItemVendaDAO:
    def listar_items_por_venda(self, id_venda):
        with get_cursor() as cur:
            cur.execute("SELECT id_item, id_venda, id_produto, quantidade, preco_unitario FROM Item_Venda WHERE id_venda = ?;", (id_venda,))
            return [dict(row) for row in cur.fetchall()]

    def inserir_item(self, id_item, id_venda, id_produto, quantidade, preco_unitario):
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO Item_Venda (id_item, id_venda, id_produto, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?, ?)
                """,
                (id_item, id_venda, id_produto, quantidade, preco_unitario),
            )

    def buscar_item(self, id_item):
        with get_cursor() as cur:
            cur.execute(
                "SELECT id_item, id_venda, id_produto, quantidade, preco_unitario FROM Item_Venda WHERE id_item = ?;",
                (id_item,),
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def atualizar_item(self, id_item, quantidade, preco_unitario):
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE Item_Venda SET quantidade = ?, preco_unitario = ?
                WHERE id_item = ?
                """,
                (quantidade, preco_unitario, id_item),
            )

    def deletar_item(self, id_item):
        with get_cursor() as cur:
            cur.execute("DELETE FROM Item_Venda WHERE id_item = ?;", (id_item,))

    def inserir_item_obj(self, item):
        return self.inserir_item(
            item.id_item,
            item.id_venda,
            item.id_produto,
            item.quantidade,
            item.preco_unitario,
        )
