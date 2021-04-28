// StatsPane.qml
import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11

Item {
    objectName: "paneStats"
    id: paneStats
    width: 640
    height: 1080

    //width: 455
    //height: 768

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
        }

        Row {
            id: rowEq
            Rectangle {
                width: labelFont
                height: labelFont
                color: "red"
            }

            Text {
                text: "Energia Quantica:"
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: labelFont
                font.bold: true
            }

            Text {
                text: statsBridge.energy
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: labelFont
            }

            Button{
                text: "Consuma"
                visible: false
                font.pixelSize: labelFont
            }

            spacing: 10
        }

        /*Row {
            id: rowCoin
            Rectangle {
                width: labelFont
                height: labelFont
                color: "yellow"
            }

            Text {
                text: "Crediti:"
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: labelFont
                font.bold: true
            }

            Text {
                text: statsBridge.money
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: labelFont
            }
            spacing: 10
        }*/

        Row {
            id: rowPower
            Rectangle {
                width: labelFont
                height: labelFont
                color: "blue"
            }

            Text {
                text: "Potenza:"
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: labelFont
                font.bold: true
            }

            Text {
                text: statsBridge.power
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: labelFont
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
        }

        ListView {
            id: listItems
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: statsBridge.model
            anchors.topMargin: 195


            delegate: Item {
                x: 5
                Layout.fillHeight: true
                height: labelFont*2
                Row {
                    id: itemRow
                    spacing: 15

                    Button{
                        text: "Usa"
                        font.pixelSize: labelFont
                        font.bold: true
                        onPressed : {
                            statsBridge.onItemUsed(name, index)
                        }
                    }

                    Button{
                        text: "?"
                        font.pixelSize: labelFont
                        font.bold: true
                        onPressed : {
                            statsBridge.onItemInspect(name, index)
                        }
                    }

                    Text {
                        text: name
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: labelFont
                        font.bold: true
                    }

                    Text {
                        text: qta
                        anchors.verticalCenter: parent.verticalCenter
                        font.bold: false
                        font.pixelSize: labelFont
                    }


                }
            }

        }

        Image{
            source: statsBridge.image
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.maximumWidth: 450
            Layout.maximumHeight: 450

            visible: statsBridge.imageVisible


        }

    }








    /*
    ColumnLayout{
        id: lateralTab
        anchors.fill: parent
        anchors.margins: 10

        Text {
            id: lblStats
            Layout.fillWidth: true
            height: 100
            text: qsTr("Statistiche")
            font.pixelSize: 20
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.bold: true
        }

        ListView {
            id: listStats

            Layout.fillWidth: true
            Layout.fillHeight: true

            delegate: Item {
                x: 5
                Layout.fillHeight: true
                height: labelFont + 10
                Row {
                    id: row1
                    Rectangle {
                        width: labelFont
                        height: labelFont
                        color: colorCode
                    }

                    Text {
                        text: name
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: labelFont
                    }

                    Text {
                        text: valore
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: labelFont
                    }


                    spacing: 10
                }
            }
            model: ListModel {
                ListElement {
                    name: "Energia Quantica"
                    valore: 10
                    colorCode: "red"
                }

                ListElement {
                    name: "Crediti"
                    valore: 10
                    colorCode: "yellow"
                }

                ListElement {
                    name: "Potenza"
                    valore: 10
                    colorCode: "blue"
                }
            }
        }

        Text {
            id: lblItems
            Layout.fillWidth: true
            height: 100
            text: qsTr("Inventario")
            font.pixelSize: 20
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.bold: true
        }

        ListView {
            id: listItems
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: ListModel {
                ListElement {
                    valore: 5
                    name: "Pozioni di Cura"
                }

                ListElement {
                    valore: 1
                    name: "Pistola"
                }

                ListElement {
                    valore: 2
                    name: "Spada Laser"
                }

                ListElement {
                    valore: 2
                    name: "Granata quantica"
                }
            }
            anchors.topMargin: 195
            delegate: Item {
                x: 5
                Layout.fillHeight: true
                height: labelFont + 10
                Row {
                    id: row2
                    spacing: 10
                    Text {
                        text: name
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: labelFont
                    }

                    Text {
                        text: valore
                        anchors.verticalCenter: parent.verticalCenter
                        font.bold: false
                        font.pixelSize: labelFont
                    }
                }
            }
        }

    }
    */







}


