#!/usr/bin/env python
import socket

server1_ip = '127.0.0.1'
server1_port = 20001 #81 september
server2_ip = '127.0.0.1'
server2_port = 8110 #next port

live_ip = server1_ip
live_port = server1_port

server_cmd_terminator = ':[service_msg_end]'

def command(command_name, data, ip=None, port=None):   
    #if ip is None, user failOver()
        #This system does not balance load, as of now [since we have only 1 physical server]
        #Randomly select an instance later for load balancing
    request = command_name + ':' + data + server_cmd_terminator
    
    if (not ip):
        #try server 1
        try:
            data = sendData(request, live_ip, live_port)
            if data == 'sys:offline' or data == 'error:connect_error':
                #server down, try failover
                failOver() #resets the primary server
                data = sendData(request, live_ip, live_port)
            
            if data:    #data:**** or error:**** either case it has to be relayed back
                return data
            return 'error:unknown_error'
            #everything OK, format and send response            
        except:
            return 'error:unknown_error'
    
    #no load balancing 
    else:
        try:
            data = sendData(request, ip, port)
            if data:
                return data
            return 'error:unknown_error'
        except:
            return 'error:unknown_error'

def sendData(data_to_send, ip, port):
    data_to_send = "*password#:" + data_to_send
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.send(data_to_send)
        data = ''
        while True:
            bytes = sock.recv(1024) # get up to 1K at a time
            data += bytes
            if not bytes: break # till closed on server side        
        return data
    except:
        return "error:connect_error"

def failOver():
    global live_ip, live_port
    if live_ip == server1_ip and live_port == server1_port:
        live_ip = server2_ip
        live_port = server2_port
    elif live_ip == server2_ip and live_port == server2_port:
        live_ip = server1_ip
        live_port = server1_port

#most (or all) calls from bigfoot hit this method
def getQueryResults(command_name, query_data):
    result = command(command_name, query_data)
    if result.startswith('data:'):
        return result[5:]
    else:
        return None
