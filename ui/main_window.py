
import os
import shutil
import time

from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap

from models.produto import Produto


class MainWindow(QWidget):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        self.produto_selecionado = None
        self.imagem_path = ""

        self.setWindowTitle("Almoxarifado")
        self.resize(700, 700)
        
        layout = QVBoxLayout()
        
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome")

        self.ca_input = QLineEdit()
        self.ca_input.setPlaceholderText("CA")

        self.num_input = QLineEdit()
        self.num_input.setPlaceholderText("Numeração")
        self.EstoqueMinimo = QLineEdit()
        self.EstoqueMinimo.setPlaceholderText("Estoque Mínimo")
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Entrada")
        self.saida = QLineEdit()
        self.saida.setPlaceholderText("Saída")
        self.btn_upload = QPushButton("Selecionar Imagem")
        self.preview = QLabel("Preview")
        self.preview.setFixedHeight(120)

        self.btn_salvar = QPushButton("Salvar")
        self.btn_deletar = QPushButton("Deletar")

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CA", "Numeração", "Imagem", "Estoque Mínimo", "Entrada", "Saída"])

        layout.addWidget(self.nome_input)
        layout.addWidget(self.ca_input)
        layout.addWidget(self.num_input)
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.preview)
        layout.addWidget(self.EstoqueMinimo)
        layout.addWidget(self.entrada)
        layout.addWidget(self.saida)
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
            self.preview.setPixmap(pixmap.scaledToHeight(100))

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
            produto = Produto(self.produto_selecionado, nome, ca, int(numeracao), imagem_final if imagem_final else None, estoqueMinimo=int(self.EstoqueMinimo.text() or 0), entrada=int(self.entrada.text() or 0), saida=int(self.saida.text() or 0))
            self.repo.atualizar(produto)
        else:
            produto = Produto(None, nome, ca, int(numeracao), imagem_final if imagem_final else None, estoqueMinimo=int(self.EstoqueMinimo.text() or 0), entrada=int(self.entrada.text() or 0), saida=int(self.saida.text() or 0))
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
        self.ca_input.setText(self.table.item(row, 2).text().upper())
        self.num_input.setText(self.table.item(row, 3).text())
        self.EstoqueMinimo.setText(self.table.item(row, 5).text())
        self.entrada.setText(self.table.item(row, 6).text())
        self.saida.setText(self.table.item(row, 7).text())
        

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
        self.EstoqueMinimo.clear()
        self.entrada.clear()
        self.saida.clear()

    def carregar_dados(self):
        produtos = self.repo.listar()

        self.table.setRowCount(len(produtos))

        for row, p in enumerate(produtos):
            self.table.setItem(row, 0, QTableWidgetItem(str(p.idProduto)))
            self.table.setItem(row, 1, QTableWidgetItem(p.nome))
            self.table.setItem(row, 2, QTableWidgetItem(p.ca))
            self.table.setItem(row, 3, QTableWidgetItem(str(p.numeracao)))
            self.table.setItem(row, 4, QTableWidgetItem(p.imagem if p.imagem else ""))
            self.table.setItem(row, 5, QTableWidgetItem(str(p.estoqueMinimo)))
            self.table.setItem(row, 6, QTableWidgetItem(str(p.entrada)))
            self.table.setItem(row, 7, QTableWidgetItem(str(p.saida)))