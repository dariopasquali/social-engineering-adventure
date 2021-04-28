// StoryPane.qml
import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11

Item {
    objectName: "paneStory"
    id: paneStory
    width: 1280
    height: 1080


    property var labelFont: 18

    //width: storyBridge.width
    //height: storyBridge.height
    transformOrigin: Item.Center

    Rectangle {
        id: rectangle
        x: 0
        y: 0
        width: 1280
        height: 418
        Image {
            source: "../images/sea_text_background.jpg";
            anchors.fill: parent;
        }
    }

    Text {
        id: lblStory
        x: 20
        y: 8
        width: 1238
        height: 410
        color: "#ffffff"
        text: qsTr(storyBridge.lineText)
        font.pixelSize: 20
        Layout.minimumHeight: 0
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        wrapMode: Text.WordWrap
    }

    Button {
        id: btnCnt
        x: 484
        y: 476
        width: 312
        height: 74
        scale: 1.2
        onPressed : {
            storyBridge.onClickBtnContinue()
        }

        visible: storyBridge.btnContinueVisible
        contentItem: Label {

            font.pixelSize: labelFont
            text: qsTr(storyBridge.btnContText)
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            color: "#ffffff"

        }

        Image {
            source: "../images/sea_button.png";
            anchors.fill: parent;
        }
        background: Rectangle {color: "transparent"}

    }

    Button {
        id: btnB
        x: 929
        y: 876
        width: 310
        height: 166
        onPressed : {
            storyBridge.onClickBtnRight()
        }

        visible: storyBridge.btnRightVisible
        enabled: storyBridge.btnRightEnabled

        contentItem: Label {
            font.pixelSize: labelFont
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            color: "#ffffff"
            text: qsTr(storyBridge.btnRightText)
        }

        Image {
            source: "../images/sea_button_left.png";
            anchors.fill: parent;
        }
        background: Rectangle {color: "transparent"}
    }

    Button {
        id: btnA
        x: 43
        y: 876
        width: 310
        height: 166
        onPressed : {
            storyBridge.onClickBtnLeft()
        }

        visible: storyBridge.btnLeftVisible
        enabled: storyBridge.btnLeftEnabled

        contentItem: Label {
            text: qsTr(storyBridge.btnLeftText)
            rightPadding: -3
            leftPadding: 0
            font.pixelSize: labelFont
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            color: "#ffffff"
        }

        Image {
            source: "../images/sea_button_left.png";
            anchors.fill: parent;
        }
        background: Rectangle {color: "transparent"}

    }

    Button {
        id: btnC
        x: 485
        y: 876
        width: 310
        height: 166
        contentItem: Label {
            text: qsTr(storyBridge.btnCentreText)
            wrapMode: Text.WordWrap
            font.pixelSize: labelFont
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "#ffffff"
        }
        visible: storyBridge.btnCentreVisible

        onPressed : {
            storyBridge.onClickBtnCentre()
        }

        Image {
            source: "../images/sea_button_left.png";
            anchors.fill: parent;
        }
        background: Rectangle {color: "transparent"}
    }


}



/*##^##
Designer {
    D{i:0;formeditorZoom:0.6600000262260437}D{i:3;anchors_height:410;anchors_width:1264;anchors_x:8;anchors_y:8}
D{i:4;anchors_height:40;anchors_width:312;anchors_x:299;anchors_y:364}
}
##^##*/
