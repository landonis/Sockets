import socket
import sys
from Opts import read

sock = None
		
class newSocket:
	def __init__(self, _host, _port, _bufsize, _sock=None):
		self.sock = _sock
		self.host = _host
		self.port = int(_port)
		self.bufsize = int(_bufsize)
		if self.sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def s_connect(self):
		try:
			self.sock.connect((self.host, self.port))
			
			return True
		except Exception as e:
			print(f'{e}\n error in s_connect')
			return False
		
	def s_sendall(self, msg, bounce=False):
		try:
			self.sock.sendall(msg.encode())
			print(f'Message sent')
			return True
		except Exception as e:
			print(e)
			return False
	def s_recv(self, msg_len):
		msg_len = int(msg_len)
		try:
			chunks = []
			bytes_recd = 0
			while bytes_recd < msg_len:
				chunk = self.sock.recv(min(msg_len-bytes_recd, msg_len))
				if chunk == b'':
					raise RuntimeError("socket connection broken")
				chunks.append(chunk)
				bytes_recd = bytes_recd+len(chunk)
			final = ''
			for ch in chunks:
				final = final + ch.decode('utf-8')
			print(final)
			return final
		except Exception as e:
			print(f'{e}\nerror in s_recv')
			self.end_socket()
			return False
	def end_socket(self):
		self.sock.close()
def main(HOST, PORT, MESSAGE, BUFSIZE):
	
	print('Starting connection')
	new_sock = newSocket(HOST, PORT, BUFSIZE)
	con = new_sock.s_connect()
	snd = new_sock.s_sendall(MESSAGE)
	rpl = new_sock.s_recv(BUFSIZE)
	print(f'connection {con}, send {snd}, reply {rpl}')
if __name__ == "__main__":
	HOST, PORT, BUFSIZE, MESSAGE, OKAY = read(sys.argv[1:])
	if OKAY:
		main(HOST, PORT, MESSAGE, BUFSIZE)
		

