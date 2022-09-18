import QtQuick 2.11
import QtPositioning 5.11
import QtLocation 5.11
import QtQuick.Window 2.2

Item {
    id:item
    width: 640
    height: 480
    Plugin {
        id: osmPlugin
        name: "osm" //"googlemaps"
    }
    property variant locationTC: QtPositioning.coordinate(44.951, -93.192)

    Map {
        id: mapBase
        anchors.fill: parent
        plugin: osmPlugin
        center: locationTC
        zoomLevel: 10
        // activeMapType: MapType.SatelliteMapDay
    }

    Map {
        id: mapOverlay
        anchors.fill: parent
        plugin: Plugin { name: "itemsoverlay" }
        gesture.enabled: false
        center: mapBase.center
        color: 'transparent' // Necessary to make this map transparent
        minimumFieldOfView: mapBase.minimumFieldOfView
        maximumFieldOfView: mapBase.maximumFieldOfView
        minimumTilt: mapBase.minimumTilt
        maximumTilt: mapBase.maximumTilt
        minimumZoomLevel: mapBase.minimumZoomLevel
        maximumZoomLevel: mapBase.maximumZoomLevel
        zoomLevel: mapBase.zoomLevel
        tilt: mapBase.tilt;
        bearing: mapBase.bearing
        fieldOfView: mapBase.fieldOfView
        z: mapBase.z + 1



        MapItemView{
            model: markermodel
            delegate: MapQuickItem {
                coordinate: model.position_marker
                anchorPoint.x: image.width
                anchorPoint.y: image.height
                sourceItem:
                    Image { id: image; source: model.source_marker }

            }
        }


        // The code below enables SSAA
        layer.enabled: true
        layer.smooth: false
        property int w : mapOverlay.width
        property int h : mapOverlay.height
        property int pr: Screen.devicePixelRatio
        layer.textureSize: Qt.size(w  * 2 * pr, h * 2 * pr)
    }
}
