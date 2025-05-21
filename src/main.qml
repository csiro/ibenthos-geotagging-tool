import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts
import QtQuick.Dialogs
import QtQuick.Controls
import "Components" as Components

ApplicationWindow {
    visible: true
    width: 1200
    height: 600
    title: "iBenthos - PhotoTransect Tool build " + configModel.buildHash
    id: root

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent
        RowLayout {
            id: parentLayout
            Layout.fillHeight: true
            Layout.fillWidth: true

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
                    Layout.preferredWidth: 300
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

                CheckBox {
                    text: "Export as an iFDO dataset"
                    onToggled: {
                        userInputModel.ifdoEnable = checked
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
                    text: "iFDO details"
                    visible: userInputModel.ifdoEnable
                }

                Components.ConfigTextBox {
                    id: imageSetName
                    label: "Image set name:"
                    defaultValue: "i.e. date and site identification"
                    value: userInputModel.imageSetName
                    visible: userInputModel.ifdoEnable
                    configValue {
                        onEditingFinished: {
                            userInputModel.imageSetName = configValue.text
                        }
                    }
                }

                Components.ConfigTextBox {
                    id: imageContext
                    label: "Context:"
                    defaultValue: "i.e. seagrass surveying in North Sulawesi"
                    value: userInputModel.imageContext
                    visible: userInputModel.ifdoEnable
                    configValue {
                        onEditingFinished: {
                            userInputModel.imageContext = configValue.text
                        }
                    }
                }

                Components.ConfigTextBox {
                    id: projectName
                    label: "Project Name:"
                    defaultValue: "i.e. iBenthos"
                    value: userInputModel.projectName
                    visible: userInputModel.ifdoEnable
                    configValue {
                        onEditingFinished: {
                            userInputModel.projectName = configValue.text
                        }
                    }
                }

                Components.ConfigTextBox {
                    id: campaignName
                    label: "Campaign Name:"
                    defaultValue: "i.e. North Sulawesi June 2023"
                    value: userInputModel.campaignName
                    visible: userInputModel.ifdoEnable
                    configValue {
                        onEditingFinished: {
                            userInputModel.campaignName = configValue.text
                        }
                    }
                }

                Components.ConfigTextBox {
                    id: piName
                    label: "Principal Investigator's name:"
                    defaultValue: "Jane Smith"
                    widthRatio: 0.5
                    value: userInputModel.piName
                    visible: userInputModel.ifdoEnable
                    configValue {
                        onEditingFinished: {
                            userInputModel.piName = configValue.text
                        }
                    }
                }

                Components.ConfigTextBox {
                    id: piORCID
                    label: "PI's ORCID (optional):"
                    defaultValue: "0000-0000-0000-0000"
                    widthRatio: 0.5
                    value: userInputModel.piORCID
                    visible: userInputModel.ifdoEnable
                    configValue {
                        onEditingFinished: {
                            userInputModel.piORCID = configValue.text
                        }
                        validator: RegularExpressionValidator { 
                            regularExpression: /^(\d{4})-(\d{4})-(\d{4})-(\d{3}[\dX])$/ 
                        }
                    }
                }

                Components.ConfigTextBox {
                    id: collectorName
                    label: "Collector's name:"
                    defaultValue: "Jane Smith"
                    widthRatio: 0.5
                    value: userInputModel.collectorName
                    visible: userInputModel.ifdoEnable
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
                    visible: userInputModel.ifdoEnable
                    configValue {
                        onEditingFinished: {
                            userInputModel.collectorORCID = configValue.text
                        }
                        validator: RegularExpressionValidator { 
                            regularExpression: /^(\d{4})-(\d{4})-(\d{4})-(\d{3}[\dX])$/ 
                        }
                    }
                }

                Components.ConfigTextBox {
                    id: organisation
                    label: "Copyright owner:"
                    defaultValue: "University of the Sea"
                    widthRatio: 0.5
                    value: userInputModel.organisation
                    visible: userInputModel.ifdoEnable
                    configValue {
                        onEditingFinished: {
                            userInputModel.organisation = configValue.text
                        }
                    }
                }

                Components.ConfigTextBox {
                    id: license
                    label: "License:"
                    defaultValue: "CC BY 4.0"
                    widthRatio: 0.5
                    value: userInputModel.license
                    visible: userInputModel.ifdoEnable
                    configValue {
                        onEditingFinished: {
                            userInputModel.license = configValue.text
                        }
                    }
                }

                Components.ConfigTextBox {
                    id: distanceAG
                    label: "Distance above ground (m):"
                    defaultValue: "0.8"
                    widthRatio: 0.7
                    value: userInputModel.distanceAboveGround
                    visible: userInputModel.ifdoEnable
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
                    id: imageObjective
                    label: "Image objective:"
                    defaultValue: "Survey goal"
                    widthRatio: 0.3
                    value: userInputModel.imageObjective
                    visible: userInputModel.ifdoEnable
                    configValue {
                        onEditingFinished: {
                            userInputModel.imageObjective = configValue.text
                        }
                    }
                }

                Components.ConfigMultilineTextBox {
                    id: imageAbstract
                    label: "Image abstract:"
                    defaultValue: "Description of the image set"
                    value: userInputModel.imageAbstract
                    visible: userInputModel.ifdoEnable
                    configValue {
                        onEditingFinished: {
                            userInputModel.imageAbstract = configValue.text
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
                            // This ensures that the text fields have been loaded into the model
                            // before the geotagging process starts
                            var editable_fields = [
                                gpsDateTime.configDate,
                                gpsDateTime.configTime,
                                imageSetName.configValue,
                                imageContext.configValue,
                                projectName.configValue,
                                campaignName.configValue,
                                piName.configValue,
                                piORCID.configValue,
                                collectorName.configValue,
                                collectorORCID.configValue,
                                organisation.configValue,
                                license.configValue,
                                distanceAG.configValue,
                                imageObjective.configValue,
                                imageAbstract.configValue
                            ]
                            editable_fields.forEach( (x) => {
                                x.editingFinished()
                            });
                            controller.geotag()
                        }
                    }
                }
                ScrollView {
                    id: feedbackScroll
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredWidth: rightPane.Layout.maximumWidth
                    Layout.preferredHeight: rightPane.Layout.maximumHeight
                    clip: true

                    TextArea {
                        id: feebackText
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        placeholderText: "Feedback messages will be displayed here..."
                        text: feedbackModel.feedbackText
                        readOnly: true
                    }

                }
            }
        }
        ProgressBar {
            id: progressBar
            visible: true
            Layout.fillWidth: true
            height: 20
            value: feedbackModel.progress
            from: 0
            to: 100
        }
    }
} 

