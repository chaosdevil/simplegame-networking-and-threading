import socket
import sys
import argparse
import re
import threading

class HangmanClient():
    def __init__(self, name, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.name = name
        self.host = host
        self.port = port
        self.connecting = True

        self.prompt = "[[%s]] >> " % (self.name)
 
        server_address = (host, port)
        print("Connecting to %s port %s" % server_address)

        # connect to echo server
        self.sock.connect(server_address)
        print(f"Connection to {host}:{port} is successful")
        
    def run(self):

        def sender():
            while True:
                sending_message = sys.stdin.readline().strip()
                sys.stdin.flush()
                if sending_message:
                    self.sock.send(sending_message.encode('utf-8'))
                if self.connecting == False:
                    break

        def receiver():
            while True:
                received_message = self.sock.recv(4096).decode('utf-8')
                if received_message:
                    sys.stdout.write(received_message + '\n')
                    signal = re.search(r'lost*|won*', received_message)
                    if signal:
                        self.sock.close()
                        self.connecting = False
                        break
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

        _ = self.sock.recv(4096).decode('utf-8')

        receiver_thread = threading.Thread(target=receiver)
        sender_thread = threading.Thread(target=sender)

        sender_thread.start()
        receiver_thread.start()

        try:
            sender_thread.join()
            receiver_thread.join()
        except KeyboardInterrupt:
            self.sock.close()
            self.connecting = False
        except Exception as e:
            self.sock.close()
            self.connecting = False
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Hangman using python socket",
        usage="python hangmanclient.py --name=<your name> --host=<ipv4_address> --port=8800")
    parser.add_argument("--name", action="store", dest="name", type=str, required=True)
    parser.add_argument("--host", action="store", dest="host", type=str, required=True)
    parser.add_argument("--port", action="store", dest="port", type=int, required=True)

    given_agrs = parser.parse_args()

    name = given_agrs.name
    host = given_agrs.host
    port = given_agrs.port
    
    # name = 'sura'
    # host = '192.168.1.42'
    # port = 8800

    try:
        hangmanserver = HangmanClient(name, host, port)
        hangmanserver.run()
    except Exception as e:
        print(e)
        print("Server stopped")
        # sys.exit(-1)