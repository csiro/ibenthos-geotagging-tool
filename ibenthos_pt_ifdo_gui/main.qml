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
    title: "iBenthos - PhotoTransect Tool"
    id: root


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
                    text: userInputModel.importDirectory
                    readOnly: true
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
                        userInputModel.importDirectory = importDirectory.currentFolder
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
                    text: userInputModel.gpxFilepath
                    readOnly: true
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
                        userInputModel.gpxFilepath = gpxFile.selectedFile
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
                    text: userInputModel.gpsPhotoFilepath
                    readOnly: true
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
                        userInputModel.gpsPhotoFilepath = gpsPhoto.selectedFile
                        gpsDateTime.visible = true
                        gpsTimezonePrompt.visible = true
                    }
                }
            }

            Image {
                id: gpsPhotoPreview
                source: userInputModel.gpsPhotoFilepath
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
                date: userInputModel.gpsDate
                time: userInputModel.gpsTime
                configDate {
                    onEditingFinished: {
                        userInputModel.gpsDate = configDate.text
                    }
                }
                configTime {
                    onEditingFinished: {
                        userInputModel.gpsTime = configTime.text
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
                    model: configModel.gpsTimezoneOptions
                    currentIndex: userInputModel.gpsTimezoneIndex
                    // editable: true
                    onActivated: {
                        userInputModel.gpsTimezoneIndex = gpsTimezoneInput.currentIndex
                    }

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
                    readOnly: true
                    text: userInputModel.exportDirectory
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
                        userInputModel.exportDirectory = exportDirectory.currentFolder
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
                    Layout.minimumWidth: parent.width*0.2
                    text: "Site coordinates:"
                }

                TextField {
                    id: siteLatitudeField
                    Layout.minimumWidth: parent.width*0.25
                    placeholderText: "Latitude"
                    text: userInputModel.siteLatitude
                    onEditingFinished: {
                        userInputModel.siteLatitude = siteLatitudeField.text
                    }
                    validator: RegularExpressionValidator { 
                        regularExpression: /^[+-]?([0-9]*[.])?[0-9]+$/ 
                    }
                }

                TextField {
                    id: siteLongitudeField
                    Layout.minimumWidth: parent.width*0.25
                    placeholderText: "Longitude"
                    text: userInputModel.siteLongitude
                    onEditingFinished: {
                        userInputModel.siteLongitude = siteLongitudeField.text
                    }
                    validator: RegularExpressionValidator { 
                        regularExpression: /^[+-]?([0-9]*[.])?[0-9]+$/ 
                    }
                }
            }

            Components.ConfigTextBox {
                id: projectName
                label: "Project Name:"
                defaultValue: "iBenthos"
                value: userInputModel.projectName
                configValue {
                    onEditingFinished: {
                        userInputModel.projectName = configValue.text
                    }
                }
            }

            Components.ConfigTextBox {
                id: campaignName
                label: "Campaign Name:"
                defaultValue: "North Sulawesi 2023"
                value: userInputModel.campaignName
                configValue {
                    onEditingFinished: {
                        userInputModel.campaignName = configValue.text
                    }
                }
            }

            Components.ConfigTextBox {
                id: siteID
                label: "Site ID:"
                defaultValue: "NS01"
                value: userInputModel.siteID
                configValue {
                    onEditingFinished: {
                        userInputModel.siteID = configValue.text
                    }
                }
            }

            Text {
                id: dataCollectionTitle
                width: middlePane.Layout.maximumWidth
                text: "Data collection details"
            }

            Components.ConfigDateTime {
                id: dataCollectionStartDateTime
                label: "Start time:"
                date: userInputModel.collectionStartDate
                time: userInputModel.collectionStartTime
                configDate {
                    onEditingFinished: {
                        userInputModel.collectionStartDate = configDate.text
                    }
                }
                configTime {
                    onEditingFinished: {
                        userInputModel.collectionStartTime = configTime.text
                    }
                }
            }

            Components.ConfigDateTime {
                id: dataCollectionEndDateTime
                label: "End time:"
                date: userInputModel.collectionEndDate
                time: userInputModel.collectionEndTime
                configDate {
                    onEditingFinished: {
                        userInputModel.collectionEndDate = configDate.text
                    }
                }
                configTime {
                    onEditingFinished: {
                        userInputModel.collectionEndTime = configTime.text
                    }
                }
            }

            Components.ConfigTextBox {
                id: cameraID
                label: "Camera ID:"
                defaultValue: "1"
                widthRatio: 0.7
                value: userInputModel.cameraID
                configValue {
                    onEditingFinished: {
                        userInputModel.cameraID = configValue.text
                    }
                }
            }

            Components.ConfigTextBox {
                id: distanceAG
                label: "Dist. above ground (m):"
                defaultValue: "0.8"
                widthRatio: 0.7
                value: userInputModel.distanceAboveGround
                configValue {
                    onEditingFinished: {
                        userInputModel.distanceAboveGround = configValue.text
                    }
                    validator: RegularExpressionValidator { 
                        regularExpression: /^([0-9]*[.])?[0-9]+$/ 
                    }
                }
            }

            Components.ConfigTextBox {
                id: collectorName
                label: "Collector's name:"
                defaultValue: "Jane Smith"
                widthRatio: 0.5
                value: userInputModel.collectorName
                configValue {
                    onEditingFinished: {
                        userInputModel.collectorName = configValue.text
                    }
                }
            }

            Components.ConfigTextBox {
                id: collectorORCID
                label: "Collector's ORCID (optional):"
                defaultValue: "0000-0000-0000-0000"
                widthRatio: 0.5
                value: userInputModel.collectorORCID
                configValue {
                    onEditingFinished: {
                        userInputModel.collectorORCID = configValue.text
                    }
                    validator: RegularExpressionValidator { 
                        regularExpression: /^(\d{4})-(\d{4})-(\d{4})-(\d{4})$/ 
                    }
                }
            }

            Components.ConfigTextBox {
                id: organisation
                label: "Organisation:"
                defaultValue: "University of the Sea"
                widthRatio: 0.5
                value: userInputModel.organisation
                configValue {
                    onEditingFinished: {
                        userInputModel.organisation = configValue.text
                    }
                }
            }
        }

        ColumnLayout {
            id: rightPane
            Layout.fillHeight: true
            Layout.minimumWidth: root.width*0.33
            RowLayout {
                id: controlRow
                Layout.minimumWidth: parent.width
                
                Button {
                    text: "Clear Form"
                    Layout.minimumWidth: parent.width*0.3
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        userInputModel.clearForm()
                        gpsDateTime.visible = false
                        gpsTimezonePrompt.visible = false
                        gpsPhotoPreview.source = ""
                    }
                }

                Button {
                    text: "Start processing"
                    Layout.minimumWidth: parent.width*0.3
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        if (userInputModel.validateForm()) {
                            console.log("Form validated")
                        } else {
                            console.log("Form not validated")
                        }
                    }
                }
            }
        }
    }
} 

