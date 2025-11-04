class ItemVenda:
    def __init__(self, id_item, id_venda, id_produto, quantidade, preco_unitario):
        self.id_item = id_item
        self.id_venda = id_venda
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    def __repr__(self):
        return (
            f"<ItemVenda id_item={self.id_item} id_venda={self.id_venda} "
            f"id_produto={self.id_produto} quantidade={self.quantidade} preco_unitario={self.preco_unitario}>"
        )

    def to_dict(self):
        return {
            'id_item': self.id_item,
            'id_venda': self.id_venda,
            'id_produto': self.id_produto,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
        }
