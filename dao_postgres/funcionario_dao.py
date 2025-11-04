from dao.db import get_cursor


class FuncionarioDAO:
    def __init__(self):
        # DAO não precisa conhecer a config — usa o pool inicializado em dao.db
        pass

    def listar_funcionarios(self):
        with get_cursor() as cur:
            cur.execute(
                "SELECT id_funcionario, nome, cargo, salario, data_contratacao FROM Funcionario;"
            )
            return cur.fetchall()

    def inserir_funcionario(self, id_funcionario, nome, cargo, salario, data_contratacao):
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO Funcionario (id_funcionario, nome, cargo, salario, data_contratacao)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id_funcionario, nome, cargo, salario, data_contratacao),
            )

    def buscar_funcionario(self, id_funcionario):
        with get_cursor() as cur:
            cur.execute(
                "SELECT id_funcionario, nome, cargo, salario, data_contratacao FROM Funcionario WHERE id_funcionario = %s;",
                (id_funcionario,),
            )
            return cur.fetchone()

    def atualizar_funcionario(self, id_funcionario, nome, cargo, salario, data_contratacao):
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE Funcionario SET nome = %s, cargo = %s, salario = %s, data_contratacao = %s
                WHERE id_funcionario = %s
                """,
                (nome, cargo, salario, data_contratacao, id_funcionario),
            )

    def deletar_funcionario(self, id_funcionario):
        with get_cursor() as cur:
            cur.execute("DELETE FROM Funcionario WHERE id_funcionario = %s;", (id_funcionario,))

    def inserir_funcionario_obj(self, funcionario):
        """Convenience: insere usando um modelo Funcionario"""
        return self.inserir_funcionario(
            funcionario.id_funcionario,
            funcionario.nome,
            funcionario.cargo,
            funcionario.salario,
            funcionario.data_contratacao,
        )
