import socket
import getch
import time


print("Client started, listening for offer requests....")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s2= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('',13217))

teamname="Isengard"
cha=b'\xfe\xed\xbe\xef\x02'
while True:
    try:
        s2= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        message, address = s.recvfrom(10104)
        print( "Received offer from ",address[0] ,",attempting to connect...")
        if(message[0:5]!=cha[0:5]):
            print("wrong broadcast")
        port_num=int(hex(message[5])[2:]+hex(message[6])[2:],16)
        print(port_num)
        s2.connect(("172.1.0."+address[0].split(".")[3], port_num))
        s2.sendall(bytes(teamname,"utf-8"))
        data=s2.recv(10104)
        print(data.decode("utf-8"))
        while True:
            data=s2.recv(1024)
            if(data.decode("utf-8")=="mssage"):
                a=getch.getch()
                s2.sendall(bytes("press","utf-8"))
            elif(data.decode("utf-8")=="end"):
                break
        print("Game over!")
        data=s2.recv(10104)
        print(data.decode("utf-8"))  
        print("Game over, sending out offer requests...")
        s2.close()
        time.sleep(2)
        s2=None
    except (KeyboardInterrupt,SystemExit):
        raise

    


# s.connect((socket.gethostname(), 1234))
# full_msg = ''
# while True:
#     msg = s.recv(8)
#     if len(msg) <= 0:
#         break
#     full_msg += msg.decode("utf-8")

# print(full_msg)