class Cliente:
    def __init__(self, id_cliente, nome, email=None, telefone=None, endereco=None):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

    def __repr__(self):
        return (
            f"<Cliente id={self.id_cliente} nome='{self.nome}' email='{self.email}' "
            f"telefone='{self.telefone}' endereco='{self.endereco}'>"
        )

    def to_dict(self):
        return {
            'id_cliente': self.id_cliente,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': self.endereco,
        }
