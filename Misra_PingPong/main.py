import socket
import threading
import time
import sys
import keyboard


class PingPongConnectionTCP:
    def __init__(self, addr_my, addr_next):
        self.addr_my = addr_my
        self.__addr_next = addr_next
        self.__addr_before = ()
        self.__node_to_recv = None
        self.__node_to_send = None

    def create_node_send(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.__addr_next)
        self.__node_to_send = s

    def create_node_recv(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(self.addr_my)
        s.listen()
        c, a = s.accept()
        self.__node_to_recv = c
        self.__addr_before = a

    def recv_msg(self):
        data = self.__node_to_recv.recv(4)
        if not data:
            return None
        number = int.from_bytes(data, byteorder="big", signed=True)
        return number

    def send_msg(self, value):
        data = value.to_bytes(4, byteorder="big", signed=True)
        self.__node_to_send.sendall(data)


class PingPong(PingPongConnectionTCP):
    def __init__(self, my_ip, my_port, next_ip, next_port, special_mode):
        super().__init__((my_ip, int(my_port)), (next_ip, int(next_port)))
        special_mode = int(special_mode)
        print("|", special_mode)
        self.__m = 0
        self.__ping = 1
        self.__pong = -1
        self.__has_ping = False
        print("1")
        if special_mode:
            self.create_node_send()
            self.create_node_recv()
        else:
            self.create_node_recv()
            self.create_node_send()

        if special_mode:
            self.sending(True)
            self.sending(False)
        print("Loop")
        self.__loop()

    def __loop(self):
        while True:
            time.sleep(1)
            value = self.received()
            if value is None:
                continue
            if value == self.__m:
                self.regenerate(value)
            else:
                self.__m = value
            if value > 0:
                self.__has_ping = True
                self.__critical_section()
            else:
                if self.__has_ping:
                    self.incarnate(value)
                self.sending(False)

    def regenerate(self, value):
        if value > 0:
            print(self.addr_my, "Rekonstrukcja PONGA: ", -value)
            self.__pong = -value
            self.sending(False)
        else:
            print(self.addr_my, "Rekonstrukcja PINGA: ", -value)
            self.__ping = -value
            self.sending(True)

    def incarnate(self, value):
        v = (value if value > 0 else -value) + 1
        self.__ping = v
        self.__pong = -v

    def sending(self, send_ping):
        if keyboard.is_pressed('i'):
            print(self.addr_my, "ZAGUBIENIE PINGA")
            return
        if keyboard.is_pressed('o'):
            print(self.addr_my, "ZAGUBIENIE PONGA")
            return
        value = self.__ping if send_ping else self.__pong
        self.send_msg(value)
        print(self.addr_my, "Send: ", value)

    def received(self):
        value = self.recv_msg()
        print(self.addr_my, "Recv: ", value)
        return value

    def __critical_section(self):
        threading.Thread(target=self.__critical_section_body).start()

    def __critical_section_body(self):
        print(self.addr_my, "CS: Start")
        time.sleep(5)
        print(self.addr_my, "CS: End")
        self.__has_ping = False
        self.sending(True)


def main(argv):
    PingPong(argv[1], argv[2], argv[3], argv[4], argv[5])

if __name__ == "__main__":
    main(sys.argv)