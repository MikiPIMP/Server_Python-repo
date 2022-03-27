import socket
import time
import threading
import autopy
import cv2
import numpy as np
import binascii
import pyfakewebcam
import subprocess
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

virtualCamera = subprocess.run(["sudo", "modprobe", "v4l2loopback", "devices=1", "video_nr=20", "card_label='Wireless-X Camera'", "exclusive_caps=1"])
print('\n---------------- Milanov Server [Admin] v0.1 ----------------\n')

width, height = autopy.screen.size()

curr_x, curr_y = autopy.mouse.location()

remote_x = curr_x/2

remote_y = curr_y/2

s = ''

cameraSocket = ''

img_width = 720

img_height = 480

camera = pyfakewebcam.FakeWebcam('/dev/video20', img_width, img_height)

thread_run = True

keyboard = KeyboardController()
 
mouse = MouseController()

mouse_speed = 2

screenshot_count = 0

def bind_sockets():
    try:
        global s, cameraSocket
        
        cameraSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cameraSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cameraSocket.settimeout(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cam_port = 9998
        cameraSocket.bind(("0.0.0.0", cam_port))
        cameraSocket.listen(10)
        key_port = 6666
        s.bind(("0.0.0.0", key_port))
        s.listen(10)
        
        print("Server - Aktivan")
        print("Autokonekcija sa IP Adresom: \n")
        ps = subprocess.Popen(('hostname', '-I'), stdout = subprocess.PIPE)
        output = subprocess.check_output(('awk', '{print $1}'), stdin = ps.stdout)
        ps.wait()  
        print(output.decode("utf-8"))
        print('Kontrola [Ctrl+C] za prekidanje servera')
        
    except socket.error as msg:
        print("Socket Error: " + str(msg))
        time.sleep(5)
        bind_sockets()

special_key_android_dictionary = {"F1": "F1", "F2":"F2", "F3":"F3", "F4":"F4", "F5":"F5", "F6":"F6", "F7":"F7", "F8":"F8", "F9":"F9", "F10":"F10", "F11":"F11", "F12":"F12", "Alt":"ALT", "Backspace":"BACKSPACE",  "Caps\nLock":"CAPS_LOCK",  "Ctrl":"CONTROL", "Delete":"DELETE",  "↓":"DOWN_ARROW",  "End":"END", "Esc":"ESCAPE", "Home":"HOME", "←":"LEFT_ARROW", "META":"META", "Page Down":"PAGE_DOWN", "Page Up":"PAGE_UP", "Enter":"RETURN", "→":"RIGHT_ARROW", "Shift":"SHIFT", "Space":"SPACE", "↑":"UP_ARROW", "Tab":"Tab"}

def mouse_keyboard_connections():
    global thread_run, curr_x, curr_y, remote_x, remote_y
    global screenshot_count
    thread_run = True
    prev_x = int(width/2)
    prev_y = int(height/2)
    while thread_run:
        try:
            conn, address = s.accept()
            peer_response = str(conn.recv(1024).decode("utf-8"))
            if "!#Mouse#!" in peer_response:
                peer_response = peer_response.split("!#Mouse#!")[1]
                xy = peer_response.split(',')
                if len(xy) == 2:
                    mouse.position = (float(xy[0])*width, float(xy[1])*height)
            elif "!#Keyboard#!" in peer_response:
                peer_response = peer_response.split("!#Keyboard#!")[1]
                if peer_response in special_key_android_dictionary.keys():
                    
                    if peer_response == "Backspace":
                        keyboard.press(Key.backspace)
                        keyboard.release(Key.backspace)
                    
                    elif peer_response == "Tab":
                        keyboard.press(Key.tab)
                        keyboard.release(Key.tab)
                    else:
                        autopy.key.tap(eval("autopy.key.Code." + special_key_android_dictionary[peer_response]))
                elif peer_response == "Cmd":
                    keyboard.press(Key.cmd)
                    keyboard.release(Key.cmd)
                elif peer_response == "Print\nScreen":
                    print("\nSkrinsot sacuvan kao: " + "screenshot_" + str(screenshot_count) + ".png")
                    autopy.bitmap.capture_screen().save(str("screenshot_" + str(screenshot_count) + ".png"))
                    screenshot_count += 1
                else:
                    
                    if peer_response.isalnum and peer_response != "'" and peer_response != "<":
                        autopy.key.tap(peer_response.lower())
                    elif peer_response == "'":
                        keyboard.press("'")
                        keyboard.release("'")
                    elif peer_response == "<":
                        keyboard.press("<")
                        keyboard.release("<")
            elif "!#MouseClick#!" in peer_response:
                if "LEFT" in peer_response:
                    mouse.click(Button.left, 1)
                else:
                    mouse.click(Button.right, 1)
            elif "!#MouseScroll#!" in peer_response:
                if "SCROLL \nUP" in peer_response:
                    mouse.scroll(0, 2)  
                else:
                    mouse.scroll(0, -2)  
                    
            elif "!#Test#!" in peer_response:
                conn.send(bytes("Afirmativno " + str(int(width/mouse_speed)) + " " + str(int(height/mouse_speed)),"utf-8"))
            conn.close()
        except Exception as msg:
            pass

def camera_stream_connections():
    thread_run = True
    image_window_open = False
    while thread_run:
        try:
            conn, address = cameraSocket.accept()
            client_response = str(conn.recv(1024).decode("utf-8"))
            while "#$#$#$" not in client_response:
                client_response += str(conn.recv(1024).decode("utf-8"))
            pic = client_response.partition("#$#$#$")[0]
            client_response = client_response.partition("#$#$#$")[2]
            
            b = binascii.a2b_base64(pic)
            nparr = np.frombuffer(b, dtype = np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img = cv2.resize(frame, (img_width, img_height))
            try:
                camera.schedule_frame(img)
            except Exception as msg:
                print ("Greska: " + str(msg))
            
            conn.close()
        except Exception as msg:
            if "timed out" not in str(msg):
                print("Kamera_stream_konekcija() - Error{138}: " + str(msg))
            if image_window_open:
                cv2.destroyWindow("Main")
                image_window_open = False
                pass

def listening_connections():
    mouse_thread = threading.Thread(target = mouse_keyboard_connections)
    mouse_thread.daemon = True
    
    camera_thread = threading.Thread(target = camera_stream_connections)
    camera_thread.daemon = True
    mouse_thread.start()
    camera_thread.start()
    mouse_thread.join()
    camera_thread.join()


t2 = threading.Thread(target = listening_connections)
t2.daemon = True
t2.start()
t2.join()
