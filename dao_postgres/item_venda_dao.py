from dao.db import get_cursor
from models.item_venda import ItemVenda

class ItemVendaDAO:
    def __init__(self):
        pass

    def listar_items_por_venda(self, id_venda):
        """Retorna lista de ItemVenda para uma venda."""
        with get_cursor() as cur:
            cur.execute(
                "SELECT id_item, id_venda, id_produto, quantidade, preco_unitario FROM Item_Venda WHERE id_venda = %s;",
                (id_venda,),
            )
            return [ItemVenda(*row) for row in cur.fetchall()]

    def add_item_to_venda(self, id_venda, id_produto, quantidade, preco_unitario, id_item=None):
        """
        Adiciona um item à venda dentro de uma transação:
        - verifica e bloqueia o estoque do produto (FOR UPDATE)
        - insere Item_Venda (gera id_item se None)
        - decrementa estoque do Produto
        - atualiza total da Venda
        """
        with get_cursor() as cur:
            # 1) bloquear produto e verificar estoque
            cur.execute("SELECT estoque FROM Produto WHERE id_produto = %s FOR UPDATE", (id_produto,))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Produto {id_produto} não encontrado")
            estoque = row[0]
            if estoque < quantidade:
                raise ValueError(f"Estoque insuficiente para o produto {id_produto}")

            # 2) gerar id_item simples se não fornecido (nota: pode ter corrida em alto concurrent)
            if id_item is None:
                cur.execute("SELECT COALESCE(MAX(id_item), 0) + 1 FROM Item_Venda")
                id_item = cur.fetchone()[0]

            # 3) inserir item
            cur.execute(
                "INSERT INTO Item_Venda (id_item, id_venda, id_produto, quantidade, preco_unitario) VALUES (%s, %s, %s, %s, %s)",
                (id_item, id_venda, id_produto, quantidade, preco_unitario),
            )

            # 4) decrementar estoque
            cur.execute("UPDATE Produto SET estoque = estoque - %s WHERE id_produto = %s", (quantidade, id_produto))

            # 5) atualizar total da venda
            cur.execute("UPDATE Venda SET total = COALESCE(total, 0) + %s WHERE id_venda = %s", (quantidade * preco_unitario, id_venda))

            return id_item

    def update_item_quantity(self, id_item, nova_quantidade):
        """
        Atualiza a quantidade de um item, ajustando estoque do produto e total da venda.
        """
        with get_cursor() as cur:
            # bloquear linha do item
            cur.execute("SELECT id_venda, id_produto, quantidade, preco_unitario FROM Item_Venda WHERE id_item = %s FOR UPDATE", (id_item,))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Item {id_item} não encontrado")
            id_venda, id_produto, quantidade_atual, preco_unitario = row

            diff = nova_quantidade - quantidade_atual
            if diff == 0:
                return

            # se precisa reduzir estoque (aumentar venda do item), bloquear produto e verificar
            if diff > 0:
                cur.execute("SELECT estoque FROM Produto WHERE id_produto = %s FOR UPDATE", (id_produto,))
                estoque = cur.fetchone()[0]
                if estoque < diff:
                    raise ValueError("Estoque insuficiente para aumentar a quantidade")

            # atualizar item
            cur.execute("UPDATE Item_Venda SET quantidade = %s WHERE id_item = %s", (nova_quantidade, id_item))

            # ajustar estoque (pode ser positivo ou negativo)
            cur.execute("UPDATE Produto SET estoque = estoque - %s WHERE id_produto = %s", (diff, id_produto))

            # ajustar total da venda
            cur.execute("UPDATE Venda SET total = COALESCE(total,0) + %s WHERE id_venda = %s", (diff * preco_unitario, id_venda))

    def remove_item(self, id_item):
        """
        Remove item e restitui estoque + ajusta total da venda.
        """
        with get_cursor() as cur:
            # obter e bloquear
            cur.execute("SELECT id_venda, id_produto, quantidade, preco_unitario FROM Item_Venda WHERE id_item = %s FOR UPDATE", (id_item,))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Item {id_item} não encontrado")
            id_venda, id_produto, quantidade, preco_unitario = row

            # deletar item
            cur.execute("DELETE FROM Item_Venda WHERE id_item = %s", (id_item,))

            # devolver estoque
            cur.execute("UPDATE Produto SET estoque = estoque + %s WHERE id_produto = %s", (quantidade, id_produto))

            # atualizar total da venda
            cur.execute("UPDATE Venda SET total = COALESCE(total,0) - %s WHERE id_venda = %s", (quantidade * preco_unitario, id_venda))

    def buscar_item(self, id_item):
        with get_cursor() as cur:
            cur.execute("SELECT id_item, id_venda, id_produto, quantidade, preco_unitario FROM Item_Venda WHERE id_item = %s", (id_item,))
            row = cur.fetchone()
            return ItemVenda(*row) if row else None

    def add_item_from_model(self, item: ItemVenda):
        """Convenience: adiciona ItemVenda a partir de um modelo ItemVenda"""
        return self.add_item_to_venda(item.id_venda, item.id_produto, item.quantidade, item.preco_unitario, id_item=item.id_item)
