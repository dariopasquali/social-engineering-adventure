// StoryPane.qml
import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11

Item {
    objectName: "paneStory"
    id: paneStory
    width: 1280
    height: 1080

    //width: 910
    //height: 768

    GridLayout {
        id: grid
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.fill: parent
        anchors.margins: 10

        anchors.verticalCenterOffset: 0
        anchors.horizontalCenterOffset: 0

        columns: 14
        rows: 14

        property var alpha_color : "transparent"
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        anchors.bottomMargin: -1
        anchors.topMargin: 0
        antialiasing: true
        columnSpacing: 0
        rowSpacing: 0
        Rectangle {
            id: spaceTop
            color: "#ff1919"
            Layout.minimumWidth: 12
            Layout.row: 0
            Layout.column: 0
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 12
            Layout.rowSpan: 1
            Layout.preferredWidth: 12
            Layout.preferredHeight: 1
        }


        Rectangle {
            id: spaceBfLbl
            color: "#ff1919"
            Layout.row: 1
            Layout.column: 0
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 1
            Layout.rowSpan: 3
            Layout.preferredWidth: 1
            Layout.preferredHeight: 3
        }

        Text {
            id: lblStory
            text: qsTr(storyBridge.lineText)
            Layout.minimumHeight: 0
            font.pixelSize: 15
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            wrapMode: Text.WordWrap
            Layout.row: 1
            Layout.column: 1
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 10
            Layout.rowSpan: 3
            Layout.preferredWidth: 9
            Layout.preferredHeight: 2
        }


        Rectangle {
            id: spaceAftLbl
            color: "#ff1919"
            Layout.row: 1
            Layout.column: 11
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 1
            Layout.rowSpan: 3
            Layout.preferredWidth: 1
            Layout.preferredHeight: 3
        }


        Rectangle {
            id: spaceMiddle
            //anchors.fill: parent
            //color: "#ffaaaa"
            color: "#0074d9"
            Layout.row: 4
            Layout.column: 0
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 12
            Layout.rowSpan: 1
            Layout.preferredWidth: 12
            Layout.preferredHeight: 1
        }


        Rectangle {
            id: spaceBfBtn
            color: "#ff1919"
            Layout.fillWidth: true
            Layout.row: 5
            Layout.fillHeight: true
            Layout.preferredWidth: 5
            Layout.preferredHeight: 1
            Layout.rowSpan: 1
            Layout.columnSpan: 5
            Layout.column: 0
        }

        Button {
            id: btnCnt
            text: qsTr(storyBridge.btnContText)
            Layout.row: 5
            Layout.column: 5
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 2
            Layout.rowSpan: 1
            Layout.preferredWidth: 2
            Layout.preferredHeight: 1
            onPressed : {
                storyBridge.onClickBtnContinue()
            }

            visible: storyBridge.btnContinueVisible
            Component.onCompleted: contentItem.wrapMode = Text.WordWrap
        }

        Rectangle {
            id: spaceAftBtn
            color: "#ff1919"
            Layout.fillWidth: true
            Layout.row: 5
            Layout.column: 7
            Layout.fillHeight: true
            Layout.preferredWidth: 5
            Layout.preferredHeight: 1
            Layout.columnSpan: 5
            Layout.rowSpan: 1

        }


        Rectangle {
            id: spaceMiddle2
            //anchors.fill: parent
            //color: "#ffaaaa"
            color: "#38ff19"
            Layout.row: 6
            Layout.column: 0
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 12
            Layout.rowSpan: 2
            Layout.preferredWidth: 12
            Layout.preferredHeight: 2
        }


        Rectangle {
            id: spaceBottm1
            color: "#ff1919"
            Layout.fillWidth: true
            Layout.row: 8
            Layout.fillHeight: true
            Layout.preferredWidth: 1
            Layout.preferredHeight: 3
            Layout.rowSpan: 3
            Layout.columnSpan: 1
            Layout.column: 0
        }

        Button {
            id: btnA
            text: qsTr(storyBridge.btnLeftText)
            font.weight: Font.Normal
            display: AbstractButton.TextOnly
            Layout.row: 8
            Layout.column: 1
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 3
            Layout.rowSpan: 3
            Layout.preferredWidth: 3
            Layout.preferredHeight: 3
            onPressed : {
                storyBridge.onClickBtnLeft()
            }

            visible: storyBridge.btnLeftVisible
            enabled: storyBridge.btnLeftEnabled

            Component.onCompleted: contentItem.wrapMode = Text.WordWrap

        }

        Rectangle {
            id: spaceBottom2
            color: "#ff1919"
            Layout.fillWidth: true
            Layout.row: 8
            Layout.fillHeight: true
            Layout.preferredWidth: 4
            Layout.preferredHeight: 3
            Layout.rowSpan: 3
            Layout.columnSpan: 4
            Layout.column: 4
        }

        Button {
            id: btnB
            text: qsTr(storyBridge.btnRightText)
            display: AbstractButton.TextOnly
            Layout.row: 8
            Layout.column: 8
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 3
            Layout.rowSpan: 3
            Layout.preferredWidth: 3
            Layout.preferredHeight: 3

            onPressed : {
                storyBridge.onClickBtnRight()
            }

            visible: storyBridge.btnRightVisible
            enabled: storyBridge.btnRightEnabled

            Component.onCompleted: contentItem.wrapMode = Text.WordWrap
        }

        Rectangle {
            id: spaceBottom3
            color: "#ff1919"
            Layout.fillWidth: true
            Layout.row: 8
            Layout.fillHeight: true
            Layout.preferredWidth: 1
            Layout.preferredHeight: 1
            Layout.rowSpan: 3
            Layout.columnSpan: 1
            Layout.column: 11
        }

        Rectangle {
            id: spaceBottom
            color: "#04ffd2"
            Layout.row: 11
            Layout.column: 0
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 12
            Layout.rowSpan: 1
            Layout.preferredWidth: 12
            Layout.preferredHeight: 1
        }

    }
}



/*##^##
Designer {
    D{i:0;formeditorZoom:0.8999999761581421}
}
##^##*/
