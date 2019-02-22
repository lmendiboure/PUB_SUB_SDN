#!/usr/bin/python
import socket, threading, errno, signal,sys,json
from utils import client_utils
from data import services

# Main program


# Handle ctrl+C to stop application
def sigint_handler(signum, frame):
    client_utils.exitClient() # kill threads
    sys.exit() # exit from while loop
 
signal.signal(signal.SIGINT, sigint_handler)

def main():
	# Variables
	sub_topics=[] # List of subcriptions of the client
	IP_addr="" # Client IP Address
	ID="" # Client ID (correponds to the first argument of the client program and the hostname

	# Get client infos	
	(IP_addr,ID) = client_utils.get_client_infos()	

	# First, we add the default services 
	client_utils.add_services_list(services.default_services,ID)
	for defaut_sub in services.default_services:
		sub_topics.append(defaut_sub)


	# Then, we launch the client interface
	while True:
		choice =client_utils.print_menu()
		if choice == "1":
			service_name = client_utils.sub_menu(services.services_list, sub_topics,ID)
			if service_name:
				sub_topics.append(service_name)

		if choice == "2":
			 service_name = client_utils.unsubscribe_service_display(sub_topics)
			 if service_name:
				sub_topics.remove(service_name)
		if choice == "3":			
			client_utils.pub_process(services.services_list)
		if choice == "4":			
			client_utils.subscribed_services_display(sub_topics)
		if choice == "5":			
			client_utils.display_client_infos(IP_addr,ID)
		if choice == "6":
			client_utils.exitClient()
			break
   
if __name__== "__main__":
	main()

	
	
