class Produto:

    def __init__(self, idProduto, nome, ca, numeracao, imagem):
        self.idProduto = idProduto
        self.nome = nome
        self.ca = ca
        self.numeracao = numeracao
        self.imagem = imagem
    
    def listar_produtos():
        cursor.execute("SELECT * FROM Produto")
        return cursor.fetchall()