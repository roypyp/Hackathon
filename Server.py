from socket import *
import time
import thread

print("Server started, listening on IP address 172.1.0.36")

s = socket(AF_INET, SOCK_DGRAM)
#s2 = socket(AF_INET, SOCK_STREAM)
#s2.bind((gethostname(), 2513))
#s2.listen()

msg = b'\xfe\xed\xbe\xef\x02\x25\x13'
#bytes(gethostbyname(gethostname()),"utf-8")
while True:
    #s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    s.sendto(msg, ('<broadcast>', 13117))
    time.sleep(1)

    
    #conn, addr = s2.accept()
    #data = conn.recv(1024)
    #print(data.decode("utf-8"))

# s.bind((socket.gethostname(), 1234))
# s.listen(5)
# while True:
    
#     # now our endpoint knows about the OTHER endpoint.
#     clientsocket, address = s.accept()
#     print(f"Connection from {address} has been established.")
#     clientsocket.send(bytes("Hey there!!! sdfdsf","utf-8"))
#     clientsocket.close()