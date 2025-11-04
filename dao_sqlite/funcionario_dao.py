from .db import get_cursor

class FuncionarioDAO:
    def listar_funcionarios(self):
        with get_cursor() as cur:
            cur.execute("SELECT id_funcionario, nome, cargo, salario, data_contratacao FROM Funcionario;")
            return [dict(row) for row in cur.fetchall()]

    def inserir_funcionario(self, id_funcionario, nome, cargo, salario, data_contratacao):
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO Funcionario (id_funcionario, nome, cargo, salario, data_contratacao)
                VALUES (?, ?, ?, ?, ?)
                """,
                (id_funcionario, nome, cargo, salario, data_contratacao),
            )

    def buscar_funcionario(self, id_funcionario):
        with get_cursor() as cur:
            cur.execute(
                "SELECT id_funcionario, nome, cargo, salario, data_contratacao FROM Funcionario WHERE id_funcionario = ?;",
                (id_funcionario,),
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def atualizar_funcionario(self, id_funcionario, nome, cargo, salario, data_contratacao):
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE Funcionario SET nome = ?, cargo = ?, salario = ?, data_contratacao = ?
                WHERE id_funcionario = ?
                """,
                (nome, cargo, salario, data_contratacao, id_funcionario),
            )

    def deletar_funcionario(self, id_funcionario):
        with get_cursor() as cur:
            cur.execute("DELETE FROM Funcionario WHERE id_funcionario = ?;", (id_funcionario,))

    def inserir_funcionario_obj(self, funcionario):
        return self.inserir_funcionario(
            funcionario.id_funcionario,
            funcionario.nome,
            funcionario.cargo,
            funcionario.salario,
            funcionario.data_contratacao,
        )
