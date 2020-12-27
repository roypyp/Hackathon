from socket import *
import time
import _thread
import select

teamsdict={}
def listenT(s):
    global teamsdict
    print(startTime)
    while True:
        readable, writeable, erro = select.select([s],[],[],startTime+10-time.time())
        if len(readable)<=0:
            break
        conn, addr = s.accept()
        print("hey")
        data = conn.recv(1024)
        teamsdict[addr]=[conn,data.decode("utf-8")]
        print(data.decode("utf-8"))
        #_thread.start_new_thread(listenT,())
def broadCast():
    print("Server started, listening on IP address ", "172.1.0."+gethostbyname(gethostname()).split(".")[3])
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    msg = b'\xfe\xed\xbe\xef\x02\x25\x13'
    
    for i in range(10):
    #s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.sendto(msg, ('<broadcast>', 13217))
        time.sleep(1)

def KSBR():
    global teamsdict


s = socket(AF_INET, SOCK_STREAM)
s.bind(("172.1.0."+gethostbyname(gethostname()).split(".")[3], 9491))
s.listen()

while True:
    _thread.start_new_thread(broadCast,())
    _thread.start_new_thread(listenT,(s,))
    time.sleep(11)






# s.bind((socket.gethostname(), 1234))
# s.listen(5)
# while True:
    
#     # now our endpoint knows about the OTHER endpoint.
#     clientsocket, address = s.accept()
#     print(f"Connection from {address} has been established.")
#     clientsocket.send(bytes("Hey there!!! sdfdsf","utf-8"))
#     clientsocket.close()