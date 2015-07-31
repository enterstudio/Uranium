# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the AGPLv3 or higher.

from PyQt5.QtCore import Qt, pyqtSlot, pyqtProperty, pyqtSignal

from UM.Application import Application
from UM.Qt.ListModel import ListModel
from UM.OutputDevice import OutputDeviceError
from UM.Logger import Logger
from UM.Message import Message
from UM.Scene.Selection import Selection

##  A list model providing a list of all registered OutputDevice instances.
#
#   This list model wraps OutputDeviceManager's list of OutputDevice instances.
#   Additionally it provides a function to set OutputDeviceManager's active device.
#
#   Exposes the following roles:
#   * id - The device ID
#   * name - The human-readable name of the device
#   * short_description - The short description of the device
#   * description - The full description of the device
#   * icon_name - The name of the icon used to identify the device
#   * priority - The device priority
#
class OutputDevicesModel(ListModel):
    IdRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2
    ShortDescriptionRole = Qt.UserRole + 3
    DescriptionRole = Qt.UserRole + 4
    IconNameRole = Qt.UserRole + 5
    PriorityRole = Qt.UserRole + 6

    def __init__(self, parent = None):
        super().__init__(parent)

        self._device_manager = Application.getInstance().getOutputDeviceManager()

        self._active_device = None

        self.addRoleName(self.IdRole, "id")
        self.addRoleName(self.NameRole, "name")
        self.addRoleName(self.ShortDescriptionRole, "short_description")
        self.addRoleName(self.DescriptionRole, "description")
        self.addRoleName(self.IconNameRole, "icon_name")
        self.addRoleName(self.PriorityRole, "priority")

        self._device_manager.outputDevicesChanged.connect(self._update)
        self._device_manager.activeDeviceChanged.connect(self._onActiveDeviceChanged)
        self._update()
        self._onActiveDeviceChanged()

    activeDeviceChanged = pyqtSignal()
    @pyqtProperty("QVariantMap", notify = activeDeviceChanged)
    def activeDevice(self):
        return self._active_device

    @pyqtSlot(str)
    def setActiveDevice(self, device_id):
        self._device_manager.setActiveDevice(device_id)

    @pyqtSlot(str)
    def requestWriteToDevice(self, device_id):
        self._writeToDevice(Application.getInstance().getController().getScene().getRoot(), device_id)

    @pyqtSlot(str)
    def requestWriteSelectionToDevice(self, device_id):
        if not Selection.hasSelection():
            return

        self._writeToDevice(Selection.getSelectedObject(0), device_id)

    def _update(self):
        self.clear()

        devices = self._device_manager.getOutputDevices()
        for device in devices:
            self.appendItem({
                "id": device.getId(),
                "name": device.getName(),
                "short_description": device.getShortDescription(),
                "description": device.getDescription(),
                "icon_name": device.getIconName(),
                "priority": device.getPriority()
            })

        self.sort(lambda i: -i["priority"])

    def _onActiveDeviceChanged(self):
        device = self._device_manager.getActiveDevice()
        self._active_device = self.getItem(self.find("id", device.getId()))
        self.activeDeviceChanged.emit()

    def _writeToDevice(self, node, device_id):
        device = self._device_manager.getOutputDevice(device_id)
        if not device:
            return

        try:
            device.requestWrite(node)
        except OutputDeviceError.UserCanceledError:
            pass
        except OutputDeviceError.WriteRequestFailedError as e:
            message = Message(str(e))
            message.show()