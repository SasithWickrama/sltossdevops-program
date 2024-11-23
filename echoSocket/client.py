import socket  
# This represent the server's hostname or IP address  
HOST = '172.25.2.133'    
# This is port number used by the server  
PORT = 65432          
  
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
    s.connect((HOST, PORT))
    name = input("Enter your name: ")
    message = input("Message: ")
    s.send("{}: {}".format(name, message).encode('utf-8'))	  
    s.sendall(b'Hello, world')  
    data = s.recv(1024)  
  
print('Received', repr(data))  
