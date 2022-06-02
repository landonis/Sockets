MAX_CONNECTIONS = 2
listening = True

import socket
import sys
from Opts import read

def main(cd_ip, cd_port, BUFSIZE):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #AF_INET Defines IPv4
			sock.bind((cd_ip, cd_port)) 	
#binds socket object to host ip and port
			try:
				while True:
					sock.listen(MAX_CONNECTIONS)
					
					new_socket, new_ip = sock.accept() 
#Returns new Socket for communicating with new connection
					com_sock = newSocket(cd_ip, cd_port, BUFSIZE, new_socket)
					print(f'recieving new connection from "{new_ip}"')
					print('waiting for a message...')
#waiting for 16b message Can you hear me?		
					data = com_sock.s_recv(BUFSIZE)
					if not data or data==b'':
#send response
						print('failed to recieve initial message')
						com_sock.end_socket()
						break
						
					else:
						print(data)
						rply = f'you said "{data}"?'
						com_sock.s_sendall(rply)
					com_sock.end_socket()		
			except Exception as e:
				print(e)
				print('bad loop')
				sock.close()

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

if __name__ == "__main__":
	HOST, PORT, BUFSIZE, MESSAGE, OKAY = read(sys.argv[1:])
	if OKAY:
		main(HOST, int(PORT), int(BUFSIZE))

