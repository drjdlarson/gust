import sys
import math
import io
import matplotlib.image as mpimg
from scipy import ndimage
import folium # pip install folium
from PyQt5.QtWidgets import QLineEdit, QLCDNumber, QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from gust.gui.msg_decoder import MessageDecoder as msg_decoder

"""
Folium in PyQt5
"""


class MapWidget(QWidget):
    def __init__(self, parent):
        self.drone_icon_list = []
        super().__init__(parent=parent)

        self.setWindowTitle('Folium in PyQt')

        layout = QVBoxLayout()
        self.setLayout(layout)

        m = folium.Map(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            zoom_start=12,
            #location=[self.latitude, self.longitude]
        )

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)


        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())

        layout.addWidget(self.webView)

    def clear_drone_list(self):
        self.drone_icon_list = []

    def add_drone(self, name, latitude, longitude, heading, track, mode, ctx):
        self.drone_icon_list.append(DroneHelper(name, latitude, longitude, heading, track, mode, ctx))

    def update_map(self):
        map_kwargs = dict(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        zoom_start=12,
        )
        if len(self.drone_icon_list) > 0:
            latitude = 0
            longitude = 0
            for drone in self.drone_icon_list:
                latitude += drone.latitude
                longitude += drone.longitude

            latitude /= len(self.drone_icon_list)
            longitude /= len(self.drone_icon_list)
            map_kwargs['location'] = [latitude, longitude]

        m = folium.Map(**map_kwargs)

        for drone in self.drone_icon_list:
            drone.update_map(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        #self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())

class DroneHelper():
    def __init__(self, name, latitude, longitude, heading, track, mode, ctx):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.heading = heading
        self.track = track
        self.mode = mode
        self.ctx = ctx

    def update_map(self, m):
        self.icon = self.icon_selector()
        marker = folium.Marker(
            location=[self.latitude, self.longitude],
            tooltip=self.name,
            popup=self.name,
            icon=folium.features.CustomIcon(ndimage.rotate(self.icon, 360 - (self.heading % 360)),
                                              icon_size=(30, 30),
                                             )
        )
        marker.add_to(m)

        heading_points = self.get_points(self.heading)
        heading_line = folium.PolyLine(
            [(self.latitude, self.longitude),
             (heading_points)],
            color = 'crimson'
            )
        heading_line.add_to(m)

        track_points = self.get_points(self.track)
        track_line = folium.PolyLine(
            [(self.latitude, self.longitude),
             (track_points)],
            color = 'white'
            )
        track_line.add_to(m)

    def get_points(self, angle):
        R = 6378.1
        dis = 5
        angle = math.radians(angle)
        lat_1 = math.radians(self.latitude)
        lon_1 = math.radians(self.longitude)
        lat_2 = math.asin(math.sin(lat_1) * math.cos(dis / R) + math.cos(lat_1) * math.sin(dis / R) * math.cos(angle))
        lon_2 = lon_1 + math.atan2(math.sin(angle) * math.sin(dis / R) * math.cos(lat_1),
                                   math.cos(dis / R) - math.sin(lat_1) * math.sin(lat_2))
        lat_2 = math.degrees(lat_2)
        lon_2 = math.degrees(lon_2)

        return lat_2, lon_2

    def icon_selector(self):
        mode = msg_decoder.findMode(int(self.mode))
        if mode in ("Test", "Stabilize", "Manual", "None"):
            icon_type = mpimg.imread(self.ctx.get_resource('map_widget/greenarrow.png'))
        elif mode == "Guided":
            icon_type = mpimg.imread(self.ctx.get_resource('map_widget/bluearrow.png'))
        elif mode in ("Auto", "Simulation"):
            icon_type = mpimg.imread(self.ctx.get_resource('map_widget/redarrow.png'))
        return icon_type
