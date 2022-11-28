from random import randint
from sys import argv
from time import sleep
from webbrowser import open_new

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFontDatabase, QImage, QPalette, QBrush, QPixmap, QIcon, QPicture
from PyQt6.QtWidgets import *
from pyqrcode import create


def initwindow():
    def iniciar():
        load = 0
        while load < 100:
            janela.showMessage(f"Carregando Modulos: {load}%", align, Qt.GlobalColor.white)
            sleep(0.5)
            load += randint(5, 10)
        janela.close()
        app.janela_principal.show()

    img = QPixmap("./favicon/favicon-512x512.png")
    align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignAbsolute)
    janela = QSplashScreen(img)
    janela.setStyleSheet(theme)
    janela.show()
    iniciar()


class LQR:
    def __init__(self):
        self.gcapp = QApplication(argv)

        QFontDatabase.addApplicationFont("./font/abel.ttf")

        self.janela_principal = QMainWindow()
        self.janela_principal.setWindowTitle("GC-liteQR")
        self.janela_principal.setStyleSheet(theme)
        self.janela_principal.setFixedSize(QSize(500, 500))
        self.janela_principal.setWindowIcon(QIcon("./favicon/favicon.ico"))

        bg_image = QImage(f"./img/bg.jpg")
        set_bg_image = bg_image.scaled(QSize(600, 500))  # resize Image to widget's size
        palette = QPalette()
        palette.setBrush(palette.ColorGroup.All, palette.ColorRole.Window, QBrush(set_bg_image))
        self.janela_principal.setPalette(palette)

        menu = QMenuBar()
        detalhes = menu.addMenu("Details")
        detalhes.addAction("Intructions")
        detalhes.addSeparator()
        sair = detalhes.addAction("Quit")
        sair.triggered.connect(self._sair)
        sobre = menu.addAction("About")
        sobre.triggered.connect(self._sobre)

        self.janela_principal.setMenuBar(menu)
        self.mainwindow()

    def _sobre(self):
        QMessageBox.information(self.janela_principal, "About",
                                "<h1>Info about the program</h1><hr>"
                                "<p>...</p>")

    def _sair(self):
        perg = QMessageBox.question(self.janela_principal, "Quit",
                                    "Are you sure you want to end the program?")
        if perg.Yes:
            exit(0)

    def mainwindow(self):
        def guardar():
            if datainput.toPlainText().isspace() or datainput.toPlainText() == "":
                QMessageBox.warning(self.janela_principal, "Warning",
                                    "<h1>Please fill in the content field before saving the file!</h1>")
            else:
                filename = QFileDialog.getSaveFileName(caption="Choose where to save and the file's name")[0]
                fileqr = create(content=datainput.toPlainText())
                fileqr.png(file=f"{filename}.png", scale=10,
                           module_color=(randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)),
                           background=(randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)))
                datainput.clear()
                perg = QMessageBox.question(self.janela_principal, "Successfuly Saved",
                                            f"<h1>The file has been succesfully saved to the location bellow, "
                                            f"would you like to preview it?</h1><hr>- {filename}.png")
                if perg.Yes:
                    view = QDialog()
                    viewlayout = QVBoxLayout()

                    imglabel = QLabel()
                    imglabel.setPixmap(QPixmap(f"{filename}.png"))
                    imglabel.setToolTip("Unfortunatelly you can't scan the code from here due to graphical issues!")
                    viewlayout.addWidget(imglabel)

                    fechar = lambda: view.close()
                    fecharbtn = QPushButton("Close")
                    fecharbtn.clicked.connect(fechar)
                    viewlayout.addWidget(fecharbtn)

                    view.setLayout(viewlayout)
                    view.show()

        ferramentas = QWidget()
        layout = QFormLayout()

        textlabel = QLabel("<h1>GC-liteQR</h1><hr><small>Simple QR code generator</small>")
        textlabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addRow(textlabel)

        datainput = QTextEdit()
        datainput.setPlaceholderText("Type here the content..")
        layout.addRow(datainput)

        savebtn = QPushButton("Save")
        savebtn.clicked.connect(guardar)
        layout.addRow(savebtn)

        # copyright-label
        browser = lambda p: open_new('https://artesgc.home.blog')
        website = QLabel("<a href='#' style='text-decoration:none; color:green;'>™ ArtesGC, Inc.</a>")
        website.setAlignment(Qt.AlignmentFlag.AlignRight)
        website.setToolTip('Access to the official website of ArtesGC!')
        website.linkActivated.connect(browser)
        layout.addRow(website)

        ferramentas.setLayout(layout)
        self.janela_principal.setCentralWidget(ferramentas)


if __name__ == '__main__':
    theme = open("./theme/liteqr.qss").read().strip()
    app = LQR()
    initwindow()
    app.gcapp.exec()

