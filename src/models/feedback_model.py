"""
feeback_model.py: This moudule defines a data model for feedback and progress tracking.

Copyright (c) 2025
Commonwealth Scientific and Industrial Research Organisation (CSIRO)
ABN 41 687 119 230

Author: Brendan Do <brendan.do@csiro.au>
"""
from PySide6.QtCore import Property, QObject, Signal, Slot


class FeedbackModel(QObject):
    """
    FeedbackModel: A model to manage feedback text and progress updates.
    This model provides properties for feedback text and progress, along with methods
    to update these properties. It emits signals when the feedback text or progress changes.
    """
    # pylint: disable=invalid-name
    # Camel case to comply with pyside6 naming conventions

    # pylint: disable=missing-function-docstring
    # Setters and getters are self-explanatory and do not require additional documentation

    feedbackTextChanged = Signal(str)
    progressChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self._feedback_text = ""
        self._progress = 0

    @Property(str, notify=feedbackTextChanged)
    def feedbackText(self): # pylint: disable=method-hidden # getter method, not redefined
        return self._feedback_text

    @feedbackText.setter
    def feedbackText(self, text):
        if self._feedback_text != text:
            self._feedback_text = text
            self.feedbackTextChanged.emit(text)

    @Slot(str)
    def addFeedbackLine(self, new_line):
        """
        This method appends a new line to the existing feedback text.
        Args:
            new_line (str): The new line of feedback to append.
        """
        self.feedbackText += new_line + "\n"

    @Property(int, notify=progressChanged)
    def progress(self): # pylint: disable=method-hidden # getter method, not redefined
        return self._progress

    @progress.setter
    def progress(self, value):
        if self._progress != value:
            self._progress = value
            self.progressChanged.emit(value)

    @Slot(int, int)
    def updateProgress(self, current_value, max_value):
        """
        This method updates the progress value based on the current and maximum values.
        Args:
            current_value (int): The current progress value.
            max_value (int): The maximum value for progress calculation.
        """
        if max_value > 0:
            self.progress = int((current_value / max_value) * 100)
        else:
            self.progress = 0
