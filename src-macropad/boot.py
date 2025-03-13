import board
import digitalio
import storage

noStorage = False
noStoragePin = digitalio.DigitalInOut(board.GP6)
noStoragePin.direction = digitalio.Direction.INPUT
noStoragePin.pull = digitalio.Pull.DOWN
noStorage = noStoragePin.value

if(noStorage == True):
    print("USB drive  enabled")
else:
    # normal boot
    storage.disable_usb_drive()
    print("USB drive disable")