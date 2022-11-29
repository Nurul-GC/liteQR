from random import randint
from sys import argv, exit
from time import sleep
from webbrowser import open_new

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFontDatabase, QImage, QPalette, QBrush, QPixmap, QIcon
from PyQt6.QtWidgets import *
from pyqrcode import create


def initwindow():
    def iniciar():
        load = 0
        while load < 100:
            janela.showMessage(f"Loading Modules: {load}%", align, Qt.GlobalColor.white)
            sleep(0.5)
            load += randint(2, 10)
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
        self.janela_principal.setFixedSize(QSize(600, 500))
        self.janela_principal.setWindowIcon(QIcon("./favicon/favicon-256x256.ico"))

        bg_image = QImage(f"./favicon/bg.jpg")
        set_bg_image = bg_image.scaled(QSize(600, 500))  # resize Image to widget's size
        palette = QPalette()
        palette.setBrush(palette.ColorGroup.All, palette.ColorRole.Window, QBrush(set_bg_image))
        self.janela_principal.setPalette(palette)

        menu = QMenuBar()
        detalhes = menu.addMenu("Details")
        instr = detalhes.addAction("Intructions")
        instr.triggered.connect(self._instr)
        detalhes.addSeparator()
        _sair = lambda: self.gcapp.exit(0)
        sair = detalhes.addAction("Quit")
        sair.triggered.connect(_sair)
        sobre = menu.addAction("About")
        sobre.triggered.connect(self._sobre)

        self.janela_principal.setMenuBar(menu)
        self.mainwindow()

    def _sobre(self):
        QMessageBox.information(self.janela_principal, "About",
                                "<b>Info about the program</b><hr>"
                                "<p><ul><li><b>Name:</b> GC-liteQR</li>"
                                "<li><b>Version:</b> 0.1-112022</li>"
                                "<li><b>Maintener:</b> &copy;Nurul-GC</li>"
                                "<li><b>Publisher:</b> &trade;ArtesGC, Inc.</li></ul></p>")

    def _instr(self):
        QMessageBox.information(self.janela_principal, "Instructions",
                                "<b>Brief Presentation</b><hr>"
                                "<p>GC-liteQR is a simple and practical QR codes generator"
                                "it was built with `PyQt6 + QSS + PyQRCode` frameworks allowing the user"
                                "to easily create QR codes on his PC (offline) with three simple steps:</p>"
                                "<p>1. Type de content on the text box;<br>"
                                "2. Create the file clicking the button;<br>"
                                "3. Giving a name to the file and confirming the action;</p>"
                                "<p>The program saves the file as a PNG image and also customizes it"
                                "with different colors (automatically) each time you try to create a new one.</p>"
                                "<p>Thanks for your support!<br>"
                                "<b>&trade;ArtesGC, Inc.</b></p>")

    def mainwindow(self):
        def guardar():
            if datainput.toPlainText().isspace() or datainput.toPlainText() == "":
                QMessageBox.warning(self.janela_principal, "Warning",
                                    "<b>Please fill in the content field before saving the file!</b>")
            else:
                filename = QFileDialog.getSaveFileName(caption="Choose where to save and the file's name")[0]
                fileqr = create(content=datainput.toPlainText())
                fileqr.png(file=f"{filename}.png", scale=10,
                           module_color=(randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)),
                           background=(randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)))
                datainput.clear()
                perg = QMessageBox.question(self.janela_principal, "Successfuly Saved",
                                            f"<b>The file has been succesfully saved to the location bellow, "
                                            f"would you like to preview it?</b><hr>- {filename}.png")
                if perg.Yes:
                    view = QDialog()
                    viewlayout = QVBoxLayout()

                    imglabel = QLabel()
                    imglabel.setPixmap(QPixmap(f"{filename}.png"))
                    imglabel.setToolTip("Unfortunatelly you maybe unable to scan the code from here "
                                        "due to graphical issues!")
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
