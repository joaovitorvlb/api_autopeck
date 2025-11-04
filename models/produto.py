class Produto:
    def __init__(self, id_produto, nome, descricao=None, preco=0.0, estoque=0):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque

    def __repr__(self):
        return (
            f"<Produto id={self.id_produto} nome='{self.nome}' descricao='{self.descricao}' "
            f"preco={self.preco} estoque={self.estoque}>"
        )

    def to_dict(self):
        return {
            'id_produto': self.id_produto,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'estoque': self.estoque,
        }
