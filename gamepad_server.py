import socket
import libevdev


device = libevdev.Device( )
device.name = 'Discord plays'


addr = ( '', 1334 )
s = socket.create_server( addr )
s.listen( )

buttons = [
    libevdev.EV_SYN.SYN_REPORT,
    libevdev.EV_KEY.BTN_DPAD_UP,
    libevdev.EV_KEY.BTN_DPAD_DOWN,
    libevdev.EV_KEY.BTN_DPAD_LEFT,
    libevdev.EV_KEY.BTN_DPAD_RIGHT,
    libevdev.EV_KEY.BTN_SOUTH,
    libevdev.EV_KEY.BTN_EAST,
    libevdev.EV_KEY.BTN_NORTH,
    libevdev.EV_KEY.BTN_WEST,
    libevdev.EV_KEY.BTN_TL,
    libevdev.EV_KEY.BTN_TR,
    libevdev.EV_KEY.BTN_SELECT,
    libevdev.EV_KEY.BTN_START,
    ]

report = libevdev.InputEvent( buttons[0], value = 0 )

for x in range( 1, len(buttons) ):
    device.enable( buttons[x] )

uinput = device.create_uinput_device()

while True:
    c, addr = s.accept( )
    data = c.recv( 2 )
    print(data)

    if data[0] == 0: break
    press = [ libevdev.InputEvent( buttons[data[0]], value = 1 ), report ]
    uinput.send_events( press )
    press = [ libevdev.InputEvent( buttons[data[0]], value = 0 ), report ]
    uinput.send_events( press )

    c.close( )
