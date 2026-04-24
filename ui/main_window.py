
import os
import shutil
import time

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QFileDialog, QLabel
)
from PySide6.QtGui import QPixmap

from models.produto import Produto


class MainWindow(QWidget):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        self.produto_selecionado = None
        self.imagem_path = ""

        self.setWindowTitle("Sistema de Produtos")
        self.resize(700, 500)

        layout = QVBoxLayout()

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome")

        self.ca_input = QLineEdit()
        self.ca_input.setPlaceholderText("CA")

        self.num_input = QLineEdit()
        self.num_input.setPlaceholderText("Numeração")

        self.btn_upload = QPushButton("Selecionar Imagem")
        self.preview = QLabel("Preview")
        self.preview.setFixedHeight(120)

        self.btn_salvar = QPushButton("Salvar")
        self.btn_deletar = QPushButton("Deletar")

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CA", "Numeração"])

        layout.addWidget(self.nome_input)
        layout.addWidget(self.ca_input)
        layout.addWidget(self.num_input)
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.preview)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_deletar)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.btn_upload.clicked.connect(self.selecionar_imagem)
        self.btn_salvar.clicked.connect(self.salvar)
        self.btn_deletar.clicked.connect(self.deletar)
        self.table.cellClicked.connect(self.selecionar)

        self.carregar_dados()

    def selecionar_imagem(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar imagem",
            "",
            "Imagens (*.png *.jpg *.jpeg)"
        )

        if file_path:
            if not file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                QMessageBox.warning(self, "Erro", "Formato inválido")
                return

            self.imagem_path = file_path
            pixmap = QPixmap(file_path)
            self.preview.setPixmap(pixmap.scaledToHeight(120))

    def salvar(self):
        nome = self.nome_input.text()
        ca = self.ca_input.text()
        numeracao = self.num_input.text()

        if not nome:
            QMessageBox.warning(self, "Erro", "Nome obrigatório")
            return

        imagem_final = ""

        if self.imagem_path:
            uploads_dir = os.path.join(os.getcwd(), "uploads")
            os.makedirs(uploads_dir, exist_ok=True)

            nome_arquivo = f"{int(time.time())}_{os.path.basename(self.imagem_path)}"
            destino = os.path.join(uploads_dir, nome_arquivo)

            shutil.copy(self.imagem_path, destino)
            imagem_final = destino

        if self.produto_selecionado:
            produto = Produto(self.produto_selecionado, nome, ca, int(numeracao), imagem_final)
            self.repo.atualizar(produto)
        else:
            produto = Produto(None, nome, ca, int(numeracao), imagem_final)
            self.repo.criar(produto)

        self.limpar()
        self.carregar_dados()

    def deletar(self):
        if not self.produto_selecionado:
            return

        self.repo.deletar(self.produto_selecionado)
        self.limpar()
        self.carregar_dados()

    def selecionar(self, row, _):
        self.produto_selecionado = int(self.table.item(row, 0).text())
        self.nome_input.setText(self.table.item(row, 1).text())
        self.ca_input.setText(self.table.item(row, 2).text())
        self.num_input.setText(self.table.item(row, 3).text())

        produtos = self.repo.listar()
        produto = next((p for p in produtos if p.idProduto == self.produto_selecionado), None)

        if produto and produto.imagem and os.path.exists(produto.imagem):
            pixmap = QPixmap(produto.imagem)
            self.preview.setPixmap(pixmap.scaledToHeight(120))

    def limpar(self):
        self.produto_selecionado = None
        self.nome_input.clear()
        self.ca_input.clear()
        self.num_input.clear()
        self.preview.clear()
        self.imagem_path = ""
