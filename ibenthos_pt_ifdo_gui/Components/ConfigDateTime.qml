import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts

Item {
    property alias label: configName.text
    property alias date: configDate.text
    property alias time: configTime.text
    property alias configDate: configDate
    property alias configTime: configTime
    property real widthRatio: 0.3
    Layout.minimumWidth: parent.width
    Layout.minimumHeight: 25
    RowLayout {
        anchors.fill: parent
        Text {
            id: configName
            Layout.minimumWidth: parent.width*widthRatio
            Layout.fillWidth: true
        }

        TextField {
            id: configDate
            Layout.minimumWidth: parent.width*((1-widthRatio-0.1)/2)
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight
            placeholderText: "YYYY-MM-DD"
            inputMethodHints: Qt.ImhDate
            validator: RegularExpressionValidator { 
                regularExpression: /^(\d{4})-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$/ 
            }
        }

        TextField {
            id: configTime
            Layout.minimumWidth: parent.width*((1-widthRatio-0.1)/2)
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight
            placeholderText: "HH:MM:SS"
            inputMethodHints: Qt.ImhTime
            validator: RegularExpressionValidator { 
                regularExpression: /^(0[0-9]|[0-9]|1[0-9]|2[0-3]):([0-9]|[0-5][0-9]):([0-9]|[0-5][0-9])$/ 
            }
        }

    }
}
