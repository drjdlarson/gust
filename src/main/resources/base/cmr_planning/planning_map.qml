import QtQuick 2.11
import QtPositioning 5.11
import QtLocation 5.14
import QtQuick.Window 2.2

Item {
    id:item
    width: 640
    height: 480
    focus: true

    Location {
        id: mapCenter
        coordinate {
            latitude: 33.19424
            longitude: -87.48138
        }
    }

    Keys.onSpacePressed: {
        mapBase.center = mapCenter.coordinate
        mapBase.zoomLevel = 16
        // mapBase.fitViewportToVisibleMapItems()
        // var point = mapBase.fromCoordinate(locationTC, false)
        // mapBase.toCoordinate(point, false)
    }


    Plugin {
        id: osmPlugin
        name: "osm" //"googlemaps"
    }

    Map {
        id: mapBase
        anchors.fill: parent
        plugin: osmPlugin
        // anchors.centerIn: parent
        center: mapCenter.coordinate
        zoomLevel: 13
        copyrightsVisible: false
        // activeMapType: MapType.CustomMap
    }

/*
     Map {
        id: mapBase
        anchors.fill: parent
        anchors.centerIn: parent;
        center: mapCenter.coordinate
        zoomLevel: 15
        activeMapType: mapBase.supportedMapTypes[supportedMapTypes.length - 1]
        // activeMapType: mapBase.supportedMapTypes[1]
        copyrightsVisible: false
        
        plugin: Plugin {
            name: 'osm'
            PluginParameter {
                name: 'osm.mapping.custom.host'
                value: 'file:MAP_FilledByMapWidget'
            }

            PluginParameter {
                name: "osm.mapping.providersrepository.disabled"
                value: false
            }

            PluginParameter {
                name: 'osm.mapping.cache.memory_size'
                value: 0
            }

            PluginParameter {
                name: "osm.mapping.cache.directory"
                value: "CACHE_FilledByMapWidget"
            }
        }
    }
*/

    Transition {
        id: myTrans
        NumberAnimation {
            properties: "x,y"
            easing.type: Easing.InOutExpo
            duration: 1
        }
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
/*
        MapPolyline {
            line.width: 3
            line.color: line_item.color
            path: line_item.path
        }
*/
        MapItemView{
            model: line_model
            remove: myTrans
            delegate: MapPolyline {
                id: path_line
                line.width: 3
                line.color: line_color
                path: line_path
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
