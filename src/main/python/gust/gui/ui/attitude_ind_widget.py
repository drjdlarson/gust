#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 11:53:26 2022

@author: abhandari11
"""

import sys
from math import cos, radians, sin, sqrt

from PyQt5.QtCore import QLine, QPoint, QPointF, QRectF, Qt
from PyQt5.QtGui import (
    QBrush,
    QPainter,
    QPolygonF,
    QColor,
    QLinearGradient,
    QPixmap,
)
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QApplication
)
from gust.gui.msg_decoder import MessageDecoder as msg_decoder

g5Width = 480
g5CenterX = g5Width / 2
g5Height = 360
g5CenterY = g5Height / 2
altBoxWidth = 75
tasHeight = 30
speedBoxWidth = 75
g5Diag = sqrt(g5Width ** 2 + g5Height ** 2)
mstokt = 1.94384



class pyG5AIWidget(QWidget):
    """Generate G5 wdiget view."""

    def __init__(self, parent):
    # def __init__(self))
        super().__init__(parent=parent)

    def setup_hud_ui(self, ctx):
        self.setWindowTitle("Attitude Indicator")
        self.setFixedSize(g5Width, g5Height)
        self.setContentsMargins(0, 0, 0, 0)

        # parameters
        self.rollArcRadius = g5CenterY * 0.8
        self._pitchScale = 25

        self.clean_hud()
        self.ctx = ctx

    def clean_hud(self):
        self.roll_angle = 0
        self.pitch_angle = 0
        self.gndspeed = 0
        self.airspeed = 0
        self.altitude = 0
        self.vspeed = 0
        self.heading = 0
        self.arm = "NONE"
        self.gnss_fix = 0
        self.mode = "NONE"

        self.alpha = 0
        self.beta = 0
        self.sat_count = 0

        self.repaint()

    def setPen(self, width, color, style=Qt.SolidLine):
        """Set the pen color and width."""
        pen = self.qp.pen()
        pen.setColor(color)
        pen.setWidth(width)
        pen.setStyle(style)
        self.qp.setPen(pen)

    def paintEvent(self, event):
        """Paint the widget."""
        diamondHeight = 14
        diamondWidth = 14

        self.qp = QPainter(self)

        # set default font size
        font = self.qp.font()
        font.setPixelSize(6)
        font.setBold(True)
        self.qp.setFont(font)

        self.setPen(1, Qt.white)
        grad = QLinearGradient(g5CenterX, g5Height, g5CenterX, 0)
        grad.setColorAt(1, QColor(0, 50, 200, 255))
        grad.setColorAt(0, QColor(0, 255, 255, 255))
        self.qp.setBrush(grad)


        # draw contour + backgorun sky
        self.qp.drawRect(QRectF(0, 0, g5Width, g5Height))

        # draw the rotating part depending on the roll angle
        self.qp.translate(g5CenterX, g5CenterY)
        self.qp.rotate(-self.roll_angle)

        #draw the ground
        grad = QLinearGradient(
            g5CenterX,
            +self.pitch_angle / self._pitchScale * g5CenterY,
            g5CenterX,
            +g5Diag,
        )
        grad.setColorAt(0, QColor(152, 103, 45))
        grad.setColorAt(1, QColor(255, 222, 173))
        self.qp.setBrush(grad)

        self.qp.drawRect(
            QRectF(
                QPointF(
                    -g5Diag,
                    +self.pitch_angle / self._pitchScale * g5CenterY,
                ),
                QPointF(
                    +g5Diag,
                    +g5Diag,
                ),
            )
        )

        # draw the pitch lines
        height = 0
        pitch = 0
        width = [10, 20, 10, 30]
        mode = 0
        while height < self.rollArcRadius - 40:
            pitch += 2.5
            height = (
                pitch / self._pitchScale * g5CenterY
                + self.pitch_angle / self._pitchScale * g5CenterY
            )
            self.qp.drawLine(
                QPointF(
                    -width[mode],
                    height,
                ),
                QPointF(
                    width[mode],
                    height,
                ),
            )
            if width[mode] == 30:
                self.qp.drawText(QPoint(30 + 3, height + 2), str(int(pitch)))
                self.qp.drawText(QPoint(-40, height + 2), str(int(pitch)))
            mode = (mode + 1) % 4

        height = 0
        pitch = 0
        width = [10, 20, 10, 30]
        mode = 0
        while height > -self.rollArcRadius + 30:
            pitch -= 2.5
            height = (
                pitch / self._pitchScale * g5CenterY
                + self.pitch_angle / self._pitchScale * g5CenterY
            )
            self.qp.drawLine(
                QPointF(
                    -width[mode],
                    height,
                ),
                QPointF(
                    width[mode],
                    height,
                ),
            )
            if width[mode] == 30:
                self.qp.drawText(QPoint(30 + 3, height + 2), str(abs(int(pitch))))
                self.qp.drawText(QPoint(-40, height + 2), str(abs(int(pitch))))

            mode = (mode + 1) % 4

        # draw the static roll arc
        self.setPen(3, Qt.white)

        bondingRect = QRectF(
            -self.rollArcRadius,
            -self.rollArcRadius,
            2 * self.rollArcRadius,
            2 * self.rollArcRadius,
        )
        self.qp.drawArc(bondingRect, 30 * 16, 120 * 16)

        # draw the Roll angle arc markers
        rollangleindicator = [
            [-30, 10],
            [-45, 5],
            [-135, 5],
            [-150, 10],
            [-60, 10],
            [-70, 5],
            [-80, 5],
            [-100, 5],
            [-110, 5],
            [-120, 10],
        ]

        self.qp.setBrush(QBrush(Qt.white))
        self.setPen(2, Qt.white)
        for lineParam in rollangleindicator:
            self.qp.drawLine(self.alongRadiusCoord(lineParam[0], lineParam[1]))

        # draw the diamond on top of the roll arc
        self.qp.drawPolygon(
            QPolygonF(
                [
                    QPointF(
                        0,
                        -self.rollArcRadius,
                    ),
                    QPointF(-diamondWidth / 2, -self.rollArcRadius - diamondHeight),
                    QPointF(+diamondWidth / 2, -self.rollArcRadius - diamondHeight),
                ]
            )
        )

        self.qp.resetTransform()

        # create the fixed diamond
        fixedDiamond = QPolygonF(
            [
                QPointF(g5CenterX, g5CenterY - self.rollArcRadius),
                QPointF(
                    g5CenterX + diamondWidth / 2,
                    g5CenterY - self.rollArcRadius + diamondHeight,
                ),
                QPointF(
                    g5CenterX - diamondWidth / 2,
                    g5CenterY - self.rollArcRadius + diamondHeight,
                ),
            ]
        )

        self.qp.drawPolygon(fixedDiamond)

        # create the nose
        self.qp.setBrush(QBrush(Qt.yellow))
        self.qp.setBackgroundMode(Qt.OpaqueMode)

        self.setPen(1, Qt.black)

        # solid polygon left
        nose = QPolygonF(
            [
                QPointF(g5CenterX - 1, g5CenterY + 1),
                QPointF(g5CenterX - 75, g5CenterY + 38),
                QPointF(g5CenterX - 54, g5CenterY + 38),
            ]
        )
        self.qp.drawPolygon(nose)

        # solid polygon right
        nose = QPolygonF(
            [
                QPointF(g5CenterX + 1, g5CenterY + 1),
                QPointF(g5CenterX + 75, g5CenterY + 38),
                QPointF(g5CenterX + 54, g5CenterY + 38),
            ]
        )
        self.qp.drawPolygon(nose)

        # solid marker left
        marker = QPolygonF(
            [
                QPointF(120, g5CenterY - 5),
                QPointF(155, g5CenterY - 5),
                QPointF(160, g5CenterY),
                QPointF(155, g5CenterY + 5),
                QPointF(120, g5CenterY + 5),
            ]
        )
        self.qp.drawPolygon(marker)

        # solid marker right
        marker = QPolygonF(
            [
                QPointF(360, g5CenterY - 5),
                QPointF(325, g5CenterY - 5),
                QPointF(320, g5CenterY),
                QPointF(325, g5CenterY + 5),
                QPointF(360, g5CenterY + 5),
            ]
        )
        self.qp.drawPolygon(marker)

        brush = QBrush(QColor(0x7E, 0x7E, 0x34, 255))
        self.qp.setBrush(brush)

        # cross pattern polygon left
        nose = QPolygonF(
            [
                QPointF(g5CenterX - 2, g5CenterY + 2),
                QPointF(g5CenterX - 33, g5CenterY + 38),
                QPointF(g5CenterX - 54, g5CenterY + 38),
            ]
        )
        self.qp.drawPolygon(nose)

        # cross pattern polygon right
        nose = QPolygonF(
            [
                QPointF(g5CenterX + 2, g5CenterY + 2),
                QPointF(g5CenterX + 33, g5CenterY + 38),
                QPointF(g5CenterX + 54, g5CenterY + 38),
            ]
        )
        self.qp.drawPolygon(nose)

        self.setPen(0, Qt.transparent)
        # solid polygon right
        nose = QPolygonF(
            [
                QPointF(120, g5CenterY),
                QPointF(160, g5CenterY),
                QPointF(155, g5CenterY + 5),
                QPointF(120, g5CenterY + 5),
            ]
        )
        self.qp.drawPolygon(nose)
        # solid polygon right
        nose = QPolygonF(
            [
                QPointF(360, g5CenterY),
                QPointF(320, g5CenterY),
                QPointF(325, g5CenterY + 5),
                QPointF(360, g5CenterY + 5),
            ]
        )
        self.qp.drawPolygon(nose)

        #################################################
        # SPEED TAPE
        #################################################

        speedBoxLeftAlign = 7
        speedBoxHeight = 50
        speedBoxSpikedimension = 10

        speedDeltaWidth = 4

        tapeScale = 50

        self.setPen(0, Qt.transparent)

        self.qp.setBrush(QBrush(QColor(0, 0, 0, 90)))
        self.qp.drawRect(0, 0, speedBoxLeftAlign + speedBoxWidth + 15, g5Height-tasHeight)

        self.setPen(2, Qt.white)

        self.qp.setBackgroundMode(Qt.TransparentMode)
        font = self.qp.font()
        font.setPixelSize(speedBoxHeight - 15)

        # set default font size
        self.qp.setFont(font)

        currentTape = int(self.airspeed + tapeScale / 2)
        while currentTape > max(0, self.airspeed - tapeScale / 2):
            if (currentTape % 10) == 0:

                tapeHeight = (
                    1 - 2 * (currentTape - self.airspeed) / tapeScale
                ) * g5CenterY
                self.qp.drawLine(
                    QPointF(speedBoxLeftAlign + speedBoxWidth + 5, tapeHeight),
                    QPointF(speedBoxLeftAlign + speedBoxWidth + 15, tapeHeight),
                )

                self.qp.drawText(
                    QRectF(
                        speedBoxLeftAlign,
                        tapeHeight - speedBoxHeight / 2,
                        speedBoxWidth,
                        speedBoxHeight,
                    ),
                    Qt.AlignRight | Qt.AlignVCenter,
                    "{:d}".format(int(currentTape)),
                )

            elif (currentTape % 5) == 0:
                self.qp.drawLine(
                    QPointF(
                        speedBoxLeftAlign + speedBoxWidth + 8,
                        (1 - 2 * (currentTape - self.airspeed) / tapeScale) * g5CenterY,
                    ),
                    QPointF(
                        speedBoxLeftAlign + speedBoxWidth + 15,
                        (1 - 2 * (currentTape - self.airspeed) / tapeScale) * g5CenterY,
                    ),
                )

            currentTape -= 1

        speedBox = QPolygonF(
            [
                QPointF(speedBoxLeftAlign, g5CenterY + speedBoxHeight / 2),
                QPointF(
                    speedBoxLeftAlign + speedBoxWidth, g5CenterY + speedBoxHeight / 2
                ),
                QPointF(
                    speedBoxLeftAlign + speedBoxWidth,
                    g5CenterY + speedBoxSpikedimension,
                ),
                QPointF(
                    speedBoxLeftAlign + speedBoxWidth + speedBoxSpikedimension,
                    g5CenterY,
                ),
                QPointF(
                    speedBoxLeftAlign + speedBoxWidth,
                    g5CenterY - speedBoxSpikedimension,
                ),
                QPointF(
                    speedBoxLeftAlign + speedBoxWidth, g5CenterY - speedBoxHeight / 2
                ),
                QPointF(speedBoxLeftAlign, g5CenterY - speedBoxHeight / 2),
            ]
        )

        self.setPen(2, Qt.white)

        brush = QBrush(QColor(0, 0, 0, 255))
        self.qp.setBrush(brush)

        self.qp.drawPolygon(speedBox)

        font = self.qp.font()
        font.setPixelSize(speedBoxHeight - 10)
        # set default font size
        self.qp.setFont(font)

        self.qp.drawText(
            QRectF(
                speedBoxLeftAlign,
                g5CenterY - speedBoxHeight / 2,
                speedBoxWidth,
                speedBoxHeight,
            ),
            Qt.AlignHCenter | Qt.AlignVCenter,
            "{:03d}".format(int(self.airspeed)),
        )

        # draw the Ground Speed box on top
        rect = QRectF(
            0,
            0,
            speedBoxLeftAlign + speedBoxWidth + 15,
            tasHeight,
        )
        self.qp.drawRect(rect)

        font = self.qp.font()
        font.setPixelSize(20)
        # set default font size
        self.qp.setFont(font)

        self.qp.drawText(
            rect,
            Qt.AlignHCenter | Qt.AlignVCenter,
            "GS {:03d}".format(int(self.gndspeed)),
        )

        # draw the satellites count
        pixmap = QPixmap(self.ctx.get_resource('attitude_ind_widget/satellite.png'))
        x = speedBoxWidth + 28
        self.qp.drawPixmap(x, g5Height - tasHeight - 25, 22, 22, pixmap)

        rect = QRectF(
            x + 22,
            g5Height - tasHeight - 25,
            25,
            25,
            )
        font = self.qp.font()
        font.setPixelSize(15)
        self.qp.setFont(font)
        self.qp.drawText(
            rect,
            Qt.AlignHCenter | Qt.AlignVCenter,
            ": {}".format(int(self.sat_count))
            )


        #################################################
        # Alpha and Beta
        #################################################

        taller_height = 10
        smaller_height = 5
        max_span = 50
        offset = 5
        poly_thc = 5

        # Beta (-5 to +5 degrees)
        max_beta = 5
        val_range = 2 * max_beta
        small_gap = max_span / 5

        self.setPen(2, Qt.white)
        self.qp.drawLine(
            QPointF(g5CenterX - max_span, g5Height - tasHeight - offset),
            QPointF(g5CenterX + max_span, g5Height - tasHeight - offset),
            )
        for sign in (0, -1, 1):
            z = 1.2 if sign == 0 else 1
            self.qp.drawLine(
                QPointF(
                    g5CenterX + (sign * max_span),
                    g5Height - tasHeight - offset),
                QPointF(
                    g5CenterX + (sign * max_span),
                    g5Height - tasHeight - z * taller_height - offset),
                )
        for sign in (-1, 1):
            for val in range(5):
                self.qp.drawLine(
                    QPointF(
                        g5CenterX + (sign * val * small_gap),
                        g5Height - tasHeight - offset),
                    QPointF(
                        g5CenterX + (sign * val * small_gap),
                        g5Height - tasHeight - smaller_height - offset),
                    )


        beta = self.beta
        if self.beta > max_beta:
            beta = max_beta
        elif self.beta < -max_beta:
            beta = -max_beta
        beta_x = self.mapFromto(
            beta,
            -max_beta,
            max_beta,
            g5CenterX - max_span,
            g5CenterX + max_span,
            )
        beta_polygon = QPolygonF(
            [
                QPointF(beta_x, g5Height -tasHeight - offset),
                QPointF(beta_x + poly_thc, g5Height - tasHeight - offset - 2 * poly_thc),
                # QPointF(beta_x, g5Height - tasHeight - offset - 4 * poly_thc),
                QPointF(beta_x - poly_thc, g5Height - tasHeight - offset - 2 * poly_thc),
            ]
            )
        self.setPen(2, Qt.red)
        brush = QBrush(QColor(255, 0, 0))
        self.qp.setBrush(brush)
        self.qp.drawPolygon(beta_polygon)


        # Alpha (-5 to 15 deg)
        max_alpha = 15
        min_alpha = -5
        val_range = max_alpha - min_alpha
        al_x = g5Width - altBoxWidth - 5.5 * offset
        al_bottom = g5Height - tasHeight - offset
        al_top = g5CenterY + 8 * offset
        al_span = al_bottom - al_top
        al_gap = al_span / 4
        self.setPen(2, Qt.white)

        self.qp.drawLine(
            QPointF(al_x, al_top),
            QPointF(al_x, al_bottom),
            )
        for i in range(5):
            z = 1.5 if i == 3 else 1
            self.qp.drawLine(
                QPointF(
                    al_x,
                    al_top + i * al_gap,
                    ),
                QPointF(
                    al_x - z * taller_height,
                    al_top + i * al_gap),
                )
        for i in range(4):
            self.qp.drawLine(
                QPointF(
                    al_x,
                    al_top + al_gap / 2 + i * al_gap,
                    ),
                QPointF(
                    al_x - smaller_height,
                    al_top + al_gap / 2 + i * z * al_gap),
                )

        rect = QRectF(
            al_x - taller_height - 2.5 * offset,
            al_bottom - al_gap + 0.5 * offset,
            2 * offset,
            2 * offset,
            )
        font = self.qp.font()
        font.setPixelSize(12)
        self.qp.setFont(font)
        self.qp.drawText(
            rect,
            Qt.AlignHCenter | Qt.AlignVCenter,
            "0"
            )


        alpha = self.alpha
        if self.alpha > max_alpha:
            alpha = max_alpha
        elif self.alpha < min_alpha:
            alpha = min_alpha
        alpha_y = self.mapFromto(
            alpha,
            min_alpha,
            max_alpha,
            al_bottom,
            al_top,
            )
        alpha_polygon = QPolygonF(
            [
                QPointF(al_x, alpha_y),
                QPointF(al_x - 2 * poly_thc, alpha_y - poly_thc),
                QPointF(al_x - 2 * poly_thc, alpha_y + poly_thc),
            ]
            )
        self.setPen(2, Qt.red)
        brush = QBrush(QColor(255, 0, 0))
        self.qp.setBrush(brush)
        self.qp.drawPolygon(alpha_polygon)


        #################################################
        # ALTITUDE TAPE
        #################################################

        altBoxRightAlign = 7
        altBoxHeight = 40
        altBoxSpikedimension = 10
        altTapeScale = 500


        altTapeLeftAlign = g5Width - altBoxRightAlign - altBoxWidth
        alt_tape_height=g5Height #-tasHeight

        vsScale = 10
        vsIndicatorWidth = 7

        alttapteLeftBound = altTapeLeftAlign - 1.5 * altBoxSpikedimension
        self.setPen(0, Qt.transparent)
        self.qp.setBrush(QBrush(QColor(0, 0, 0, 90)))
        self.qp.drawRect(alttapteLeftBound, 0, g5Width - alttapteLeftBound, alt_tape_height)
        self.setPen(2, Qt.white)

        self.qp.setBackgroundMode(Qt.TransparentMode)
        font = self.qp.font()
        font.setPixelSize(10)
        # set default font size
        self.qp.setFont(font)

        # VS tape
        currentTape = vsScale

        while currentTape >= 0:
            tapeHeight = (vsScale - currentTape) / vsScale * alt_tape_height
            if (currentTape % 5) == 0:

                self.qp.drawLine(
                    QPointF(g5Width - 10, tapeHeight),
                    QPointF(g5Width, tapeHeight),
                )
                self.qp.drawText(
                    QRectF(
                        g5Width - 30,
                        tapeHeight - 5,
                        15,
                        vsIndicatorWidth + 3,
                    ),
                    Qt.AlignRight | Qt.AlignVCenter,
                    "{:d}".format(abs(int(currentTape - vsScale / 2))),
                )
            else:
                self.qp.drawLine(
                    QPointF(g5Width - vsIndicatorWidth, tapeHeight),
                    QPointF(g5Width, tapeHeight),
                )

            currentTape -= 1
        # tapeHeight = (vsScale - currentTape) / vsScale * g5Height
        vsHeight = -self.vspeed / 1 / vsScale * g5Height
        vsRect = QRectF(g5Width, g5CenterY, -vsIndicatorWidth, vsHeight)

        self.setPen(0, Qt.transparent)

        brush = QBrush(QColor(Qt.magenta))
        self.qp.setBrush(brush)

        self.qp.drawRect(vsRect)

        self.setPen(2, Qt.white)

        font = self.qp.font()
        font.setPixelSize(20)
        # set default font size
        self.qp.setFont(font)

        # altitude tape
        currentTape = int(self.altitude + altTapeScale / 2)

        while currentTape > self.altitude - altTapeScale / 2:
            if (currentTape % 20) == 0:

                tapeHeight = (
                    1 - 2 * (currentTape - self.altitude) / altTapeScale
                ) * g5CenterY
                self.qp.drawLine(
                    QPointF(altTapeLeftAlign - 1.5 * altBoxSpikedimension, tapeHeight),
                    QPointF(altTapeLeftAlign - altBoxSpikedimension / 2, tapeHeight),
                )
                if (currentTape % 100) == 0:

                    self.qp.drawText(
                        QRectF(
                            altTapeLeftAlign,
                            tapeHeight - speedBoxHeight / 2,
                            speedBoxWidth,
                            speedBoxHeight,
                        ),
                        Qt.AlignLeft | Qt.AlignVCenter,
                        "{:3d}".format(int(currentTape)),
                    )

            currentTape -= 1

        altBox = QPolygonF(
            [
                QPointF(g5Width - altBoxRightAlign, g5CenterY - altBoxHeight / 2),
                QPointF(
                    altTapeLeftAlign,
                    g5CenterY - altBoxHeight / 2,
                ),
                QPointF(
                    altTapeLeftAlign,
                    g5CenterY - altBoxSpikedimension,
                ),
                QPointF(
                    altTapeLeftAlign - altBoxSpikedimension,
                    g5CenterY,
                ),
                QPointF(
                    altTapeLeftAlign,
                    g5CenterY + altBoxSpikedimension,
                ),
                QPointF(
                    altTapeLeftAlign,
                    g5CenterY + altBoxHeight / 2,
                ),
                QPointF(g5Width - altBoxRightAlign, g5CenterY + altBoxHeight / 2),
            ]
        )

        brush = QBrush(QColor(0, 0, 0))
        self.qp.setBrush(brush)
        self.qp.drawPolygon(altBox)

        font = self.qp.font()
        font.setPixelSize(25)
        # set default font size
        self.qp.setFont(font)

        self.qp.drawText(
            QRectF(
                altTapeLeftAlign,
                g5CenterY - altBoxHeight / 2,
                altBoxWidth,
                altBoxHeight,
            ),
            Qt.AlignHCenter | Qt.AlignVCenter,
            "{:03d}".format(int(self.altitude)),
        )

        #################################################
        # Status Box
        #################################################

        font = self.qp.font()
        font.setPixelSize(20)
        # set default font size
        self.qp.setFont(font)

        # GNSS Status on the left
        rect = QRectF(
            0,
            g5Height - tasHeight,
            g5Width / 3,
            tasHeight,
        )
        self.setPen(2, Qt.transparent)
        self.qp.setBrush(QBrush(QColor(0, 0, 0, 200)))
        self.qp.drawRect(rect)

        f_gnss_fix = msg_decoder.findFix(self.gnss_fix)
        self.setPen(3, Qt.white)
        self.qp.drawText(
            rect,
            Qt.AlignCenter | Qt.AlignVCenter,
            f_gnss_fix,
        )

        # Arming Status on the center
        rect = QRectF(
            g5Width / 3,
            g5Height - tasHeight,
            g5Width / 3,
            tasHeight,
        )
        self.setPen(2, Qt.transparent)
        self.qp.drawRect(rect)

        if self.arm == 1:
            f_arm = "ARMED"
        else:
            f_arm = "DISARMED"
        self.setPen(3, Qt.white)
        self.qp.drawText(
            rect,
            Qt.AlignCenter | Qt.AlignVCenter,
            f_arm,
        )

        # Flight Mode on the right
        rect = QRectF(
            2 * g5Width / 3,
            g5Height - tasHeight,
            g5Width / 3,
            tasHeight,
        )
        self.setPen(2, Qt.transparent)
        self.qp.drawRect(rect)

        self.setPen(3, Qt.white)
        self.qp.drawText(
            rect,
            Qt.AlignCenter | Qt.AlignVCenter,
            str(self.mode),
        )

        self.qp.end()

    def mapFromto(self, x, a, b, c, d):
        """Maps data x originally in range[a, b] to a new range [c, d]"""
        y = (x-a)/(b-a)*(d-c) + c
        return y



    def pitchLine(self, offset, length):
        """Return a pitch line.
        As the pitch line is drawn using translate and rotate
        align the pitch line around the center
        Args:
            angle: in degrees
            length: in pixel
        Returns:
            Qline
        """
        pass

    def alongRadiusCoord(self, angle, length):
        """Return a line along the radius of the circle.
        Args:
            angle: in degrees
            length: in pixel
        Returns:
            Qline
        """
        startPoint = QPoint(
            int(self.rollArcRadius * cos(radians(angle))),
            int(self.rollArcRadius * sin(radians(angle))),
        )
        endPoint = QPoint(
            int((self.rollArcRadius + length) * cos(radians(angle))),
            int((self.rollArcRadius + length) * sin(radians(angle))),
        )

        return QLine(startPoint, endPoint)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')

    myApp = pyG5AIWidget()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
