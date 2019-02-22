import socket,sys, time
sys.path.append('..')
import config

# Generate and send X packets (first arg) to IP Y (second arg), Port Z (third arg)

if len(sys.argv) <4:

	print "Generate and send X packets (first arg) to IP Y (second arg), Port Z (third arg) with timestamp"

else :
	for i in range(int(sys.argv[1])):
		sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
		sock.sendto(str(int(round(time.time() * config.timestamp_precision))), (sys.argv[2], int(sys.argv[3])) )
