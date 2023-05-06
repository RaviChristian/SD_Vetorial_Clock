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
        message = (self.process_id, self.vector_clock)
        recipient_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recipient_socket.connect(('localhost', 5000 + recipient_id))
        recipient_socket.sendall(pickle.dumps(message))
        recipient_socket.close()

    def receive_messages(self):
        while True:
            conn = self.socket.accept()[0]
            data = conn.recv(4096)
            sender_id, sender_vector_clock = pickle.loads(data)
            self.vector_clock[sender_id] = max(self.vector_clock[sender_id], sender_vector_clock[sender_id])
            self.vector_clock[self.process_id] += 1
            print(f"O Processo {self.process_id}: recebeu mensagem do processo {sender_id} com a vetor de clock {sender_vector_clock}")
            conn.sendall(b"OK")
            conn.close()

num_processes = 4
processes = [Process(i, num_processes) for i in range(num_processes)]

processes[0].send_message(1)
time.sleep(2)
processes[1].send_message(2)
time.sleep(2)
processes[2].send_message(3)
time.sleep(2)
processes[0].send_message(3)
time.sleep(2)

