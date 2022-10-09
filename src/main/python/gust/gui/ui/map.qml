import QtQuick 2.11
import QtPositioning 5.11
import QtLocation 5.14
import QtQuick.Window 2.2

Item {
    id:item
    width: 640
    height: 480
    focus: true

    property variant locationTC: QtPositioning.coordinate(33.2098, -87.5692)

    Location {
        id: mapCenter
        coordinate {
            latitude: 33.2098
            longitude: -87.5612
        }
    }


/*

// FOR TESTING WITH OPENSTREETMAP
    Plugin {
        id: osmPlugin
        name: "osm" //"googlemaps"
            PluginParameter {
            name: "osm.mapping.custom.host"
            value: "https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/4/7/4"
        }
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
*/


    Keys.onSpacePressed: {
        console.log(mapBase.center)
        mapBase.center = mapCenter.coordinate
        mapBase.zoomLevel = 15
        // mapBase.fitViewportToVisibleMapItems()

        // var point = mapBase.fromCoordinate(locationTC, false)
        // mapBase.toCoordinate(point, false)
    }


     Map {
        id: mapBase
        anchors.fill: parent
        anchors.centerIn: parent;
        center: mapCenter.coordinate
        zoomLevel: 15
        copyrightsVisible: false
        plugin: Plugin {
            name: 'osm'

            PluginParameter {
                // name: 'osm.mapping.offline.directory'
                name: 'osm.mapping.custom.host'
                // value: 'file://home/lagerprocessor/Projects/gust/src/main/python/gust/gui/ui/offline_folders/'
                value: 'file:/home/lagerprocessor/Projects/gust/src/main/python/gust/gui/ui/offline_folders/'
            }

            PluginParameter {
                name: "osm.mapping.providersrepository.disabled"
                value: true
            }
            PluginParameter {
                name: 'osm.mapping.cache.memory_size'
                value: 0
            }

            PluginParameter {
                name: "osm.mapping.cache.directory"
                value: "file://home/lagerprocessor/Projects/gust/src/main/python/gust/gui/ui/cache_testing"
            }

/*
            PluginParameter {
                name: "osm.mapping.custom.host"
                value: "http://a.tile.openstreetmap.fr/hot/"
            }
*/
        }
        activeMapType: mapBase.supportedMapTypes[supportedMapTypes.length - 1]
        // activeMapType: mapBase.supportedMapTypes[1]
    }


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


        // 2 coordinates can be passed from map_widget
        MapItemView{
            model: heading_line
            remove: myTrans
            delegate: MapPolyline {
                id: heading_line
                line.width: 3
                line.color: 'crimson'
                path: model.heading_path
            }
        }

        // 2 coordinates can be passed from map_widget
        MapItemView{
            model: track_line
            remove: myTrans
            delegate: MapPolyline {
                id: heading_line
                line.width: 3
                line.color: 'yellow'
                path: model.track_path
            }
        }

        MapItemView{
            model: markermodel
            remove: myTrans
            delegate: MapQuickItem {
                coordinate: model.position_marker
                // coordinate: {33.2098, -87.5692}
                //coordinate: QtPositioning.coordinate(33.21534, -87.54355)
                anchorPoint.x: image.width/2
                anchorPoint.y: image.height/2
                autoFadeIn: false
                sourceItem:
                    Image {
                        id: image
                        //anchors.fill: parent
                        source: model.source_marker
                        sourceSize.width: 30
                        sourceSize.height: 30
                        width: 30
                        height: 30
                        // rotation: model.rotation_marker
                        transform: Rotation {origin.x: width/2; origin.y: height/2; angle: model.rotation_marker}
                        }
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
