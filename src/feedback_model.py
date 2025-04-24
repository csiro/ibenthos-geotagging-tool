from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot


class FeedbackModel(QObject):
    feedbackTextChanged = pyqtSignal(str)
    progressChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._feedback_text = ""
        self._progress = 0

    @pyqtProperty(str, notify=feedbackTextChanged)
    def feedbackText(self):
        return self._feedback_text
    
    @feedbackText.setter
    def feedbackText(self, text):
        if self._feedback_text != text:
            self._feedback_text = text
            self.feedbackTextChanged.emit(text)

    @pyqtSlot(str)
    def addFeedbackLine(self, new_line):
        self.feedbackText += new_line + "\n"
    
    @pyqtProperty(int, notify=progressChanged)
    def progress(self):
        return self._progress
    
    @progress.setter
    def progress(self, value):
        if self._progress != value:
            self._progress = value
            self.progressChanged.emit(value)

    @pyqtSlot(int, int)
    def updateProgress(self, current_value, max_value):
        if max_value > 0:
            self.progress = int((current_value / max_value) * 100)
        else:
            self.progress = 0
