import socket
import pickle
import time
import threading

class Process:
    def __init__(self, process_id, num_processes):
        self.process_id = process_id
        self.num_processes = num_processes
        self.vector_clock = [0] * num_processes
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 5000 + process_id))
        self.socket.listen()
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self, recipient_id):
        self.vector_clock[self.process_id] += 1
        print(f"Processo {self.process_id} enviou a mensagem. Clock: {self.vector_clock}")
        message = (self.process_id, self.vector_clock)
        recipient_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recipient_socket.connect(('localhost', 5000 + recipient_id))
        recipient_socket.sendall(pickle.dumps(message))
        recipient_socket.close()

    def receive_messages(self):
        while True:
            conn = self.socket.accept()[0]
            data = conn.recv(4096)
            sender_vector_clock = pickle.loads(data)
            for p in range(self.num_processes):
                max_value = max(self.vector_clock[p], sender_vector_clock[p])
                self.vector_clock[p] = max_value
            print(f"Processo {self.process_id} recebe a mensagem. Clock: {self.vector_clock} \n")

            conn.close()

num_processes = 4
processes = [Process(i, num_processes) for i in range(num_processes)]

processes[0].send_message(1)
time.sleep(2)
processes[1].send_message(2)
time.sleep(2)
processes[2].send_message(0)
time.sleep(2)
processes[3].send_message(2)
time.sleep(2)

