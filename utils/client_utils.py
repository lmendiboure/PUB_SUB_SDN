#!/usr/bin/python
import socket, threading, errno
import subscriber

# Visible part of the application, display the different menus and the content corresponding to the requests

threadID = 1
threads=[]

# display main menu
def print_menu():
	print "\nWhat do you want to do?"
	print "	- To Subscribe to a new service: press 1"
	print "	- To unsubscribe to a service: press 2"
	print "	- To publish: press 3"
	print "	- To display your current subscriptions: press 4"	
	print "	- To exit: press 5"
	return raw_input(">")


# enable a client to subscibe to a topic : menu + sub process
def sub_menu(service_list, already_sub):
	print "Select a service in this list:"
	max_sub_number = available_services_display(service_list,already_sub)  # display list of existing services and get index of the last service 
	sub_number = raw_input(">")
	print
	if sub_number and int(sub_number) <= int(max_sub_number):  # If in list of service, we retrieve data about this service and create a thread for this service
		name=(service_list.keys())[int(sub_number)]
		port=service_list[name]["port"]
		add_sub(name,port)
		print "You just subscribed to: " + name
		return name
	else:
		print "Wrong service number !"
		return None


# Add a new thread corresponding to a socket (ie subscription to a service)
def add_sub(name,port):
	global threadID, threads
	thread1 = subscriber.subThread(threadID, name, port)	
	thread1.start()
	threads.append(thread1)
	threadID += 1

# add all the elements of a list of services: create multiple threads at the same time
def add_services_list(services_list):
	print "By default, you subscribed to these services:"
	for key in services_list:
		add_sub(key,services_list[key]["port"])
		print key

# Manage the process on unsubscription
def unsubscribe_service_display(service_list):
	print "Which service would you like to leave ?"
	max_unsub_number = available_services_display(service_list,[])	
	unsub_number = raw_input(">")
	if unsub_number and int(unsub_number) <= int(max_unsub_number):
		for t in threads:
			if t.name == service_list[int(unsub_number)]:
				t._stopevent.set()
				t.join()
				return service_list[int(unsub_number)]  # return the table element corresponding to the unsubscription
	print "Wrong service number !"
	return None

# Display the list of services the client does not subscribed yet
def available_services_display(service_list,already_sub):
	ind = -1
	for key in service_list:
		ind+=1
		if key not in already_sub:
			print str(ind) + " : " + key
	return ind	


# Display list of subscriptions
def subscribed_services_display(services_list):
	print "Your current subscriptions are:"
	available_services_display(services_list,[])

# Quit the program when asked by the client
def exitClient():
	global threads, subscriber
	print "Goodbye !"
	for t in threads:
		print t.name
		t._stopevent.set()
		t.join()
	print "Exiting Main Thread"



