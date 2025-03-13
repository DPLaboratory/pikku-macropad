import time
import board
import displayio
import terminalio
import busio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import digitalio
from digitalio import DigitalInOut, Direction


import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Button mapping
#
#  BTN1   BTN2   BTN3
#  BTN4   BTN5   BTN6
#  

BTN1_PIN = board.GP6
BTN2_PIN = board.GP8
BTN3_PIN = board.GP11
BTN4_PIN = board.GP7
BTN5_PIN = board.GP10
BTN6_PIN = board.GP12

currentMode = 0;

MODE_AUDIO = 0
MODE_GIT = 1
MODE_VSCODE = 2
MODE_MACRO = 3
COUNT_OF_MODES = 4

modes = [
    ['Audio',
     'Mute',
     'Stop',
     'Vol Down',
     'Vol UP',
     'Play/Pause' ],
    ['Git',             # Mode name
     'Branch..',        # Key 2 function
     'Checkout main',   # Key 3 function
     'Status',          # Key 4 function
     'Push',            # Key 5 function
     'Pull org main'    # Key 6 function
    ],
    ['VS Code',         # Mode name
     'Explorer',        # Key 2 function
     'Problems',        # Key 3 function
     'Search',          # Key 4 function
     'Debug',           # Key 5 function
     'Output'           # Key 6 function
    ],
    ['Macro',         # Mode name
     'Macro 1 (.)',   # Key 2 function
     'Macro 2',       # Key 3 function
     'Macro 3',       # Key 4 function
     'Macro 4',       # Key 5 function
     'Macro 5'        # Key 6 function
    ],
]

buttons = [
    digitalio.DigitalInOut(BTN1_PIN),
    digitalio.DigitalInOut(BTN2_PIN),
    digitalio.DigitalInOut(BTN3_PIN),
    digitalio.DigitalInOut(BTN4_PIN),
    digitalio.DigitalInOut(BTN5_PIN),
    digitalio.DigitalInOut(BTN6_PIN)
]
for i in range(0,6):
    buttons[i].direction = digitalio.Direction.INPUT
    buttons[i].pull = digitalio.Pull.DOWN


keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
cc = ConsumerControl(usb_hid.devices)

# Rilascia eventuali risorse display attive
displayio.release_displays()

# Inizializza I2C sui pin GP5 (SCL) e GP4 (SDA)
i2c = busio.I2C(board.GP5, board.GP4)
 
# Configura il bus display
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# Inizializza il display SSD1306 (128x64 pixel)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

# Crea un gruppo displayio per il testo
splash = displayio.Group()

# Crea l'elemento di testo
text_area = label.Label(terminalio.FONT, text="PiKKu DPLab 1.0", color=0xFFFFFF, x=20, y=25)
splash.append(text_area)

text_mode = label.Label(terminalio.FONT, text=modes[currentMode][0], color=0xFFFFFF, x=10, y=5)
splash.append(text_mode)

text_op = label.Label(terminalio.FONT, text="(-------------)", color=0xFFFFFF, x=10, y=15)
splash.append(text_op)

# Imposta il gruppo come root del display
display.root_group = splash

def draw_screen_mode(text):
    text_mode.text = text
    
def draw_screen_op(text):
    text_op.text = "(" + text + ")"
    
def handle_mode_press(key):
    global currentMode
    if key == 0:
        currentMode += 1
        if (currentMode > COUNT_OF_MODES-1):
            currentMode = 0
        time.sleep(0.5)
    
        text = modes[currentMode][0]
        draw_screen_mode(text)
        return

    
    text = modes[currentMode][key]
    draw_screen_op(text)


    if(currentMode == MODE_AUDIO):
        if key == 1:
            cc.send(ConsumerControlCode.MUTE)
        if key == 2:
            cc.send(ConsumerControlCode.STOP)    
        if key == 3:
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        if key == 4:
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        if key == 5:
            cc.send(ConsumerControlCode.PLAY_PAUSE)
        
    if(currentMode == MODE_VSCODE):
        if key == 1:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.E)
        if key == 2:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.M)
        if key == 3:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.F)
        if key == 4:
            keyboard.send(Keycode.F5)
        if key == 5:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.U)

    if(currentMode == MODE_GIT):
        if key == 1:
            layout.write('git branch -b ')
        if key == 2:
            layout.write('git checkout main\n')
        if key == 3:
            layout.write('git status\n')
        if key == 4:
            layout.write('git push\n')
        if key == 5:
            layout.write('git pull origin main\n')
            
    if(currentMode == MODE_MACRO):
        if key == 1:
            draw_screen_op("Macro 1 Start")
            while True:
                layout.write(".")
                time.sleep(1)
                if buttons[key].value:
                    draw_screen_op("Macro 1 END")
                    time.sleep(1)
                    break;
                

# Mantiene il programma attivo
while True:
    for btn in range(0, 6):
        if buttons[btn].value:  # Il pulsante è premuto (valore basso)
            print("currentMode pre : ", currentMode, "btn:", btn)
            handle_mode_press(btn)
            print("currentMode dop :", currentMode, "btn:", btn)
           
    time.sleep(0.2)