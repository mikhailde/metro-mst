from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint, QRectF
from PyQt6.QtGui import QPainter, QPen, QBrush

class DrawingArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setMouseTracking(True)
        self.dragging_station = -1
        self.last_pan_pos = None
        self.pan_offset = QPoint(0, 0)
        
        self.metro_pen = QPen(Qt.GlobalColor.blue, 3)
        self.metro_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.station_brush = QBrush()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(self.pan_offset)
        painter.setPen(self.metro_pen)

        for start, end in self.parent.metro_optimizer.build_mst():
            painter.drawLine(start[0], start[1], end[0], end[1])

        for i, (x, y) in enumerate(self.parent.metro_optimizer.stations):
            if i == self.dragging_station:
                self.station_brush.setColor(Qt.GlobalColor.red)
            else:
                self.station_brush.setColor(Qt.GlobalColor.blue)
            
            painter.setBrush(self.station_brush)
            painter.drawRect(QRectF(x - 8, y - 8, 16, 16))

    def mousePressEvent(self, event):
        event_pos = event.pos()
        x, y = event_pos.x() - self.pan_offset.x(), event_pos.y() - self.pan_offset.y()

        if event.button() == Qt.MouseButton.LeftButton:
            for i, (station_x, station_y) in enumerate(self.parent.metro_optimizer.stations):
                if abs(station_x - x) <= 8 and abs(station_y - y) <= 8:
                    self.dragging_station = i
                    return
            self.parent.metro_optimizer.add_station(x, y)
            self.update()

        elif event.button() == Qt.MouseButton.RightButton:
            for i, (station_x, station_y) in enumerate(self.parent.metro_optimizer.stations):
                if abs(station_x - x) <= 8 and abs(station_y - y) <= 8:
                    self.parent.metro_optimizer.stations.pop(i)
                    self.update()
                    break

        elif event.button() == Qt.MouseButton.MiddleButton:
            self.last_pan_pos = event_pos

    def mouseMoveEvent(self, event):
        if self.dragging_station != -1:
            x, y = event.pos().x() - self.pan_offset.x(), event.pos().y() - self.pan_offset.y()
            self.parent.metro_optimizer.stations[self.dragging_station] = (x, y)
            self.update()
        elif self.last_pan_pos is not None:
            delta = event.pos() - self.last_pan_pos
            self.pan_offset += delta
            self.last_pan_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging_station = -1
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.last_pan_pos = None