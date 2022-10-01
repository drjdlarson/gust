import QtQuick 2.11
import QtPositioning 5.11
import QtLocation 5.14
import QtQuick.Window 2.2

Item {
    id:item
    width: 640
    height: 480


    property variant locationTC: QtPositioning.coordinate(33.2098, -87.5692)

    Map {
        id: mapBase
        anchors.fill: parent
        center: locationTC
        zoomLevel: 10
        copyrightsVisible: false
        plugin: Plugin {
            name: 'osm'
            PluginParameter {
                // name: 'osm.mapping.offline.directory'
                name: 'osm.mapping.custom.host'
                value: 'file:/offline_folders/'
            }

            PluginParameter {
                name: "osm.mapping.providersrepository.disabled"
                value: true
            }

        }
        activeMapType: mapBase.supportedMapTypes[supportedMapTypes.length - 1]
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
