import socket
import getch
import time
import sys
import select
import tty
import termios
import multiprocessing


def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def test(s2):
    try:
        while 1:
            a=getch.getch()
            s2.sendall(bytes("press","utf-8"))   
    except(KeyboardInterrupt,SystemExit):
        print("InvlidTyping")

print("Client started, listening for offer requests....")

#open a socket for broadcast message
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s2= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('',13117))

teamname="Isengard"
cha=b'\xfe\xed\xbe\xef\x02'
while True:
    try:
        s2= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        message, address = s.recvfrom(10104)
        print( "Received offer from ","172.1.0."+address[0].split(".")[3] ,",attempting to connect...")

        #validation of broadcast message 
        if(message[0:4]!=cha[0:4]):
            print("wrong broadcast")
            continue

        #convert the porn number from hex to decimal
        port_num=int(hex(message[5])[2:]+hex(message[6])[2:],16)
        #print(port_num)
        s2.connect(("172.1.0."+address[0].split(".")[3], port_num))
        s2.sendall(bytes(teamname,"utf-8"))
        data=s2.recv(10104)
        print(data.decode("utf-8"))
       
        '''starttime=time.time()
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            while 1:
                if time.time()-starttime>= 10:      
                    break
                if isData():
                    c = sys.stdin.read(1)
                    s2.sendall(bytes("press","utf-8"))
                
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)'''

        p = multiprocessing.Process(target=test, name="test", args=(s2,))
        p.start()
        time.sleep(10.2)
        p.terminate()
        p.join()
        
        #test(s2)
        print("Game over!")
        data=s2.recv(10104)
        print(data.decode("utf-8"))  
        print("Game over, sending out offer requests...")
        s2.close()
        time.sleep(0.2)
        s2=None
    except (KeyboardInterrupt,SystemExit):
        raise

    

