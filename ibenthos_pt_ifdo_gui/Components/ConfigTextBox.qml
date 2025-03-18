import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts

Item {
    property alias label: configName.text
    property alias defaultValue: configValue.placeholderText
    property alias value: configValue.text
    property alias configName: configName
    property alias configValue: configValue
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
            id: configValue
            Layout.minimumWidth: parent.width*(1-widthRatio-0.1)
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight
        }

    }
}
