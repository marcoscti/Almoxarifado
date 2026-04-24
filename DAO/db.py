import os
import sqlite3


class Database:
    def __init__(self):
        # =========================
        # CONFIGURAÇÃO DO BANCO
        # =========================
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB_DIR = os.path.join(BASE_DIR, 'database')
        self.DB_PATH = os.path.join(DB_DIR, 'banco.db')

        # cria pasta se não existir
        os.makedirs(DB_DIR, exist_ok=True)

        # conexão
        self.conn = sqlite3.connect(self.DB_PATH)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()

    # =========================
    # CRIAÇÃO DAS TABELAS
    # =========================
    def criar_tabelas(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS Produto (
                idProduto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                ca TEXT,
                numeracao INTEGER,
                imagem TEXT
            );

            CREATE TABLE IF NOT EXISTS Estoque (
                idEstoque INTEGER PRIMARY KEY AUTOINCREMENT,
                data DATETIME DEFAULT CURRENT_TIMESTAMP,
                entrada INTEGER,
                saida INTEGER,
                produto_id INTEGER NOT NULL,
                FOREIGN KEY (produto_id)
                    REFERENCES Produto(idProduto)
                    ON DELETE NO ACTION
                    ON UPDATE NO ACTION
            );
        """)
        self.conn.commit()

    # =========================
    # CRUD PRODUTO
    # =========================
    def criar_produto(self, nome, ca, numeracao, imagem):
        self.cursor.execute("""
            INSERT INTO Produto (nome, ca, numeracao, imagem)
            VALUES (?, ?, ?, ?)
        """, (nome, ca, numeracao, imagem))
        self.conn.commit()

    def listar_produtos(self):
        self.cursor.execute("SELECT * FROM Produto")
        return self.cursor.fetchall()

    # =========================
    # MOVIMENTAÇÃO DE ESTOQUE
    # =========================
    def entrada_estoque(self, produto_id, quantidade):
        self.cursor.execute("""
            INSERT INTO Estoque (entrada, saida, produto_id)
            VALUES (?, NULL, ?)
        """, (quantidade, produto_id))
        self.conn.commit()

    def saida_estoque(self, produto_id, quantidade):
        self.cursor.execute("""
            INSERT INTO Estoque (entrada, saida, produto_id)
            VALUES (NULL, ?, ?)
        """, (quantidade, produto_id))
        self.conn.commit()

    # =========================
    # CONSULTA DE ESTOQUE ATUAL
    # =========================
    def saldo_produto(self, produto_id):
        self.cursor.execute("""
            SELECT COALESCE(SUM(entrada), 0) - COALESCE(SUM(saida), 0)
            FROM Estoque
            WHERE produto_id = ?
        """, (produto_id,))
        return self.cursor.fetchone()[0]


# =========================
# TESTE
# =========================
if __name__ == "__main__":
    db = Database()
    db.criar_tabelas()

    # cria produto
    db.criar_produto("Capacete", "CA123", 42, "imagens/capacete.png")

    produtos = db.listar_produtos()
    print("Produtos:", produtos)

    produto_id = produtos[0][0]

    # movimenta estoque
    db.entrada_estoque(produto_id, 10)
    db.saida_estoque(produto_id, 3)

    # consulta saldo
    saldo = db.saldo_produto(produto_id)
    print("Saldo do produto:", saldo)