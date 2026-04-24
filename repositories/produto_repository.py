
from models.produto import Produto

class ProdutoRepository:
    def __init__(self, db):
        self.db = db

    def criar(self, produto):
        self.db.cursor.execute("""
            INSERT INTO Produto (nome, ca, numeracao, imagem)
            VALUES (?, ?, ?, ?)
        """, (produto.nome, produto.ca, produto.numeracao, produto.imagem))
        self.db.conn.commit()

    def listar(self):
        self.db.cursor.execute("SELECT * FROM Produto")
        rows = self.db.cursor.fetchall()
        return [Produto(*row) for row in rows]

    def atualizar(self, produto):
        self.db.cursor.execute("""
            UPDATE Produto
            SET nome=?, ca=?, numeracao=?, imagem=?
            WHERE idProduto=?
        """, (produto.nome, produto.ca, produto.numeracao, produto.imagem, produto.idProduto))
        self.db.conn.commit()

    def deletar(self, idProduto):
        self.db.cursor.execute("DELETE FROM Produto WHERE idProduto=?", (idProduto,))
        self.db.conn.commit()
