
from models.produto import Produto

class ProdutoRepository:
    def __init__(self, db):
        self.db = db

    def criar(self, produto):
        self.db.cursor.execute("""
            INSERT INTO Produto (nome_produto, ca_produto, numeracao_produto, imagem_produto, estoque_minimo, entrada, saida, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?,?, ?)
        """, (produto.nome, produto.ca, produto.numeracao, produto.imagem, produto.estoqueMinimo, produto.entrada, produto.saida, produto.created_at, produto.updated_at))
        self.db.conn.commit()

    def listar(self):
        self.db.cursor.execute("SELECT * FROM Produto")
        rows = self.db.cursor.fetchall()
        return [Produto(*row) for row in rows]

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
        self.db.cursor.execute("DELETE FROM Produto WHERE id_produto=?", (idProduto,))
        self.db.conn.commit()
