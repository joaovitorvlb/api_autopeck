from .db import get_cursor

class ProdutoDAO:
    def __init__(self):
        pass

    def listar_produtos(self):
        """Lista todos os produtos"""
        with get_cursor() as cur:
            sql = "SELECT id_produto, nome, descricao, preco, estoque, nome_imagem FROM Produto"
            cur.execute(sql)
            rows = cur.fetchall()
            return rows

    def inserir_produto(self, id_produto, nome, descricao, preco, estoque, url=None):
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO Produto (id_produto, nome, descricao, preco, estoque, url)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (id_produto, nome, descricao, preco, estoque, url),
            )

    def buscar_produto(self, id_produto):
        """Busca um produto específico pelo ID"""
        with get_cursor() as cur:
            sql = "SELECT id_produto, nome, descricao, preco, estoque, nome_imagem FROM Produto WHERE id_produto = %s"
            cur.execute(sql, (id_produto,))
            row = cur.fetchone()
            return row

    def atualizar_produto(self, id_produto, nome, descricao, preco, estoque, nome_imagem=None):
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE Produto SET nome = %s, descricao = %s, preco = %s, estoque = %s, nome_imagem = %s
                WHERE id_produto = %s
                """,
                (nome, descricao, preco, estoque, nome_imagem, id_produto),
            )

    def deletar_produto(self, id_produto):
        with get_cursor() as cur:
            cur.execute("DELETE FROM Produto WHERE id_produto = %s;", (id_produto,))

    def inserir_produto_obj(self, produto):
        return self.inserir_produto(
            produto.id_produto,
            produto.nome,
            produto.descricao,
            produto.preco,
            produto.estoque,
            getattr(produto, 'url', None),
        )

    def criar_produto(self, dados):
        """
        Cria um novo produto sem especificar ID (auto-increment)
        Retorna o produto criado com o ID gerado
        """
        print(f"🗄️ [DAO DEBUG] Iniciando criação de produto com dados: {dados}")
        
        try:
            with get_cursor() as cur:
                print("🗄️ [DAO DEBUG] Cursor obtido, executando INSERT...")
                
                # INSERT do produto
                sql_insert = """
                INSERT INTO Produto (nome, descricao, preco, estoque, nome_imagem)
                VALUES (%s, %s, %s, %s, %s)
                """
                params = (dados['nome'], dados.get('descricao', ''), dados['preco'], dados['estoque'], dados.get('nome_imagem'))
                
                print(f"🗄️ [DAO DEBUG] SQL INSERT: {sql_insert}")
                print(f"🗄️ [DAO DEBUG] Parâmetros: {params}")
                
                cur.execute(sql_insert, params)
                
                # Obter o ID do produto criado
                produto_id = cur.lastrowid
                print(f"🗄️ [DAO DEBUG] Produto inserido com ID: {produto_id}")
                
                # Buscar o produto na MESMA transação
                print(f"🗄️ [DAO DEBUG] Buscando produto na mesma transação...")
                sql_select = "SELECT id_produto, nome, descricao, preco, estoque, nome_imagem FROM Produto WHERE id_produto = %s"
                print(f"🗄️ [DAO DEBUG] SQL SELECT: {sql_select}")
                print(f"🗄️ [DAO DEBUG] ID para busca: {produto_id}")
                
                cur.execute(sql_select, (produto_id,))
                row = cur.fetchone()
                
                if row:
                    produto_criado = row
                    print(f"🗄️ [DAO DEBUG] Produto encontrado na mesma transação: {produto_criado}")
                    return produto_criado
                else:
                    print(f"🗄️ [DAO DEBUG] ERRO: Produto não encontrado mesmo na mesma transação!")
                    return None
                
        except Exception as e:
            print(f"💥 [DAO ERROR] Erro ao criar produto: {e}")
            import traceback
            print("📊 [DAO ERROR] Stack trace:")
            traceback.print_exc()
            raise e