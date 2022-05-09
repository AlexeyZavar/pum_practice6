import qasync
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPainter, Qt, QFont, QImage, QFontMetrics
from PySide6.QtWidgets import QWidget

from src import *

TRAIN_IMAGE = QImage('./assets/train.png').scaled(50, 50)
TRAIN_IMAGE_REVERSED = QImage('./assets/train.png').scaled(50, 50).mirrored(True, False)

DOT_RADIUS = 15
DOT_OFFSET = 60
TRAINS_OFFSET = 120
START = 80
OFFSET = 50
OFFSETS = {
    rokossovskaya: START,
    sobornaya: START + 6 * OFFSET,
    crystal: START + (6 + 3) * OFFSET,
    zarechnaya: START + (6 + 3 + 2) * OFFSET,
    biblioteka: START + (6 + 3 + 2 + 7) * OFFSET,
}

FONT = QFont('Montserrat', 14)
FONT_METRICS = QFontMetrics(FONT)


class SimulationWindow(QWidget):
    def __init__(self, simulation: Simulation):
        super().__init__()

        self.simulation = simulation

        self.setWindowTitle('Omsk Subway Simulation | by AlexeyZavar')

        self.setStyleSheet('''
        background-color: #f0fdf4;
        ''')

        self.setFixedWidth(1250)
        self.setFixedHeight(1000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.black)
        painter.setBrush(Qt.black)
        painter.setFont(FONT)

        w1 = FONT_METRICS.boundingRect(rokossovskaya.name).width()
        w2 = FONT_METRICS.boundingRect(biblioteka.name).width()
        p1 = QPoint(OFFSETS[rokossovskaya] + w1 / 2, 40)
        p2 = QPoint(OFFSETS[biblioteka] + w2 / 2, 40)

        painter.drawLine(p1, p2)

        for k, v in OFFSETS.items():
            w = FONT_METRICS.boundingRect(k.name).width()
            h = FONT_METRICS.boundingRect(k.name).height()

            count = str(len(k.people))
            w2 = FONT_METRICS.boundingRect(count).width()

            p1 = QPoint(v, 80)
            p2 = QPoint(v + w / 2, 40)
            p3 = QPoint(v + w / 2 - w2 / 2, 80 + h + 4)

            painter.drawText(p1, k.name)
            painter.drawText(p3, count)

            painter.drawEllipse(p2, DOT_RADIUS, DOT_RADIUS)

        for i, train in enumerate(self.simulation.trains):
            offset = train.path_total * (-(OFFSETS[train.current_station] - OFFSETS[train.next_station]) / 100)
            p = QPoint(OFFSETS[train.current_station] + offset, TRAINS_OFFSET)
            image = TRAIN_IMAGE if train.direction == 1 else TRAIN_IMAGE_REVERSED

            painter.drawImage(p, image)

        self.update()
