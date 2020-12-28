from socket import *
import time
import _thread
import select

teamsdict={}
def listenT(s):
    global teamsdict
    startTime=time.time()
    while True:
        readable, writeable, erro = select.select([s],[],[],startTime+10-time.time())
        if len(readable)<=0:
            break
        conn, addr = s.accept()
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


def gameStart(s,inx,a,flag):
    
    while True:
        if(flag[0]):
            break
        print("!")
        s.sendall(bytes("mssage","utf-8"))
        data=s.recv(1024)
        if(data.decode("utf-8")=="press"):
            a[inx]+=1
            print (a)
    s.sendall(bytes("end","utf-8"))


def KSBR():
    global teamsdict
    flagG=0
    group1=[]
    group2=[]
    for key in teamsdict.keys():
        if(flagG==0):
            group1.append([key,teamsdict[key][1]])
            flagG=1
        else:
            group2.append([key,teamsdict[key][1]])
            flagG=0
    mssage="Welcome to Keyboard Spamming Battle Royale.\n"
    mssage+="Group 1:\n==\n"
    for team in group1:
        mssage+=team[1]+"\n"
    for team in group2:
        mssage+=team[1]+"\n"
    mssage+="Start pressing keys on your keyboard as fast as you can!!"
    for key in teamsdict.keys():
        s=teamsdict[key][0]
        s.sendall(bytes(mssage,"utf-8"))
    a=[0]*len(teamsdict)
    inx=0
    flag=[False]
    for key in teamsdict.keys():
        _thread.start_new_thread(gameStart,(teamsdict[key][0],inx,a,flag))
        inx+=1
    time.sleep(10)
    flag[0]=True
    time.sleep(1)



s = socket(AF_INET, SOCK_STREAM)
s.bind(("172.1.0."+gethostbyname(gethostname()).split(".")[3], 9491))
s.listen()

while True:
    _thread.start_new_thread(broadCast,())
    _thread.start_new_thread(listenT,(s,))
    time.sleep(11)
    KSBR()
    time.sleep(11)






# s.bind((socket.gethostname(), 1234))
# s.listen(5)
# while True:
    
#     # now our endpoint knows about the OTHER endpoint.
#     clientsocket, address = s.accept()
#     print(f"Connection from {address} has been established.")
#     clientsocket.send(bytes("Hey there!!! sdfdsf","utf-8"))
#     clientsocket.close()