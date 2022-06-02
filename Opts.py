import json
import sys, getopt
config = None

def get_help(item='all'):
#change item to title inside list item to get specific details only
#title-command-description
	for obj in help_text:
		if isinstance(obj, str) and item=='all': 
			print(obj) 
		else: 
			[print(obj[i]) for i in range(len(obj)) if item=='all'and i!=0 or item==obj[0]]

def get_config():
	H = None
	P = None
	B = None
	M = None
	O = True
	try:
		with open('settings.json') as json_file:
			data = json.load(json_file)
			H = data['config']['host']
			P = data['config']['port']
			B = data['config']['bufsize']
			M = data['config']['message']
		
	except Exception as e:
		print(f"{e}\nfailed to retreieve settings")
		O = False
	return H, P, B, M, O	
		 
def read(argv):
	HOST, PORT, BUFSIZE, message, OKAY = get_config()
	display_config = False
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
					HOST = vl[0]+'.'+vl[1]+'.'+vl[2]+'.'+vl[3]
							
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
#check to edit bufsize
			elif opt in('-b, ,--bufsize'):
				assert(isinstance(int(arg),int)),'Number is not an integer'
				BUFSIZE=int(arg)
#check for showing information		
			if opt in ('-o', '--options'):
				display_config = True
		if display_config:
			print(f'host:{HOST}:{PORT}\nmessage:{message}\nbufsize:{BUFSIZE}')		
	except getopt.GetoptError:
		if len(argv) != 0:
			print('argument failure')
			OKAY = False
			sys.exit(2)
		else:
			print('arguments blank, attempting to continue')
	return HOST, PORT, BUFSIZE, message, OKAY			

