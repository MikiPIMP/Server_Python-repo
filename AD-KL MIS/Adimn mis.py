#Admin skripta
from pynput.mouse import Button, Controller
import os, time
import socket
import pickle

print("Program za daljinsko upravljanje [Admin]: ")
print("-" * 60)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local = socket.gethostname()
port = 11110
s.bind((local, port))
s.listen(1)

mouse = Controller()

def kontrola_mis(): 
    while True:
        M = '{}'.format(mouse.position)   #pozicije(x, y), tupl u stingu
                        
        m1 = M.replace("(","") 
        m2 = m1.replace(')','')
        m3 = m2.replace(" ","")
                                        
        L = m3.split(",")                 #lista 
                                            
        kordinata_2 = L.pop()             # kordinata druga
        kordinata_1 = L.pop()             # kordinata prva

        pozicija_mis1 = int(kordinata_1)  # horizontalna kordinata (x) "prva" za mis 
        pozicija_mis2 = int(kordinata_2)  # vertikalna kordinata (y) "druga" za mis 

        D = {'kord_x_1' : pozicija_mis1, 'kord_y_2' : pozicija_mis2}

        return pickle.dumps(D)

while True:
    print("Server - aktivan: ")
    conn, addr = s.accept()
    print("Konekcija ostvarena sa: ", addr)
    komanda = input("Komanda>>")
    
    if komanda[:5] == "#MIS#":
        while True:
            msg = conn.sendall(kontrola_mis())
    

