from evdev import InputDevice, categorize, ecodes
from re import search

dev = InputDevice('/dev/input/event4')

events = {} #A set that will contain all keys currently being held down

for event in dev.read_loop():
	if event.type == ecodes.EV_KEY:
		(key,state) = search(".+\(KEY_(\w+)\), (up|down)",str(event)).groups()
		if state == 'down':
			if key not in events:
				events.add(key) #Adds a pressed key to events
		else:
			if key in events:
				events.remove(key) #Removes a released key from events

