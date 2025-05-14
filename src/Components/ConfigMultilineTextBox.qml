import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts

Item {
    property alias label: configName.text
    property alias defaultValue: configValue.placeholderText
    property alias value: configValue.text
    property alias configName: configName
    property alias configValue: configValue
    Layout.minimumWidth: parent.width
    Layout.minimumHeight: 100
    ColumnLayout {
        anchors.fill: parent
        Text {
            id: configName
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 25
            Layout.fillWidth: true
        }

        ScrollView {
            id: scrollview
            Layout.minimumWidth: parent.width
            Layout.fillWidth: true
            Layout.minimumHeight: 75
            Layout.maximumHeight: 75
            TextArea {
                id: configValue
                Layout.minimumWidth: parent.width
                Layout.fillWidth: true
                Layout.minimumHeight: 75
                Layout.maximumHeight: 75
                wrapMode: TextArea.Wrap
            }
        }

    }
}
