import os
import sqlite3

# =========================
# CONFIGURAÇÃO DO BANCO
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'database')
DB_PATH = os.path.join(DB_DIR, 'banco.db')

# cria pasta se não existir
os.makedirs(DB_DIR, exist_ok=True)

# conexão
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()


# =========================
# CRIAÇÃO DAS TABELAS
# =========================
def criar_tabelas():
    cursor.executescript("""
                         CREATE TABLE IF NOT EXISTS Produto
                         (
                             idProduto
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             nome
                             TEXT,
                             ca
                             TEXT,
                             numeracao
                             INTEGER,
                             imagem
                             TEXT
                         );

                         CREATE TABLE IF NOT EXISTS Estoque
                         (
                             idEstoque
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             data
                             DATETIME
                             DEFAULT
                             CURRENT_TIMESTAMP,
                             entrada
                             INTEGER,
                             saida
                             INTEGER,
                             produto_id
                             INTEGER
                             NOT
                             NULL,
                             FOREIGN
                             KEY
                         (
                             produto_id
                         )
                             REFERENCES Produto
                         (
                             idProduto
                         )
                             ON DELETE NO ACTION
                             ON UPDATE NO ACTION
                             );
                         """)
    conn.commit()


# =========================
# CRUD PRODUTO
# =========================
def criar_produto(nome, ca, numeracao, imagem):
    cursor.execute("""
                   INSERT INTO Produto (nome, ca, numeracao, imagem)
                   VALUES (?, ?, ?, ?)
                   """, (nome, ca, numeracao, imagem))
    conn.commit()


def listar_produtos():
    cursor.execute("SELECT * FROM Produto")
    return cursor.fetchall()


# =========================
# MOVIMENTAÇÃO DE ESTOQUE
# =========================
def entrada_estoque(produto_id, quantidade):
    cursor.execute("""
                   INSERT INTO Estoque (entrada, saida, produto_id)
                   VALUES (?, NULL, ?)
                   """, (quantidade, produto_id))
    conn.commit()


def saida_estoque(produto_id, quantidade):
    cursor.execute("""
                   INSERT INTO Estoque (entrada, saida, produto_id)
                   VALUES (NULL, ?, ?)
                   """, (quantidade, produto_id))
    conn.commit()


# =========================
# CONSULTA DE ESTOQUE ATUAL
# =========================
def saldo_produto(produto_id):
    cursor.execute("""
                   SELECT COALESCE(SUM(entrada), 0) - COALESCE(SUM(saida), 0)
                   FROM Estoque
                   WHERE produto_id = ?
                   """, (produto_id,))

    return cursor.fetchone()[0]


# =========================
# TESTE
# =========================
if __name__ == "__main__":
    criar_tabelas()

    # cria produto
    criar_produto("Capacete", "CA123", 42, "imagens/capacete.png")

    produtos = listar_produtos()
    print("Produtos:", produtos)

    produto_id = produtos[0][0]

    # movimenta estoque
    entrada_estoque(produto_id, 10)
    saida_estoque(produto_id, 3)

    # consulta saldo
    saldo = saldo_produto(produto_id)
    print("Saldo do produto:", saldo)