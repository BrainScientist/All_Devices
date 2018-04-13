#SetPDRdefaults.py
import os
import socket
# Recording variables
QUES = []
QUES.append({'sub': 'b001', 'session': '01', 'date': '160513', 'sessionID': '160513_b001_01'})
QUES.append({'trialdur': 70000, 'framew': 640, 'frameh': 480, 'framerate': 90, 'framedur':4000})
QUES.append({'host_name': 'RPi-B', 'host_ip': '192.168.0.7'})
QUES.append({'ISO': 100, 'awb': 'off'})
# Mount networked HDD as Pi backup drive
os.system("sudo mount -t cifs -o guest //192.198.0.32/Volume_1/ /mnt/netHDmnt")

# Filename variables
FN=[]
FN.append({'recdir': QUES[0]['sessionID'],'recfile': QUES[0]['sessionID'] + "/" + QUES[0]['sessionID'] + "_01.h264" })
FN.append({'bakpath':'/mnt/netHDmnt'})

#get host name to label video files
host_name = socket.gethostname() # needed for naming files
host_ip = socket.gethostbyname(host_name)
QUES[2]['host_name'] = host_name
QUES[2]['host_ip'] = host_ip