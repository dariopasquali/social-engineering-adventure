from PySide2.QtCore import QObject, Slot, Signal, Property


class StoryBridge(QObject):

    def __init__(self, width=1000, height=1000):
        super().__init__()

        self.__width = width
        self.__height = height

        self.__storyLine = ""
        self.__btnContText = ""
        self.__btnLeftText = ""
        self.__btnRightText = ""
        self.__btnCentreText = ""

        self.__btnLeftVisible = False
        self.__btnRightVisible = False
        self.__btnContinueVisible = False
        self.__btnCentreVisible = False

        self.__btnLeftEnabled = True
        self.__btnRightEnabled = True
        self.__btnCentreEnabled = True

        self.__btnContinueCallback = None
        self.__btnLeftCallback = None
        self.__btnRightCallback = None
        self.__btnCentreCallback = None

    # region Signals

    widthChanged = Signal(int)
    heightChanged = Signal(int)

    storyLineChanged = Signal(str)
    btnContChanged = Signal(str)
    btnLeftChanged = Signal(str)
    btnRightChanged = Signal(str)
    btnCentreChanged = Signal(str)

    btnLeftVisibleChanged = Signal(bool)
    btnRightVisibleChanged = Signal(bool)
    btnContinueVisibleChanged = Signal(bool)
    btnCentreVisibleChanged = Signal(bool)

    btnLeftEnabledChanged = Signal(bool)
    btnRightEnabledChanged = Signal(bool)
    btnCentreEnabledChanged = Signal(bool)

    # endregion

    # region Setters - CHANGE TEXT

    def set_story_line(self, line):
        self.__storyLine = line
        self.storyLineChanged.emit(self.__storyLine)

    def append_story_line(self, line):
        #print("Append {}".format(line))
        self.__storyLine += "\n" + line
        self.storyLineChanged.emit(self.__storyLine)

    def set_btn_left_txt(self, txt):
        self.__btnLeftText = txt
        self.btnLeftChanged.emit(self.__btnLeftText)

    def set_btn_right_txt(self, txt):
        self.__btnRightText = txt
        self.btnRightChanged.emit(self.__btnRightText)

    def set_btn_continue_txt(self, txt):
        self.__btnContText = txt
        self.btnContChanged.emit(self.__btnContText)

    def set_btn_centre_txt(self, txt):
        self.__btnCentreText = txt
        self.btnCentreChanged.emit(self.__btnCentreText)
    # endregion

    # region Setters - BUTTON VISIBILITY

    def show_choice(self):
        self.set_btn_left_visible(True)
        self.set_btn_right_visible(True)

        self.set_btn_right_enabled(True)
        self.set_btn_left_enabled(True)

    def hide_choice(self):
        self.set_btn_left_visible(False)
        self.set_btn_right_visible(False)
        self.set_btn_centre_visible(False)

    def set_btn_right_enabled(self, status):
        self.__btnRightEnabled = status
        self.btnRightEnabledChanged.emit(self.__btnRightEnabled)

    def set_btn_left_enabled(self, status):
        self.__btnLeftEnabled = status
        self.btnLeftEnabledChanged.emit(self.__btnLeftEnabled)

    def set_btn_left_visible(self, state):
        self.__btnLeftVisible = state
        self.btnLeftVisibleChanged.emit(self.__btnLeftVisible)

    def set_btn_right_visible(self, state):
        self.__btnRightVisible = state
        self.btnRightVisibleChanged.emit(self.__btnRightVisible)

    def set_btn_continue_visible(self, state):
        self.__btnContinueVisible = state
        self.btnContinueVisibleChanged.emit(self.__btnContinueVisible)

    def set_btn_centre_enabled(self, status):
        self.__btnCentreEnabled = status
        self.btnCentreEnabledChanged.emit(self.__btnCentreEnabled)

    def set_btn_centre_visible(self, state):
        self.__btnCentreVisible = state
        self.btnCentreVisibleChanged.emit(self.__btnCentreVisible)

    # endregion

    # region Setters - CALLBACKS

    def set_continue_callback(self, callback):
        self.__btnContinueCallback = callback

    def set_right_callback(self, callback):
        self.__btnRightCallback = callback

    def set_left_callback(self, callback):
        self.__btnLeftCallback = callback

    def set_centre_callback(self, callback):
        self.__btnCentreCallback = callback

    # endregion

    # region Getters

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_story_line(self):
        return self.__storyLine

    def get_btn_continue_txt(self):
        return self.__btnContText

    def get_btn_left_txt(self):
        return self.__btnLeftText

    def get_btn_right_txt(self):
        return self.__btnRightText

    def get_btn_left_visible(self):
        return self.__btnLeftVisible

    def get_btn_right_visible(self):
        return self.__btnRightVisible

    def get_btn_continue_visible(self):
        return self.__btnContinueVisible

    def get_btn_left_enabled(self):
        return self.__btnLeftEnabled

    def get_btn_right_enabled(self):
        return self.__btnRightEnabled

    def get_btn_centre_txt(self):
        return self.__btnCentreText

    def get_btn_centre_visible(self):
        return self.__btnCentreVisible

    def get_btn_centre_enabled(self):
        return self.__btnCentreEnabled

    # endregion

    # region Properties

    width = Property(int, get_width, notify=widthChanged)
    height = Property(int, get_height, notify=heightChanged)

    lineText = Property(str, get_story_line, notify=storyLineChanged)
    btnContText = Property(str, get_btn_continue_txt, notify=btnContChanged)
    btnLeftText = Property(str, get_btn_left_txt, notify=btnLeftChanged)
    btnRightText = Property(str, get_btn_right_txt, notify=btnRightChanged)
    btnCentreText = Property(str, get_btn_centre_txt, notify=btnCentreChanged)

    btnLeftVisible = Property(bool, get_btn_left_visible, notify=btnLeftVisibleChanged)
    btnRightVisible = Property(bool, get_btn_right_visible, notify=btnRightVisibleChanged)
    btnContinueVisible = Property(bool, get_btn_continue_visible, notify=btnContinueVisibleChanged)
    btnCentreVisible = Property(bool, get_btn_centre_visible, notify=btnCentreVisibleChanged)

    btnLeftEnabled = Property(bool, get_btn_left_enabled, notify=btnLeftEnabledChanged)
    btnRightEnabled = Property(bool, get_btn_right_enabled, notify=btnRightEnabledChanged)
    btnCentreEnabled = Property(bool, get_btn_centre_enabled, notify=btnCentreEnabledChanged)

    # endregion

    # region Slots for callbacks

    @Slot()
    def onClickBtnContinue(self):
        self.__btnContinueCallback()

    @Slot()
    def onClickBtnLeft(self):
        self.__btnLeftCallback()

    @Slot()
    def onClickBtnRight(self):
        self.__btnRightCallback()

    @Slot()
    def onClickBtnCentre(self):
        self.__btnCentreCallback()

    # endregion