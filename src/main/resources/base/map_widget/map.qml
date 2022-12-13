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
            latitude: 33.21456
            longitude: -87.54322
        }
    }

// FOR TESTING WITH OPENSTREETMAP
/*
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
        mapBase.center = mapCenter.coordinate
        mapBase.zoomLevel = 16
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
/*
            PluginParameter {
                name: "osm.mapping.cache.directory"
                value: "CACHE_FilledByMapWidget"
            }
*/
        }
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
            model: yaw_line
            remove: myTrans
            delegate: MapPolyline {
                id: yaw_line
                line.width: 3
                line.color: yaw_color
                path: model.yaw_path
            }
        }

        // 2 coordinates can be passed from map_widget
        MapItemView{
            model: heading_line
            remove: myTrans
            delegate: MapPolyline {
                id: heading_line
                line.width: 3
                line.color: heading_color
                path: heading_path
            }
        }

        MapItemView{
            model: markermodel
            remove: myTrans
            delegate: MapQuickItem {
                coordinate: position_marker
                // coordinate: {33.2098, -87.5692}
                //coordinate: QtPositioning.coordinate(33.21534, -87.54355)
                anchorPoint.x: image.width/2
                anchorPoint.y: image.height/2
                autoFadeIn: false
                sourceItem:
                    Image {
                        id: image
                        //anchors.fill: parent
                        source: source_marker
                        sourceSize.width: 30
                        sourceSize.height: 30
                        width: 30
                        height: 30
                        // rotation: model.rotation_marker
                        transform: Rotation {origin.x: width/2; origin.y: height/2; angle: rotation_marker}
                        }
            }
        }

        MapItemView{
            model: homemodel
            remove: myTrans
            delegate: MapQuickItem {
                coordinate: position_home
                anchorPoint.x: image.width/2
                anchorPoint.y: image.height/2
                autoFadeIn: false
                sourceItem:
                    Image {
                        id: image
                        //anchors.fill: parent
                        source: source_home
                        sourceSize.width: 30
                        sourceSize.height: 30
                        width: 30
                        height: 30
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
