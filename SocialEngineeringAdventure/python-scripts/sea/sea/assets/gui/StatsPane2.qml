// StatsPane.qml
import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11

Item {
    objectName: "paneStats"
    id: paneStats
    width: 640
    height: 1080

    //width: statsBridge.width
    //height: statsBridge.height

    property var labelFont: 20

    ColumnLayout {
        id: statsCols
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.fill: parent
        anchors.margins: 10

        Text {
            id: lblStats
            Layout.fillWidth: true
            height: 100
            text: qsTr("Statistiche")
            font.pixelSize: 25
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.bold: true
            color: "#ffffff"
        }

        Row {
            id: rowEq
            Rectangle {
                width: labelFont
                height: labelFont
                color: "blue"
            }

            Text {
                text: "Energia Quantica:"
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: labelFont
                font.bold: true
                color: "#ffffff"
            }

            Text {
                text: statsBridge.energy
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: labelFont
                color: "#ffffff"
            }
            spacing: 10
        }

        Row {
            id: rowPower
            Rectangle {
                width: labelFont
                height: labelFont
                color: "red"
            }

            Text {
                text: "Attacco:"
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: labelFont
                font.bold: true
                color: "#ffffff"
            }

            Text {
                text: statsBridge.power
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: labelFont
                color: "#ffffff"
            }
            spacing: 10
        }

        Text {
            id: lblItems
            Layout.fillWidth: true
            height: 100
            text: qsTr("Inventario")
            font.pixelSize: 25
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.bold: true
            color: "#ffffff"
        }

        ListView {
            id: listItems
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: statsBridge.model
            anchors.topMargin: 195

            ScrollBar.vertical: ScrollBar {}


            delegate: Item {
                x: 5
                Layout.fillHeight: true
                height: labelFont*2
                Row {
                    id: itemRow
                    spacing: 15

                    Button{
                        onPressed : {
                            statsBridge.onItemUsed(name, index)
                        }
                        Image {
                            anchors.rightMargin: 0
                            anchors.bottomMargin: 0
                            anchors.leftMargin: 0
                            anchors.topMargin: 0
                            source: "../images/btn_right_2.jpg";
                            anchors.fill: parent;
                        }

                        contentItem: Label {
                            font.pixelSize: labelFont
                            text: "Usa"
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            color: "#ffffff"
                        }
                    }

                    Button{

                        contentItem: Label {
                            font.pixelSize: labelFont
                            text: "?"
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            color: "#ffffff"
                        }

                        onPressed : {
                            statsBridge.onItemInspect(name, index)
                            popupObj.open()
                        }
                        Image {
                            anchors.rightMargin: 0
                            anchors.bottomMargin: 0
                            anchors.leftMargin: 0
                            anchors.topMargin: 0
                            source: "../images/btn_right_2.jpg";
                            anchors.fill: parent;
                        }
                    }

                    Text {
                        text: name
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: labelFont
                        color: "#ffffff"
                    }

                    Text {
                        text: qta
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: labelFont
                        color: "#ffffff"
                        visible: qtaVisible
                    }
                }
            }
        }

        Image{
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            transformOrigin: Item.Center
            Layout.preferredHeight: 500
            Layout.preferredWidth: 640
            source: statsBridge.image
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.maximumWidth: 640
            Layout.maximumHeight: 500

            visible: statsBridge.imageVisible
        }
    }

    Text{
        x: 30
        y: 691
        text: qsTr(statsBridge.countdown)
        font.weight: Font.Bold
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        font.pixelSize: 200
        color: "#f7f300"
        //visible: true
        visible: statsBridge.countdownVisible
    }



}


