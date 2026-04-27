
import datetime
from database.database import Database
from models.produto import Produto
from repositories.produto_repository import ProdutoRepository


produtoRepository = ProdutoRepository(Database())
#produtoRepository.criar(Produto(None, "Produto Teste 3", "CA12345", 42, "imagem.png", 10, 100, 50, datetime.datetime.now(), datetime.datetime.now()))
try:
    produtoRepository.atualizar(Produto(2, "Produto Teste Atualizado", "CA54321", 43, "imagem_atualizada.png", 5, 150, 30,None, datetime.datetime.now()))
except Exception as e:
    print(f"Erro ao atualizar produto: {e}")

for produto in produtoRepository.listar():
    print('-----------------------------')
    print(f"ID: {produto.idProduto},\nNome: {produto.nome},\nCA: {produto.ca},\nNumeracao: {produto.numeracao},\nImagem: {produto.imagem},\nEstoque Minimo: {produto.estoqueMinimo},\nEntrada: {produto.entrada},\nSaida: {produto.saida},\nCriado: {produto.created_at},\nAtualizado: {produto.updated_at}\nSaldo: {produto.entrada - produto.saida}")
