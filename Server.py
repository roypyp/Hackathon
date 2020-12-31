from socket import *
import time
import _thread
import select

teamsdict={}
#litsen for TSP massage
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
      

#send broadcast offer
def broadCast():
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    portBC=13117
    #The broadcast message
    msg = b'\xfe\xed\xbe\xef\x02\x25\x13'
    
    for i in range(10):
        s.sendto(msg, ('<broadcast>', portBC))
        time.sleep(1)


#game start to listen to clint key smashing
def gameStart(s,inx,a,flag):
    while True:
        if(flag[0]):
            break
        data=s.recv(1024)
        a[inx]+=1
   

#split to group send the massage and start thread for each client 
def KSBR():
    global teamsdict
    flagG=0
    group1=[]
    group2=[]

    #divide the clients to 2 groups, odd group and even group
    for key in teamsdict.keys():
        if(flagG==0):
            group1.append([key,teamsdict[key][1]])
            flagG=1
        else:
            group2.append([key,teamsdict[key][1]])
            flagG=0


##building the message - what we will print
    mssage="Welcome to Keyboard Spamming Battle Royale.\n"
    mssage+="Group 1:\n==\n"
    for team in group1:
        mssage+=team[1]+"\n"
    mssage+="Group 2:\n==\n"
    for team in group2:
        mssage+=team[1]+"\n"
    mssage+="Start pressing keys on your keyboard as fast as you can!!"

    #sending the message to everyone
    for key in teamsdict.keys():
        s=teamsdict[key][0]
        s.sendall(bytes(mssage,"utf-8"))

    #counter of the number of pressing 
    a=[0]*len(teamsdict)

    inx=0
    flag=[False]
    for key in teamsdict.keys():
        _thread.start_new_thread(gameStart,(teamsdict[key][0],inx,a,flag))
        inx+=1

    time.sleep(10)
    flag[0]=True
    time.sleep(0.2)
    group1point=0
    group2point=0
    flagG=0

    for i in range(len(a)):
        if(flagG==0):
            group1point+=a[i]
            flagG=1
        else:
            group2point+=a[i]
            flagG=0

    fmssage="Group 1 typed in "+ str(group1point)+" characters. Group 2 typed in " + str(group2point) +" characters.\n"
    if group1point>=group2point:
        fmssage+="Group 1 wins!\n\n"

        fmssage+="Congratulations to the winners:\n==\n"
        for team in group1:
            fmssage+=team[1]+"\n"
    else:
        fmssage+="Group 2 wins!\n\n"

        fmssage+="Congratulations to the winners:\n==\n"
        for team in group2:
            fmssage+=team[1]+"\n"

    #send the message to everyone(clients)
    for key in teamsdict.keys():
        s=teamsdict[key][0]
        s.sendall(bytes(fmssage,"utf-8"))

    #Cant closing the socket until revicing from client
    for key in teamsdict.keys():
        s=teamsdict[key][0]
        s.recv(1024)
        s.close()




s = socket(AF_INET, SOCK_STREAM)
s.bind(("172.1.0."+gethostbyname(gethostname()).split(".")[3], 9491))
s.listen()
print("Server started, listening on IP address ", "172.1.0."+gethostbyname(gethostname()).split(".")[3])
while True:
    try:
        _thread.start_new_thread(broadCast,())
        _thread.start_new_thread(listenT,(s,))
        time.sleep(11)
        KSBR()
        print("Server disconnected, listening for offer requests...")
        time.sleep(1)
        teamsdict={}
    except:
        print("code fall")


