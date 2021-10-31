### 20181116 / 작성자 : 이한결 ###
### 서버와 접속하고, 메세지를 주고 받는다. ###

import socket
from threading import Thread

_default_message = "hello"
_default_host = 'LocalHost'
_default_port = '4040'

# 해당 요람의 고유 시리얼 "DEVICE;고유번호" 의 형식
_device_serial = "DEVICE;01"

### 서버에 소켓통신 연결하고 메세지를 전송하는 메소드를 가지고 있는 class ###
class ConnectServer():
    ### 생성자 : default host와 default port로 연결 ###
    ### 기본 전송할 문구(msg)는 _default_message ###
    def __init__(self):
        self.host = 'LocalHost'
        self.port = 4040
        self.msg = _default_message

    ### host를 셋팅한다. ###
    def setHost(self, host):
        self.host = host
    
    ### port를 셋팅한다. ###
    def setPort(self, port):
        self.port = port
        
    ### 전송할 문구를 셋팅한다. ###
    def setMsg(self, msg):
        self.msg = msg
        
    ### 문구를 디바이스의 시리얼과 함께 서버로 송신한다. ###
    # def SendMsg(self):
    #     self.sock.sendall(self.msg.encode())
    def SendMsg(self):
        self.msg = _device_serial + ";" + self.msg
        self.sock.sendall(self.msg.encode())
        
    ### 셋팅된 host와 port를 이용해 서버에 접속하고 서버로부터 메세지를 받는 데몬 스레드를 실행한다. ###
    def ConnectToServer(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.t = Thread(target = self.ReceiveMsg, args = (self.sock,))
        self.t.daemon = True
        self.t.start()              

    ### 서버로부터 메세지를 받는 메소드, 따로 실행할 필요가 없이 서버와 연결하는 순간 Thread로 실행된다. ###
    def ReceiveMsg(self, sock):
        while True:
            try:
                data = sock.recv(1024)
                if not data: break
                # print("에코메세지 : " + data.decode()) 에코서버일 경우, 해당 내용을 출력
                # 수신된 내용은 반드시 decode 되야 한다.
                # 수신된 내용을 큐에 담아 사용한다.(예정)
            except: 
                pass
        
    ### 연결을 끊는다. ###
    def ConnectClose(self):
        print("연결이 종료되었습니다")
        self.sock.close()

''' 테스트용 예제, 서버와의 채팅 기능
a = ConnectServer()
a.ConnectToServer()

while True:
    print("메세지를 입력하세요 : ", end = '')
    msg = input()
    a.setMsg(msg)
    a.SendMsg()dksl 
    if msg == "exit":
        a.ConnectClose()
        break
'''