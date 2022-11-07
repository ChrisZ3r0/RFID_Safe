from time import sleep

# SOURCE: https://www.youtube.com/watch?v=EpvVYyKwfjs

KEY_UP = 0
KEY_DOWN = 1

# ACTUALIZE
keys = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]

# ACTUALIZE PIN Names !!!
rows = [2, 3, 4, 5]
cols = [6, 7, 8, 9]

# Set pins for rows as outputs
row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in rows]

# Set pins for cols as inputs
col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_name in cols]


def initRowOfPins():
	for row in range(4):
		for col in range(4):
			row_pins[row].low()


def scanKeyPad(inputRow : int, InputCol : int) -> int:
	row_pins[inputRow].high()
	key_state = KEY_UP

	if col_pins[InputCol].value() == KEY_DOWN:
		key_state = KEY_DOWN
	row_pins[inputRow].low()

	return key_state


initRowOfPins()
while True:
	# To prevent multiple unintentional presses later
	# time.sleep(1)
	for row in range(4):
		for col in range(4):
			key = scanKeyPad(row, col)
			if key == KEY_DOWN:
				print(f"Key pressed: {keys[row][col]}")
				last_pressed_key = keys[row][col]
