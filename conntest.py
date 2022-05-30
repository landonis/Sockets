MESSAGE = 'Can you hear me?'
HOST = '127.0.0.1' 
PORT = 50001
BUFSIZE=2048

help_text = ['Arguments:',[ 'Message','-s, --send', f'Takes 1 argument for setting message from default message {MESSAGE}'],['Display','-o --option', 'Takes no arguments. Shows message connection details.'],['Address','-i, --ip', f'Takes 1 argument, set server to connect to. Default set to {HOST}'],['Port','-p, --port', f'Takes 1 argument to assign server port to reach. Default set to {PORT}'],['Bufsize','-b, --bufsize', f'Takes 1 argument to assign the maximum amount of data to be recieved at one time. Default is set to {BUFSIZE}.']]
import socket
import sys, getopt


sock = None

def get_help(item='all'):
#change item to title inside list item to get specific details only
#title-command-description
	for obj in help_text:
		if isinstance(obj, str) and item=='all': 
			print(obj) 
		else: 
			[print(obj[i]) for i in range(len(obj)) if item=='all'and i!=0 or item==obj[0]]
			
class newSocket:
	def __init__(self, _host, _port, _bufsize, _sock=None):
		self.sock=_sock
		self.host = _host
		self.port = _port
		self.bufsize = _bufsize
		if self.sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock
	def s_connect(self):
		try:
			self.sock.connect((self.host, self.port))
			print(f'Message sent')
			return True
		except Exception as e:
			print(e)
			return False
		
	def s_sendall(self, msg, bounce=False):
		try:
			self.sock.sendall(msg.encode())
			return True
		except Exception as e:
			print(e)
			return False
	def s_recv(self, msg_len):
		try:
			chunks = []
			bytes_recd = 0
			while bytes_recd < msg_len:
				chunk = self.sock.recv(min(msg_len-bytes_recd, self.bufsize))
				if chunk == b'':
					raise RuntimeError("socket connection broken")
				chunks.append(chunk)
				bytes_recd = bytes_recd+len(chunk)
			return b''.join(chunks)
		except Exception as e:
			print(e)
			self.end_socket()
			return False
	def end_socket(self):
		self.sock.close()
def main(argv, HOST, PORT, BUFSIZE):
	try:
#docs.python.org/3/library/getopt.html
		opts, args = getopt.getopt(argv,'i:s:p:b:ho',['ip=','send=','port=', 'bufsize=', 'help', 'options'])
		
		for opt, arg in opts:
			if opt in ('-h', '--help'):
				get_help()
				sys.exit()
#check for valid ip
			elif opt in ('-i', '--ip'):
				print(f'checking for valid ip from input "{arg}"')
				try:
					ip_list = arg.split('.')
					assert(len(ip_list)==4),'invalid length/separator'
					vl = [item for item in ip_list if (isinstance(int(item), int) and int(item)>=0 and int(item)<=255)]
					assert(len(vl)==4), "invalid IP"
					HOST = vl[0]+'.'+vl[1]pyt+'.'+vl[2]+'.'+vl[3]
							
				except Exception as e:
					print(e)
					print(f'supplied IP "',arg,'" is invalid. Example:\n-i 1.1.1.1')
					print('Terminating...')
					sys.exit()
#Check if port is supplied
			elif opt in ('--port', '-p'):
				try: 
					assert(isinstance(int(arg), int)),'Number is not an integer'
					PORT=int(arg) 
				except Exception as e: print(e,'bad port "{arg}" supplied') 
#check if message is supplied			
			elif opt in ('--send', '-s'):
				message = arg
#check for showing information		
			elif opt in ('-o', '--options'):
				print(f'Host: {HOST}\nPort: {PORT}\nMessage: {message}')	
#check to edit bufsize
			elif opt in('-b, ,--bufsize'):
				assert(isinstance(int(arg),int)),'Number is not an integer'
				BUFSIZE=int(arg)
	except getopt.GetoptError:
		if len(argv) != 0:
			print('argument failure')
			sys.exit(2)
		else:
			print('arguments blank, attempting to continue')			
	print('Starting connection')
	new_sock = newSocket(HOST, PORT, BUFSIZE)
	con = new_sock.s_connect()
	snd = new_sock.s_sendall(MESSAGE)
	rpl = new_sock.s_recv(16)
	print(f'connection {con}, send {snd}, reply {rpl}')
if __name__ == "__main__":
	main(sys.argv[1:], HOST, PORT, BUFSIZE)
		

