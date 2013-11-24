from tornado import websocket, web, ioloop
import json
import threading
import serial

clList = []

# Read From SerialPort
def read_from_port(ser):
	while True:
		data = ser.readline().rstrip()
		if data != '':
			data = {"message": data}
			jsondata = json.dumps(data)

			for cl in clList:
				cl.write_message(jsondata)

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

class SerialHandler(web.RequestHandler):
	@web.asynchronous
	def get(self, *args):
		self.finish()
		data = {"message": "test"}
		data = json.dumps(data)
		for cl in clList:
			cl.write_message(data)

	@web.asynchronous
	def post(self):
		pass

app = web.Application([
		(r'/', RootHandler),
		(r'/ws', WebSocketHandler),
		(r'/serial', SerialHandler)
])

if __name__ == '__main__':
	# Serial
	ser = serial.Serial(4, timeout=0) # read from COM5
	thread = threading.Thread(target=read_from_port, args=(ser,))
	thread.setDaemon(True)
	thread.start()
	
	app.listen(8080)
	ioloop.IOLoop.instance().start()
