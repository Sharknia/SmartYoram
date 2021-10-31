import Protocol
import socketserver
import threading

_default_host = Protocol._default_host
_default_port = Protocol._default_port
lock = threading.Lock() # 동기화 진행 스레드

class Manager:
    # 지금은 리스트로 관리하지만 추후 DB로 관리 예정
    def __init__(self):
        self.devices = {}
        self.users = {}

    #새로운 디바이스 추가
    def AddDevices(self, devicename, conn, addr):
        if devicename in self.devices :
            conn.send('이미 등록된 디바이스입니다. \n'.encode())
            return None

        lock.acquire() #쓰레드 동기화 막기 위한 락
        self.devices[devicename] = (conn, addr)
        lock.release() # 업데이트 이후 락 해제

        self.sendMessageToAll('[%s]디바이스 추가됨.' % devicename)
        print('디바이스 추가됨!')

        return devicename

    #새로운 안드로이드(유저) 추가
    def AddUsers(self, userid, conn, addr):
        if userid in self.devices:
            conn.send('이미 등록된 사용자입니다. \n'.encode())
            return None

        lock.acquire()  # 쓰레드 동기화 막기 위한 락
        self.devices[userid] = (conn, addr)
        lock.release()  # 업데이트 이후 락 해제

        self.sendMessageToAll('[%s]디바이스 추가됨.'%userid)
        print('유저 추가됨!')

        return userid

    # 유저나 디바이스 삭제 : 미구현
    def RemoveDevice(self, devicename):
        pass
    def RemoveUser(self, userid):
        pass

    # 메세지 처리 부분.
    def messageHandler(self, userid, msg):
        split = msg.split(';')
        # 디바이스에서 온 메세지일 경우(현재 시리얼은 고려하지 않고 진행한다.)
        # 1. 잠든 시간 저장
        # 2. 깬 시간 저장
        if split[0] == Protocol._device:
            if split[2] == Protocol.pattern_time_sleep:
                pass
            if split[2] == Protocol.pattern_time_wakeup:
                pass

        # 유저에게서 온 메세지의 경우
        # 1. 자동수면 모드 ON : 디바이스로 자동 수면모드 ON 을 쏜다.
        # 2. 자동수면 모드 OFF : 디바이스로 자동 수면모드 OFF 를 쏜다.
        # 3. 수면 패턴 분석 자료 요청 : 유저에게 원하는 구간의 분석 자료를 리턴한다.
        if split[0] == Protocol._user:
            if split[2] == Protocol.auto_sleep_mode_on:
                pass
            if split[2] == Protocol.auto_sleep_mode_off:
                pass
            if split[2] == Protocol.request_sleep_pattern_data:
                pass

    def SendMsgToDevice(self, msg):
        for conn, addr in self.devices.values():
            conn.send(msg.encode())

    def SendMsgToUser(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())

class TcpHandler(socketserver.BaseRequestHandler):
    userman = Manager()

    #클라이언트 접속시 클라이언트 주소 출력
    def handle(self):
        print('[%s] 연결됨' % self.client_address[0])

        try:


    def RegisterUser(self):
        while True:
            self.request.send("로그인 ID")