#!/usr/bin/python
import socket, threading, errno,time, sys
sys.path.append('..')
import config


# Handle the different subscriptions corresponding to different ports, a thread is created for each subscription

class subThread (threading.Thread):
   def __init__(self, threadID, name, udp_port):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.udp_port = udp_port
      self._stopevent = threading.Event(  ) # If stop event is set: the thread is stoped !
   def run(self):
      listen_socket(self,self.name, self.udp_port)
      print "Exiting " + self.name


def listen_socket(self,threadName, udp_port):
    UDP_IP = "127.0.0.1"
    UDP_PORT = int(udp_port)
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    sock.setblocking(0)
    while not self._stopevent.isSet(  ): # Quit the program when requested by the user
	try:
	        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        	print "\n%s, received message: %s" % (threadName,data)
		data = int(data)
		print int(round(time.time() * 1000000)) - data
	except socket.error, e:
		if e.args[0] == errno.EWOULDBLOCK:  # Non blocking socket
			continue
		else:
			print e
			break


def publish_message(IP,udp_port,message):
	
	sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
	sock.sendto(message, (IP, udp_port))
