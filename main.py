from random import randint
from sys import argv
from webbrowser import open_new

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFontDatabase, QImage, QPalette, QBrush
from PyQt6.QtWidgets import *
from pyqrcode import create


class LQR:
    def __init__(self):
        self.gcapp = QApplication(argv)

        QFontDatabase.addApplicationFont("./font/abel.ttf")

        self.janela_principal = QMainWindow()
        self.janela_principal.setWindowTitle("GC-liteQR")
        self.janela_principal.setStyleSheet(theme)
        self.janela_principal.setFixedSize(QSize(500, 500))

        bg_image = QImage(f"./img/bg.jpg")
        set_bg_image = bg_image.scaled(QSize(600, 500))  # resize Image to widget's size
        palette = QPalette()
        palette.setBrush(palette.ColorGroup.All, palette.ColorRole.Window, QBrush(set_bg_image))
        self.janela_principal.setPalette(palette)

        menu = QMenuBar()
        detalhes = menu.addMenu("Detalhes")
        detalhes.addAction("Intruções")
        detalhes.addSeparator()
        sair = detalhes.addAction("Sair")
        sair.triggered.connect(self._sair)
        sobre = menu.addAction("Sobre")
        sobre.triggered.connect(self._sobre)

        self.mainwindow()
        self.janela_principal.setMenuBar(menu)
        self.janela_principal.show()

    def _sobre(self):
        QMessageBox.information(self.janela_principal, "Sobre",
                                "<h1>Informações do Programa</h1><hr>"
                                "<p>...</p>")

    def _sair(self):
        perg = QMessageBox.question(self.janela_principal, "Sair",
                                    "Tem a certeza que deseja terminar o programa?")
        if perg.Yes:
            exit(0)

    def mainwindow(self):
        def guardar():
            if datainput.toPlainText().isspace() or datainput.toPlainText() == "":
                QMessageBox.warning(self.janela_principal, "Erro",
                                    "<h1>Por favor preencha o campo de conteudo antes de salvar o arquivo!</h1>")
            else:
                filename = QFileDialog.getSaveFileName(caption="Selecione aonde salvar e o nome do arquivo")[0]
                fileqr = create(content=datainput.toPlainText())
                fileqr.png(file=f"{filename}.png",
                           module_color=(randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)),
                           background=(randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)))
                QMessageBox.information(self.janela_principal, "Arquivo Salvo",
                                        f"<h1>O arquivo foi salvo com sucesso na localização</h1><hr>- {filename}")

        ferramentas = QWidget()
        layout = QFormLayout()

        textlabel = QLabel("<h1>GC-liteQR</h1><small>Simples criador de codigos QR</small><hr>")
        textlabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addRow(textlabel)

        datainput = QTextEdit()
        layout.addRow("Digite aqui\no conteudo:", datainput)

        savebtn = QPushButton("Guardar")
        savebtn.clicked.connect(guardar)
        layout.addWidget(savebtn)

        # copyright-label
        browser = lambda p: open_new('https://artesgc.home.blog')
        website = QLabel("<a href='#' style='text-decoration:none; color:white;'>™ ArtesGC, Inc.</a>")
        website.setAlignment(Qt.AlignmentFlag.AlignRight)
        website.setToolTip('Access to the official website of ArtesGC!')
        website.linkActivated.connect(browser)
        layout.addRow(website)

        ferramentas.setLayout(layout)
        self.janela_principal.setCentralWidget(ferramentas)


if __name__ == '__main__':
    theme = open("./theme/liteqr.qss").read().strip()
    app = LQR()
    app.gcapp.exec()
