from .db import get_cursor

class ClienteDAO:
    def listar_clientes(self):
        with get_cursor() as cur:
            cur.execute("SELECT id_cliente, nome, email, telefone, endereco FROM Cliente;")
            return [dict(row) for row in cur.fetchall()]

    def inserir_cliente(self, id_cliente, nome, email, telefone, endereco):
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO Cliente (id_cliente, nome, email, telefone, endereco)
                VALUES (?, ?, ?, ?, ?)
                """,
                (id_cliente, nome, email, telefone, endereco),
            )

    def buscar_cliente(self, id_cliente):
        with get_cursor() as cur:
            cur.execute(
                "SELECT id_cliente, nome, email, telefone, endereco FROM Cliente WHERE id_cliente = ?;",
                (id_cliente,),
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def atualizar_cliente(self, id_cliente, nome, email, telefone, endereco):
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE Cliente SET nome = ?, email = ?, telefone = ?, endereco = ?
                WHERE id_cliente = ?
                """,
                (nome, email, telefone, endereco, id_cliente),
            )

    def deletar_cliente(self, id_cliente):
        with get_cursor() as cur:
            cur.execute("DELETE FROM Cliente WHERE id_cliente = ?;", (id_cliente,))

    def inserir_cliente_obj(self, cliente):
        return self.inserir_cliente(
            cliente.id_cliente,
            cliente.nome,
            cliente.email,
            cliente.telefone,
            cliente.endereco,
        )
