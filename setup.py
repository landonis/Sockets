HOST = ''#all available interfaces
PORT = 50002
MAX_CONNECTIONS = 2
import socket
listening = True

def main(cd_ip, cd_port, con_num):
	
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #AF_INET Defines IPv4
			sock.bind((cd_ip, cd_port)) 
			
	#binds socket object to host ip and port
			try:
				while True:
					sock.listen(con_num)
					
					new_socket, new_ip = sock.accept() 
	#Returns new Socket for communicating with new connection
					com_sock = newSocket(HOST, PORT, 16, new_socket)
					print(f'recieving new connection from "{new_ip}"')
					print('waiting for a message...')
	#waiting for 16b message Can you hear me?		
					data = com_sock.s_recv(16)
					if not data or data==b'':
	#send the Okay "A"
						print('failed to recieve initial message')
						com_sock.end_socket()
						break
						
					else:
						rply = "Can you hear me?"
						com_sock.s_sendall(rply)
					com_sock.end_socket()		
			except Exception as e:
				print(e)
				print('bad loop')
				sock.close()
				
						
				sock.close()
	except Exception as e:
		print(f'{e}\nmainloop failed')
		
class newSocket:
	def __init__(self, _host, _port, _bufsize, _sock):
		self.sock=_sock
		self.host = _host
		self.port = _port
		self.bufsize = _bufsize
		print(f'new socket {self.host}:{self.port}')
	def s_connect(self):
		try:
			self.sock.connect((self.host, self.port))
			print(f'connected')
			return True
		except Exception as e:
			print(e)
			return False
		
	def s_sendall(self, msg):
		print(f'trying to send msg "{msg}"')
		try:
			self.sock.sendall(msg.encode('utf-8'))
			return True
		except Exception as e:
			print(e)
			return False
	def s_recv(self, msg_len):
		try:
			chunks = []
			bytes_recd = 0
			while bytes_recd < msg_len:
				print(f'bt:{bytes_recd} \ msl: {msg_len}')
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
			print(e)
			self.end_socket()
			return False
	def end_socket(self):
		self.sock.close()
if __name__ == "__main__":

	main(HOST, PORT, MAX_CONNECTIONS)

