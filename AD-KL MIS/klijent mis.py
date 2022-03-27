#Klijent skripta
from pynput.mouse import Button, Controller
import os, time
import socket
import subprocess
import pickle
    
print("Program za daljinsko upravljanje [Klijent]: ")
print("-" * 60)

host = "192.168.0.16"
port = 11110

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print('Konekcija je ostvarena sa: ', host, ';', port)

mouse = Controller()

def kord_p(A):
    while True:
        prva_k = A.get("kord_x_1")
        druga_k = A.get("kord_y_2")
        M = mouse.position = (prva_k, druga_k)
        return M

while True:
    prijem = s.recv(1024*10)
    A = pickle.loads(prijem)
    kord_p(A)
    
    
        

