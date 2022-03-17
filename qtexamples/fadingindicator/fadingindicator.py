import qtexamples.shared

import sys

from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *

class FadingIndicator(QWidget):
    pixmapIndicator = None
    textIndicator = None

    def __init__(self, parent: QWidget, fontSize: int) -> None:
        super().__init__(parent)
        self.m_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.m_effect)
        self.m_effect.setOpacity(0.9)

        self.m_label = QLabel()
        font = self.m_label.font()
        font.setPixelSize(fontSize)
        self.m_label.setFont(font)

        pal = self.palette()
        pal.setColor(QPalette.WindowText, pal.color(QPalette.Window))
        self.m_label.setPalette(pal)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.m_label)

        self.m_pixmap = QPixmap()

    def setText(self, text: str) -> None:
        self.m_pixmap = QPixmap()
        self.m_label.setText(text)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.adjustSize()
        parent: QWidget = self.parentWidget()
        pos: QPoint = (parent.rect().center() - self.rect().center()) if parent else QPoint()
        if self.pixmapIndicator and self.pixmapIndicator.geometry().intersects(QRect(pos, self.size())):
            pos.setY(self.pixmapIndicator.getometry().bottom() + 1)
        self.move(pos)

    def setPixmap(self, uri: str) -> None:
        self.m_label.hide()
        self.m_pixmap.load(uri)
        self.layout().setSizeConstraint(QLayout.SetNoConstraint)
        self.resize(self.m_pixmap.size() // self.m_pixmap.devicePixelRatio())

        parent: QWidget = self.parentWidget()
        pos: QPoint = (parent.rect().center() - self.rect().center()) if parent else QPoint()
        if self.textIndicator and self.textIndicator.geometry().intersects(QRect(pos, self.size())):
            pos.setY(self.textIndicator.getometry().bottom() + 1)
        self.move(pos)

    def run(self, ms: int) -> None:
        self.show()
        self.raise_()
        QTimer.singleShot(ms, lambda: self.runInternal())

    def runInternal(self) -> None:
        animation = QPropertyAnimation(self.m_effect, b'opacity', self)
        animation.setDuration(200)
        animation.setEndValue(0.)
        animation.finished.connect(self.deleteLater)
        animation.start()

    def paintEvent(self, event: QPaintEvent) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        if not self.m_pixmap.isNull():
            p.drawPixmap(self.rect(), self.m_pixmap)
        else:
            p.setBrush(self.palette().color(QPalette.WindowText))
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(self.rect(), 15, 15)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.resize(640, 640)

    centralWidget = QWidget()
    win.setCentralWidget(centralWidget)
    win.show()

    def showFadingIndicator():
        indicator = FadingIndicator(centralWidget, 24)
        indicator.setText('Hello')
        indicator.run(3000)
    
    # Show a indicator
    QTimer.singleShot(1000, showFadingIndicator)

    app.exec_()