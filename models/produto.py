
class Produto:
    def __init__(self, idProduto: int = None, nome: str = None, ca: str = None, numeracao: int = None, imagem: str = None, estoqueMinimo: int = None, entrada: int = None, saida: int = None, created_at: str = None, updated_at: str = None):
        self.idProduto = idProduto
        self.nome = nome
        self.ca = ca
        self.numeracao = numeracao
        self.imagem = imagem
        self.estoqueMinimo = estoqueMinimo
        self.entrada = entrada
        self.saida = saida
        self.created_at = created_at
        self.updated_at = updated_at