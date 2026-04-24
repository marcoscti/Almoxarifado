
import sys
from PySide6.QtWidgets import QApplication

from database.database import Database
from repositories.produto_repository import ProdutoRepository
from ui.main_window import MainWindow

app = QApplication(sys.argv)

db = Database()
db.criar_tabelas()

repo = ProdutoRepository(db)

window = MainWindow(repo)
window.show()

sys.exit(app.exec())
