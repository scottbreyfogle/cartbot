from evdev import uinput, ecodes

def predict(network, stop, key_threshold=.5):
    ui = uinput.UInput()    
    keys_down = set([])
    
    while not stop.set():
        vals = network.predict() 
        for (index, val) in enumerate(vals):
            type, code = network.event_codes[index]
            if type == ecodes.EV_KEY:
                if val > key_threshold:
                    ui.write(ecodes.EV_KEY, code, 1)
                else:
                    ui.write(ecodes.EV_KEY, code, 0)
            else:
                ui.write(type, code, val)

            ui.syn()
