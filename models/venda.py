class Venda:
    def __init__(self, id_venda, id_cliente, id_funcionario, data_venda, total):
        self.id_venda = id_venda
        self.id_cliente = id_cliente
        self.id_funcionario = id_funcionario
        self.data_venda = data_venda
        self.total = total

    def __repr__(self):
        return (
            f"<Venda id={self.id_venda} id_cliente={self.id_cliente} "
            f"id_funcionario={self.id_funcionario} data_venda={self.data_venda} total={self.total}>"
        )

    def to_dict(self):
        return {
            'id_venda': self.id_venda,
            'id_cliente': self.id_cliente,
            'id_funcionario': self.id_funcionario,
            'data_venda': self.data_venda,
            'total': self.total,
        }
