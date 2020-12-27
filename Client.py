import socket

print("Client started, listening for offer requests....")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('',13117))

teamname="isengard"
cha=b'\xfe\xed\xbe\xef\x02'

try:
    message, address = s.recvfrom(10104)
    print( "Received offer from ",address[0] ,",attempting to connect...")
    if(message[0:5]!=cha[0:5]):
        print("wrong broadcast")
    port_num=int(hex(message[5])[2:]+hex(message[6])[2:])
    print(port_num)
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