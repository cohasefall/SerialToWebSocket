from tornado import websocket, web, ioloop
import json
import threading
import serial
from time import sleep

clList = []

# Read From SerialPort
def read_from_port(ser):
	while True:
		data = ser.readline().rstrip()
		if data != '':
			data = {"data": data}
			jsondata = json.dumps(data)

			for cl in clList:
				cl.write_message(jsondata)
		sleep(0.5)

# Tornado 
class RootHandler(web.RequestHandler):
	def get(self):
		self.render("index.html")

class WebSocketHandler(websocket.WebSocketHandler):
	def open(self):
		if self not in clList:
			clList.append(self)
	
	def on_close(self):
		if self in clList:
			clList.remove(self)

app = web.Application([
		(r'/', RootHandler),
		(r'/ws', WebSocketHandler)
])

if __name__ == '__main__':
	# Serial
	ser = serial.Serial(4) # read from COM5
	thread = threading.Thread(target=read_from_port, args=(ser,))
	thread.setDaemon(True)
	thread.start()
	
	app.listen(8080)
	ioloop.IOLoop.instance().start()

