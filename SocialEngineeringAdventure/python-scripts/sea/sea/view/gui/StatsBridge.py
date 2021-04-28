from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2 import QtCore


class ItemsModel(QtCore.QAbstractListModel):
    NameRole = QtCore.Qt.UserRole + 1000
    QtaRole = QtCore.Qt.UserRole + 1001
    QtaVisibleRole = QtCore.Qt.UserRole + 1001

    def __init__(self, entries, parent=None):
        super(ItemsModel, self).__init__(parent)
        self._entries = entries

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._entries)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount() and index.isValid():
            item = self._entries[index.row()]
            if role == ItemsModel.NameRole:
                return item["name"]
            elif role == ItemsModel.QtaRole:
                return item["qta"]
            elif role == ItemsModel.QtaVisibleRole:
                return item["qtaVisible"]

    def roleNames(self):
        roles = dict()
        roles[ItemsModel.NameRole] = b"name"
        roles[ItemsModel.QtaRole] = b"qta"
        roles[ItemsModel.QtaVisibleRole] = b"qtaVisible"
        return roles

    def add(self, name, qta, qtaVisible):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._entries.append(dict(name=name, qta=qta, qtaVisible=qtaVisible))
        self.endInsertRows()

    def remove(self, index):
        #print("Finished, remove {}".format(index))
        self.beginRemoveRows(QtCore.QModelIndex(), index, index)
        self.endRemoveRows()

    def consume(self, name, row_index):

        print("Use {}".format(name))

        to_remove = False
        id_to_remove = -1
        for id, item in enumerate(self._entries):
            if item["name"] == name:
                qta = item["qta"]
                if qta <= 1:
                    to_remove = True
                    id_to_remove = id
                else:
                    item["qta"] = qta - 1
                    print("Remaining {}".format(qta - 1))

        if (to_remove):
            self.remove(row_index)
            self._entries.pop(id_to_remove)

        self.dataChanged.emit(self.createIndex(row_index, 0), self.createIndex(row_index, 0), [ItemsModel.QtaRole])

    def clear(self):
        while len(self._entries) > 0:
            self.remove(0)
            self._entries.pop(0)


class StatsBridge(QObject):

    def __init__(self, width=1000, height=1000):
        super().__init__()

        self.__width = width
        self.__height = height

        self.__energy = 10
        self.__money = 10
        self.__power = 10

        self.image_path = ""
        self.__image = ""
        self.__imageVisible = False

        self.__countdown = "00:00"
        self.__countdownVisible = False

        self.__objectDescription = ""

        entries = [
        ]
        self._model = ItemsModel(entries)

        self.update_engine_callback = None
        self.show_item_callback = None
        self.fetch_stats_callback = None

        self.__notify_view()



    # Signals

    widthChanged = Signal(int)
    heightChanged = Signal(int)

    energyChanged = Signal(int)
    moneyChanged = Signal(int)
    powerChanged = Signal(int)

    imgChanged = Signal(str)
    imgVisibleChanged = Signal(bool)

    countdownChanged = Signal(str)
    countdownVisibleChanged = Signal(bool)

    objectDescriptionChanged = Signal(str)

    # Setters

    def set_update_engine_callback(self, callback):
        self.update_engine_callback = callback

    def set_show_item_callback(self, callback):
        self.show_item_callback = callback

    def set_fetch_stats_callback(self, callback):
        self.fetch_stats_callback = callback

    def set_image_path(self, path):
        self.image_path = path

    def set_energy(self, energy):
        self.__energy = energy
        self.energyChanged.emit(self.__energy)

    def set_money(self, money):
        self.__money = money
        self.moneyChanged.emit(self.__money)

    def set_power(self, power):
        self.__power = power
        self.powerChanged.emit(self.__power)

    def set_image(self, img):
        if img != "":
            self.__image = self.image_path + img
        self.imgChanged.emit(self.__image)

    def show_image(self):
        if self.__countdownVisible:
            return
        self.__imageVisible = True
        self.imgVisibleChanged.emit(self.__imageVisible)

    def hide_image(self):
        self.__imageVisible = False
        self.imgVisibleChanged.emit(self.__imageVisible)

    def set_countdown(self, cnt):
        if self.__imageVisible:
            return
        self.__countdown = cnt
        self.countdownChanged.emit(self.__countdown)

    def show_countdown(self):
        self.__countdownVisible = True
        self.countdownVisibleChanged.emit(self.__countdownVisible)

    def hide_countdown(self):
        self.__countdownVisible = False
        self.countdownVisibleChanged.emit(self.__countdownVisible)

    def set_object_description(self, descr):
        self.__objectDescription = descr
        self.objectDescriptionChanged.emit(self.__objectDescription)

    # Getters

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_energy(self):
        return self.__energy

    def get_money(self):
        return self.__money

    def get_power(self):
        return self.__power

    def get_image(self):
        return self.__image

    def get_imageVisible(self):
        return self.__imageVisible

    def get_countdown(self):
        return self.__countdown

    def get_countdownVisible(self):
        return self.__countdownVisible

    def get_objectDescription(self):
        return self.__objectDescription

    # Properties

    width = Property(int, get_width, notify=widthChanged)
    height = Property(int, get_height, notify=heightChanged)

    energy = Property(int, get_energy, notify=energyChanged)
    money = Property(int, get_money, notify=moneyChanged)
    power = Property(int, get_power, notify=powerChanged)

    image = Property(str, get_image, notify=imgChanged)
    imageVisible = Property(bool, get_imageVisible, notify=imgVisibleChanged)

    countdown = Property(str, get_countdown, notify=countdownChanged)
    countdownVisible = Property(bool, get_countdownVisible, notify=countdownVisibleChanged)

    objectDescription = Property(str, get_objectDescription, notify=objectDescriptionChanged)

    @QtCore.Property(QtCore.QObject, constant=False)
    def model(self):
        return self._model

    # Methods

    def __notify_view(self):
        self.widthChanged.emit(self.__width)
        self.heightChanged.emit(self.__height)
        self.energyChanged.emit(self.__energy)
        self.moneyChanged.emit(self.__money)
        self.powerChanged.emit(self.__power)
        self.imgChanged.emit(self.__image)
        self.imgVisibleChanged.emit(self.__imageVisible)

    def update_stats(self):
        hp, power, _ = self.fetch_stats_callback()
        self.__energy = hp
        self.__power = power
        self.__notify_view()

    def update(self, hp, power, inventory):
        self.__energy = hp
        self.__power = power

        self._model.clear()
        for _, item in inventory.items():
            self._model.add(item.name, item.qta, item.qta_visible())

        self.__notify_view()

    @Slot(str, int)
    def onItemUsed(self, name, index):

        is_consumable = self.update_engine_callback(name)
        if is_consumable:
            self._model.consume(name, index)

        self.update_stats()

    @Slot(str, int)
    def onItemInspect(self, name, index):
        self.show_item_callback(name)
