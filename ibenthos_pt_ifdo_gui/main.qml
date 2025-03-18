import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts
import QtQuick.Dialogs
import QtQuick.Controls
import "Components" as Components
// import QtLocation 6.8
// import QtPositioning 5.5

ApplicationWindow {
    visible: true
    width: 1200
    height: 600
    title: "iBenthos - PhotoTransect processor"
    id: root
    property variant timezones: ["None"]


    RowLayout {
        id: parentLayout
        anchors.fill: parent

        ColumnLayout {
            id: leftPane
            Layout.fillHeight: true
            Layout.minimumWidth: root.width*0.3
            Layout.alignment: Qt.AlignTop

            RowLayout {
                id: importDirectoryPrompt
                Layout.minimumWidth: parent.width
                
                Text {
                    id: inputTextField
                    Layout.minimumWidth: parent.width*0.2
                    text: "Input directory: "
                }

                TextField {
                    id: importDirPathField
                    Layout.minimumWidth: parent.width*0.4
                    Layout.alignment: Qt.AlignRight
                    Layout.fillWidth: true
                    placeholderText: "Select an input directory..."
                }

                Button {
                    text: "Browse"
                    Layout.minimumWidth: parent.width*0.2
                    Layout.alignment: Qt.AlignRight
                    onClicked: importDirectory.open()
                }

                FolderDialog {
                    id: importDirectory
                    title: "Select a directory"
                    onAccepted: {
                        importDirPathField.text = importDirectory.currentFolder
                        gpxFile.currentFolder = importDirectory.currentFolder
                        gpsPhoto.currentFolder = importDirectory.currentFolder
                    }
                }
            }

            RowLayout {
                id: gpxFilePrompt
                width: leftPane.Layout.maximumWidth

                Text {
                    id: gpxTextField
                    Layout.minimumWidth: parent.width*0.2
                    text: "GPX file: "
                }

                TextField {
                    id: gpxFilePathField
                    Layout.minimumWidth: parent.width*0.5
                    placeholderText: "Select a GPX file..."
                    Layout.alignment: Qt.AlignRight
                    Layout.fillWidth: true
                }

                Button {
                    text: "Browse"
                    Layout.minimumWidth: parent.width*0.2
                    onClicked: gpxFile.open()
                    Layout.alignment: Qt.AlignRight
                }

                FileDialog {
                    id: gpxFile
                    title: "Select a GPX file"
                    nameFilters: ["GPX files (*.gpx)"]
                    onAccepted: {
                        gpxFilePathField.text = gpxFile.selectedFile
                        mainModel.onGpxFileSelected(gpxFile.selectedFile)
                    }
                }
            }

            RowLayout {
                id: gpsPhotoPrompt
                width: leftPane.Layout.maximumWidth

                Text {
                    id: gpsPhotoTextField
                    Layout.minimumWidth: parent.width*0.2
                    text: "GPS photo: "
                }

                TextField {
                    id: gpsPhotoPathField
                    Layout.alignment: Qt.AlignRight
                    Layout.fillWidth: true
                    placeholderText: "Select a GPS photo..."
                }

                Button {
                    text: "Browse"
                    Layout.minimumWidth: parent.width*0.2
                    Layout.alignment: Qt.AlignRight
                    onClicked: gpsPhoto.open()
                }

                FileDialog {
                    id: gpsPhoto
                    title: "Select a GPS photo"
                    nameFilters: ["Image files (*.jpg *.jpeg *.png *.bmp)"]
                    onAccepted: {
                        gpsPhotoPathField.text = gpsPhoto.selectedFile
                        gpsDateTime.visible = true
                        gpsTimezonePrompt.visible = true
                    }
                }
            }

            Image {
                source: gpsPhotoPathField.text
                Layout.preferredWidth: 400
                Layout.preferredHeight: 300
                Layout.alignment: Qt.AlignHCenter
                fillMode: Image.PreserveAspectFit
                asynchronous: true
            }

            Components.ConfigDateTime {
                id: gpsDateTime
                label: "Date time on GPS:"
                visible: false
                configDate {
                    onEditingFinished: {
                        dataCollectionStartDateTime.date = gpsDateTime.date
                        dataCollectionEndDateTime.date = gpsDateTime.date
                    }
                }
            }

            RowLayout {
                id: gpsTimezonePrompt
                width: leftPane.Layout.maximumWidth
                visible: false

                Text {
                    id: gpsTimezoneText
                    text: "Timezone: "
                }

                ComboBox {
                    id: gpsTimezoneInput
                    model: timezones
                    currentIndex: 0
                    editable: true
                }
            }

            RowLayout {
                id: exportDirectoryPrompt
                Layout.minimumWidth: parent.width
                
                Text {
                    id: outputTextField
                    Layout.minimumWidth: parent.width*0.2
                    text: "Output directory: "
                }

                TextField {
                    id: exportDirPathField
                    // width: exportDirectoryPrompt.width
                    placeholderText: "Select an output directory..."
                    Layout.alignment: Qt.AlignRight
                    Layout.fillWidth: true
                }

                Button {
                    text: "Browse"
                    Layout.minimumWidth: parent.width*0.2
                    Layout.alignment: Qt.AlignRight
                    onClicked: exportDirectory.open()
                }

                FolderDialog {
                    id: exportDirectory
                    title: "Select a directory"
                    onAccepted: {
                        exportDirPathField.text = exportDirectory.currentFolder
                    }
                }
            }
        }

        ColumnLayout {
            id: middlePane
            Layout.fillHeight: true
            Layout.minimumWidth: root.width*0.3
            Layout.alignment: Qt.AlignTop

            Text {
                id: siteDetailsTitle
                width: middlePane.Layout.maximumWidth
                text: "Site details"
            }

            RowLayout {
                id: sitePointPrompt
                Layout.minimumWidth: parent.width
                
                Text {
                    id: sitePointText
                    width: sitePointPrompt.width*0.2
                    text: "Site coordinates:"
                }

                TextField {
                    id: siteLatitudeField
                    width: sitePointPrompt.width*0.4
                    placeholderText: "Latitude"
                }

                TextField {
                    id: siteLongitudeField
                    width: sitePointPrompt.width*0.4
                    placeholderText: "Longitude"
                }
            }

            Components.ConfigTextBox {
                id: projectName
                label: "Project Name:"
                defaultValue: "iBenthos"
            }

            Components.ConfigTextBox {
                id: campaignName
                label: "Campaign Name:"
                defaultValue: "North Sulawesi 2023"
            }

            Components.ConfigTextBox {
                id: siteID
                label: "Site ID:"
                defaultValue: "NS01"
            }

            Text {
                id: dataCollectionTitle
                width: middlePane.Layout.maximumWidth
                text: "Data collection details"
            }

            Components.ConfigDateTime {
                id: dataCollectionStartDateTime
                label: "Start time:"
            }

            Components.ConfigDateTime {
                id: dataCollectionEndDateTime
                label: "End time:"
            }

            Components.ConfigTextBox {
                id: cameraID
                label: "Camera ID:"
                defaultValue: "1"
                widthRatio: 0.7
            }

            Components.ConfigTextBox {
                id: distanceAG
                label: "Dist. above ground (m):"
                defaultValue: "0.8"
                widthRatio: 0.7
            }

            Components.ConfigTextBox {
                id: collectorName
                label: "Collector's name:"
                defaultValue: "Jane Smith"
                widthRatio: 0.5
            }

            Components.ConfigTextBox {
                id: collectorORCID
                label: "Collector's ORCID (optional):"
                defaultValue: "0000-0000-0000-0000"
                widthRatio: 0.5
            }

            Components.ConfigTextBox {
                id: organisation
                label: "Organisation:"
                defaultValue: "University of the Sea"
                widthRatio: 0.5
            }
        }

        ColumnLayout {
            id: rightPane
            Layout.fillHeight: true
            Layout.minimumWidth: root.width*0.3
            // Layout.minimumWidth: 400
        }
    }

    Connections {
        target: mainModel
        function onAvgLatitudeChanged(latitude) {
            siteLatitudeField.text = latitude
        }
        function onAvgLongitudeChanged(longitude) {
            siteLongitudeField.text = longitude
        }
    }

} 

