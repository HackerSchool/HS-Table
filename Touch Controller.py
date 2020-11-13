import pyautogui
import serial

def moveMouse(coordinates):
    """ Moves the mouse to the coordinates """

    pyautogui.moveTo(coords)

if __name__ == "__main__":
	ser = serial.Serial('COM3', 9600)

	pyautogui.FAILSAFE = False

	coords = [500,500]
	
	while True :
		# get serial
		if ser.inWaiting():
			coords[0] = int.from_bytes(ser.read(2), "little")
			coords[1] = int.from_bytes(ser.read(2), "little")
			
			print(coords)
			
			moveMouse(coords)