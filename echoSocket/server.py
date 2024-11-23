import socket  
# Standard loopback interface address (localhost)  
host_name = '0.0.0.0'    
# Specified Port to listen on (non-privileged ports are > 1023)  
port_name = 65432          
# TCP Sockets  
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
    s.bind((host_name, port_name))  
    s.listen()  
    conn, addr = s.accept()  
    with conn:  
        print('Connected by', addr)  
        while True:  
            data = conn.recv(1024)
            print(data)  
            if not data:  
                break	 
            conn.sendall(data)  
