#!/usr/bin/python
import socket, threading, errno,time, sys,json
sys.path.append('..')
import config


# Handle the different subscriptions corresponding to different ports, a thread is created for each subscription

class subThread (threading.Thread):
   def __init__(self, threadID, name, udp_port,clientID):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.udp_port = udp_port
      self.clientID = clientID
      self._stopevent = threading.Event(  ) # If stop event is set: the thread is stoped !
   def run(self):
      listen_socket(self,self.name, self.udp_port,self.clientID)
      print "Exiting " + self.name


def listen_socket(self,threadName, udp_port,ID):
    UDP_IP = "127.0.0.1"
    UDP_PORT = int(udp_port)
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    sock.setblocking(0)
   
    previous_pkt_nb =0 
    average_latency = 0	 
    init_time=0
    end_time=0  

    while not self._stopevent.isSet(  ): # Quit the program when requested by the user
	try:
	        send_tmstp, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		cur_time = int(round(time.time() * config.timestamp_precision))
		if (previous_pkt_nb ==0 and config.mode=="p"):
				init_time=cur_time
		if (config.mode=="p"):		
        		print "\n%s, received message: %s" % (threadName,send_tmstp)
			send_tmstp = int(send_tmstp)		
			print  cur_time - send_tmstp
			average_latency = (previous_pkt_nb*average_latency + cur_time - send_tmstp)/(previous_pkt_nb+1)
			previous_pkt_nb += 1 
			print previous_pkt_nb
			if previous_pkt_nb==config.eval_packet_nb:
				end_time=int(round(time.time() * config.timestamp_precision))
		if (config.mode=="n"):
			print "\n%s, received message: %s" % (threadName,send_tmstp)

	except socket.error, e:
		if e.args[0] == errno.EWOULDBLOCK:  # Non blocking socket
			continue
		else:
			print e
			break
    if config.mode=="p":
	print end_time, init_time
    	file_name= "data/clients/"+ID	
    	with open(file_name, "a+") as myfile:
		string = str(udp_port)+",latency: "+str(average_latency)+"\n"
    		myfile.write(string)


def publish_message(IP,udp_port,message):
	
	sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
	sock.sendto(message, (IP, udp_port))
