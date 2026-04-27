
from models.produto import Produto

class ProdutoRepository:
    def __init__(self, db):
        self.db = db

    def criar(self, produto):
        try:
            self.db.cursor.execute("""
                INSERT INTO Produto (nome_produto, ca_produto, numeracao_produto, imagem_produto, estoque_minimo, entrada, saida, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (produto.nome, produto.ca, produto.numeracao, produto.imagem, produto.estoqueMinimo, produto.entrada, produto.saida, produto.created_at, produto.updated_at))
            self.db.conn.commit()
        except Exception as e:
            print(f"Erro ao criar produto: {e}")

    def listar(self):
        try:
            self.db.cursor.execute("SELECT * FROM Produto")
            rows = self.db.cursor.fetchall()
            if len(rows) > 0:
                return [Produto(*row) for row in rows]
            else:
                print("Nenhum produto encontrado.")
                return []
        except Exception as e:
            print(f"Erro ao listar produtos: {e}")
            return []

    def atualizar(self, produto):
        try:
            self.db.cursor.execute("""
                UPDATE Produto
                SET nome_produto=?, ca_produto=?, numeracao_produto=?, imagem_produto=?, estoque_minimo=?, entrada=?, saida=?, updated_at=?
                WHERE id_produto=?
            """, (produto.nome, produto.ca, produto.numeracao, produto.imagem, produto.estoqueMinimo, produto.entrada, produto.saida, produto.updated_at, produto.idProduto))
            self.db.conn.commit()
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")

    def deletar(self, idProduto):
        try:
            self.db.cursor.execute("DELETE FROM Produto WHERE id_produto=?", (idProduto,))
            self.db.conn.commit()
        except Exception as e:
            print(f"Erro ao deletar produto: {e}")
