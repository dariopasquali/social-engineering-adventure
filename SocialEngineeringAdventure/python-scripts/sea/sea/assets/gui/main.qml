import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11
import QtQuick.Window 2.2

ApplicationWindow {
    id: storyWindow
    objectName: "storyWindow"
    width: 1920
    height: 1080
    color: "#19313d"

    visible: true
    title: qsTr("SEAdventure")

    //visibility: "FullScreen"
    RowLayout{
        StoryPane2{
            id: storyPane
            objectName: "storyPane"
        }

        StatsPane2{
            id: statsMenu
            objectName: "statsPane"
        }
    }

    Button {
        id: btnHelpOpen
        x: 1811
        y: 14
        text: "Open"
        onClicked: popup.open()
        Image {
            anchors.rightMargin: 0
            anchors.bottomMargin: 0
            anchors.leftMargin: 0
            anchors.topMargin: 0
            source: "../images/btn_right_2.jpg";
            anchors.fill: parent;
        }

        contentItem: Label {
            text: "AIUTO"
            font.pixelSize: 16
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            color: "#ffffff"
        }
    }

    Popup {
        Button {
            id: btnPopupObjClose
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
                    text: "CHIUDI"
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    color: "#ffffff"
                }
                onClicked: popupObj.close()
            }

            id: popupObj
            x: 0
            y: 0
            width: 1280
            height: 1080
            modal: true
            focus: true
            background: Rectangle {
                    color: "#19313d"
                    border.color: "#19313d"
                }
            Text{
                    font.pixelSize: 25
                    text: qsTr(statsBridge.objectDescription)
                    anchors.topMargin: 0
                    wrapMode: Text.WordWrap
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    color: "#ffffff"
                    anchors.fill: parent
                }
            closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent | btnPopupObjClose.clicked()
     }


    Popup {
        Button {
            id: btnPopupClose
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
                    text: "CHIUDI"
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    color: "#ffffff"
                }
                onClicked: popup.close()
            }

            id: popup
            x: 0
            y: 0
            width: 1280
            height: 1080
            modal: true
            focus: true
            background: Rectangle {
                    color: "#19313d"
                    border.color: "#19313d"
                }
            Text{
                    font.pixelSize: 25
                    text: "- Non hai limiti di tempo per scegliere ma ogni decisione è irreversibile. Quindi <b>scegli con attenzione</b><br><br>

                            - A volte sarà il caso a decidere per te: ti verrà chiesto di lanciare un <b>dado virtuale</b> che deciderà lo svolgimento della storia<br><br>

                            - Dovrai anche combattere con <b>creature ostili</b> potrai raccogliere ed equipaggiare oggetti che ti aiuteranno a sconfiggerle.<br><br>

                            - Durante l'avventura dovrai gestire una risorsa molto importante l'<b>Energia Quantica (EQ)</b>. Se la tua <b>EQ</b> scende a 0 <b>avrai perso</b> e il gioco finirà immediatamente!<br><br>

                            - <b>Se perdi non riceverai alcun compenso al termine dell'avventura</b><br><br>

                            - Maggiore l' Energia Quantica rimasta a fine partita più alto sarà il tuo punteggio. Se vuoi, pubblicheremo online il tuo punteggio assieme a quello degli altri giocatori<br><br>

                            - Non preoccuparti per iCub, il suo ruolo diventerà chiaro iniziata l'avventura<br><br>"
                    anchors.topMargin: 0
                    wrapMode: Text.WordWrap
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    color: "#ffffff"
                    anchors.fill: parent
                }
            closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent | btnPopupClose.clicked()
     }
}



/*##^##
Designer {
    D{i:0;formeditorZoom:0.6600000262260437}
}
##^##*/
