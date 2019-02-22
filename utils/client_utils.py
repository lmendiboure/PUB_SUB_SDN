#!/usr/bin/python
import socket, threading, errno, sys,random
import subscriber

# Visible part of the application, display the different menus and the content corresponding to the requests

threadID = 1
threads=[]

# get host infos
def get_client_infos():
	hostname = socket.gethostname()    
	IPAddr = socket.gethostbyname(hostname)
	ID=""  
	if (len(sys.argv)>=2):
			ID=sys.argv[1]  
	ID+="_"+hostname
	return (IPAddr, ID)	

def display_client_infos(IP_addr,ID):
	print "Your IP address: " +IP_addr
	print "Your ID: " +ID
	
# display main menu
def print_menu():
	print "\nWhat do you want to do?"
	print "	- To Subscribe to a new service: press 1"
	print "	- To unsubscribe to a service: press 2"
	print "	- To publish: press 3"
	print "	- To display your current subscriptions: press 4"
	print "	- To display your client information: press 5"	
	print "	- To exit: press 6"
	return raw_input(">")


# enable a client to subscibe to a topic : menu + sub process
def sub_menu(service_list, already_sub,ID):
	print "Select a service in this list:"
	available_services_display(service_list,already_sub)  # display list of existing services and get index of the last service 
	sub_number = raw_input(">")
	print
	if sub_number and int(sub_number) <= len(service_list):  # If in list of service, we retrieve data about this service and create a thread for this service
		name=(service_list.keys())[int(sub_number)]
		port=service_list[name]["port"]
		add_sub(name,port,ID)
		print "You just subscribed to: " + name
		return name
	else:
		print "Wrong service number !"
		return None


# Add a new thread corresponding to a socket (ie subscription to a service)
def add_sub(name,port,ID):
	global threadID, threads
	thread1 = subscriber.subThread(threadID, name,port, ID)	
	thread1.start()
	threads.append(thread1)
	threadID += 1

# add all the elements of a list of services: create multiple threads at the same time
def add_services_list(services_list,ID):
	print "By default, you subscribed to these services:"
	for key in services_list:
		add_sub(key,services_list[key]["port"],ID)
		print key

# Manage the process on unsubscription
def unsubscribe_service_display(service_list):
	print "Which service would you like to leave ?"
	available_services_display(service_list,[])	
	unsub_number = raw_input(">")
	if unsub_number and int(unsub_number) < len(service_list):
		for t in threads:
			if t.name == service_list[int(unsub_number)]:
				t._stopevent.set()
				t.join()
				return service_list[int(unsub_number)]  # return the table element corresponding to the unsubscription
	print "Wrong service number !"
	return None

# New publication
def pub_process(service_list):
	print "In which service would you like to publish ?"
	available_services_display(service_list,[])	
	pub_number = raw_input(">")
	display_sec_menu()
	action = raw_input(">")	
	if int(action)==1:
		print "Write the content of this message ?"	
		content = raw_input(">")
		subscriber.publish_message(service_list[service_list.keys()[int(pub_number)]]["IP"],service_list[service_list.keys()[int(pub_number)]]["port"],content)
	if int(action)==2:
		print "Write the number of messages to send:"
		number = raw_input(">")
		for i in range(int(number)):
			string_content = "x" * random.randint(1,1024)
			subscriber.publish_message("127.0.0.1",5005,string_content)

# Display secondary publish process menu : action
def display_sec_menu():
	print "\nWhat do you want to do?"
	print "	- Publish a specific message: press 1"
	print "	- Publish X random messages: press 2"
	
	

# Display the list of services the client does not subscribed yet
def available_services_display(service_list,already_sub):
	ind = -1
	for key in service_list:
		ind+=1
		if key not in already_sub:
			print str(ind) + " : " + key


# Display list of subscriptions
def subscribed_services_display(services_list):
	print "Your current subscriptions are:"
	available_services_display(services_list,[])

# Quit the program when asked by the client
def exitClient():
	global threads, subscriber
	print "Goodbye !"
	for t in threads:
		t._stopevent.set()
		t.join()
	print "Exiting Main Thread"



