
import os
import sqlite3

class Database:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "banco.db")

        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()

    def criar_tabelas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Produto (
                id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_produto TEXT,
                ca_produto TEXT,
                numeracao_produto INTEGER,
                imagem_produto TEXT,
                estoque_minimo INTEGER,
                entrada INTEGER,
                saida INTEGER,
                created_at DATETIME,
                updated_at DATETIME
                            )
        """)
        self.conn.commit()
