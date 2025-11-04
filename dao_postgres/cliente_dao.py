from dao.db import get_cursor
from models.cliente import Cliente

class ClienteDAO:
    def __init__(self):
        pass

    def listar_clientes(self):
        with get_cursor() as cur:
            cur.execute("SELECT id_cliente, nome, email, telefone, endereco FROM Cliente;")
            return [Cliente(*row) for row in cur.fetchall()]

    def inserir_cliente(self, id_cliente, nome, email=None, telefone=None, endereco=None):
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO Cliente (id_cliente, nome, email, telefone, endereco)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id_cliente, nome, email, telefone, endereco),
            )

    def buscar_cliente(self, id_cliente):
        with get_cursor() as cur:
            cur.execute(
                "SELECT id_cliente, nome, email, telefone, endereco FROM Cliente WHERE id_cliente = %s;",
                (id_cliente,),
            )
            row = cur.fetchone()
            return Cliente(*row) if row else None

    def atualizar_cliente(self, id_cliente, nome, email=None, telefone=None, endereco=None):
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE Cliente SET nome = %s, email = %s, telefone = %s, endereco = %s
                WHERE id_cliente = %s
                """,
                (nome, email, telefone, endereco, id_cliente),
            )

    def deletar_cliente(self, id_cliente):
        with get_cursor() as cur:
            cur.execute("DELETE FROM Cliente WHERE id_cliente = %s;", (id_cliente,))

    def inserir_cliente_obj(self, cliente: Cliente):
        """Convenience: insere usando um modelo Cliente"""
        return self.inserir_cliente(
            cliente.id_cliente,
            cliente.nome,
            cliente.email,
            cliente.telefone,
            cliente.endereco,
        )
