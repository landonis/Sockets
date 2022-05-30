message = 'Can you hear me?'
HOST = '127.0.0.1' 
PORT = 50001

help_text = ['Arguments:', '-s, --send', f'Takes 1 argument for setting message from default message {message}','-o --option', 'Takes no arguments. Shows message connection details.', '-i, --ip', f'Takes 1 argument, set server to connect to. Default set to {HOST}', '-p, --port', f'Takes 1 argument to assign server port to reach. Default set to {PORT}']
import socket
import sys, getopt


sock = None

def get_details():
	return HOST, PORT, message

def getResponse(argv):
	try:
		HOST, PORT, message = get_details()
	except:
		print('couldnt load default details')
		sys.exit()
	try:
		opts, args = getopt.getopt(argv,'sip:ho',['send=','ip=','port=', 'help', 'options'])
		print(opts, args)
		for opt, arg in opts:
#			print ('opt:', opt,', arg: ',arg)
			if opt in ('-h', '--help'):
				for desc in help_text:
					print(desc)
				sys.exit()
			if opt in ('-i', '--i'):
				
				try:
					ip_list = arg.split('.')
					if len(ip_list)==4:
						vl = [x for item in ip_list if (isinstance(int(item), int) and int(item)>=0 and int(item)<=255)]
						HOST = vl[0]+'.'+vl[1]+'.'+vl[2]+'.'+vl[3]
					else:
						print('invalid length/separator')
				except:
					print('could not concate ip')
			elif opt in ('--port', '-p'):
				try: 
					if isinstance(int(arg), int):
						PORT=arg 
				except: print('bad port') 
			
			elif opt in ('--send', '-s'):
				message = arg
		
			elif opt in ('-o', '--options'):
				print(f'Host: {HOST}\nPort: {PORT}\nMessage: {message}')	
	
	except getopt.GetoptError:
		if len(argv) != 0:
			print('argument failure')
			sys.exit(2)
		else:
			print('arguments blank, attempting to continue')
	
	valid = None
	print('Starting connection')
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.connect((HOST,PORT))
			sock.sendall(message.encode())
			data = sock.recv(1024)
		try:
			print(str(data, 'utf-8'))
			print('response: ', str(data, 'utf-8'))
			
		except:
			print('something went wrong getting the response')
	except:
		print('failed to establish connection')
		return False
if __name__ == "__main__":
	getResponse(sys.argv[1:])
		

