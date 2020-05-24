from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen,QColor
from PyQt5.QtCore import Qt
import sys
from generator import Generator


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.first_draw=False

    def initUI(self):
        self.setGeometry(300, 300, 1000, 1000)
        self.setWindowTitle('ega')
        self.show()

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        graph = self.drawLines(qp)
        self.drawPoints(qp,graph)
        qp.end()

    def drawLines(self, qp):
        self.first_draw=True
        pen = QPen(Qt.black, 2, Qt.SolidLine)

        qp.setPen(pen)
        #qp.drawLine(20, 40, 250, 40)

        generator = Generator(1000,1000,10,10)
        graph = generator.build_graph()

        for edge in graph.edges:
            qp.drawLine(edge.source.x,edge.source.y,edge.target.x,edge.target.y)
        return graph

    def drawPoints(self,qp,graph):
        pen = QPen()
        pen.setWidth(15)
        pen.setColor(QColor("red"))
        qp.setPen(pen)
        for node in graph.nodes:

            x = node.x
            y = node.y
            #pen.setColor(QColor("red"))
            qp.drawPoint(x, y)

            #qp.drawText(x,y,str(node.i))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())