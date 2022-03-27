#Administrator kod
import socket

print("Program za daljinsko upravljanje [admin]: ")
print("-" * 60)

soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = soket

local_pc = ""
port = 19304

s.bind((local_pc, port))
s.listen(5)

while True:
    print("Server - aktivan: ")
    conn, addr = s.accept()
    print("Konekcija ostvarena sa: ", addr)

    try:
        while True:
            komanda = input("Komanda: ")
            if len(komanda) > 0:
                conn.sendall(komanda.encode())
                paket = conn.recv(1024)
                dekodovan = paket.decode()
                print(dekodovan)
            else:
                print("Nema komande..!")
    except:
        print("Konekcija prekinuta sa: ", addr)


