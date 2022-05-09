import socket
import sys
import argparse
import threading

from game.hangman import Hangman
from game.draw import phases

backlog = 5
data_payload = 16 # bytes


class HangmanServer:

    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port
        self.connections = [] # empty list. store clients 

        # create TCP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # enable reuse address/port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to the port
        server_address = (host, port)
        print("Starting up echo server on %s port %s" % server_address)
        self.sock.bind(server_address)

        # listen to clients backlog variable specifies the max number
        self.sock.listen(backlog)

        # start game
        self.hangman = Hangman()

        # receive connections
        # while len(self.connections) < 1:
        #     client, address = self.sock.accept()
        #     print(f"Received connection from {client}")
        #     self.connections.append((client, address))
        #     threading.Thread(target=self.run, args=(client), daemon=True).start()

    def run(self, client):

        while True:
            if len(self.connections) == 1:
                for conn in self.connections:
                    conn[0].send("Game Start!".encode('utf-8'))
                break

        running = True
        
        while running:
            try:
                if self.hangman.tries <= 0:
                    for conn in self.connections:
                        conn[0].send(
                            f"You've all lost! The answer is {self.hangman.answer}".encode('utf-8'))
                    self.sock.close()
                    running = False
                    break

                if self.hangman.won:
                    for conn in self.connections:
                        conn[0].send(
                            f"You've all won! The answer is {self.hangman.answer}".encode('utf-8'))
                    self.sock.close()
                    running = False
                    break

                # self.sock.sendall(''.encode('utf-8'))

                guess = client.recv(data_payload).decode('utf-8')
                if guess:
                    if len(guess) == 1 and guess.isnumeric():
                        guillotine, av_nums, is_correct = self.hangman.check(guess)
                        
                        # create message
                        message = f"%s\n%s\n\n%s is received\n\n%s\n\n%s" % \
                            (guillotine, self.hangman.empty_answer, \
                            guess, is_correct, av_nums)

                        # send data to all including ourselves
                        for neighbor_conn in self.connections:
                            neighbor_conn[0].send(message.encode('utf-8'))
                    else:
                        client.send(
                            'Guess number must be a digit of integer'.encode('utf-8'))
            except KeyboardInterrupt:
                for conn in self.connections:
                    conn[0].send('stop'.encode('utf-8'))
                    conn[0].close()
                self.sock.close()
            except Exception:
                for conn in self.connections:
                    conn[0].close()
                self.sock.close()
                

# driver code
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(
    #     description="Hangman using python socket",
    #     usage="python server.py --name=server --host=<ipv4_address> --port=8800")
    # parser.add_argument("--name", action="store", dest="name", type=str, required=True)
    # parser.add_argument("--host", action="store", dest="host", type=str, required=True)
    # parser.add_argument("--port", action="store", dest="port", type=int, required=True)

    # given_agrs = parser.parse_args()

    # name = given_agrs.name
    # host = given_agrs.host
    # port = given_agrs.port

    name = "server"
    host = '192.168.1.42'
    port = 8800

    hangmanserver = HangmanServer(name, host, port)
    try:
        while len(hangmanserver.connections) < 5:
            # receive client
            client, address = hangmanserver.sock.accept()
            print(f"Received connection from {client}")
            hangmanserver.connections.append((client, address))
            threading.Thread(target=hangmanserver.run, args=[client], daemon=True).start()
    except Exception as e:
        hangmanserver.sock.close()
    finally:
        print("Server Shutdown")

