::QUELLEN https://superuser.com/questions/1256951/how-do-i-extract-the-ipv4-ip-addresses-from-the-output-of-ipconfig-and-then-fil
::QUELLEN https://stackoverflow.com/questions/43876891/given-ip-address-and-netmask-how-can-i-calculate-the-subnet-range-using-bash

@echo off

setlocal
setlocal enabledelayedexpansion
SET COUNT=1
for /f "usebackq tokens=2 delims=:" %%a in (`ipconfig ^| findstr /r "[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*"`) do (
  set _temp=%%a
  SET var!COUNT!=!_temp:~1!
  SET /a COUNT=!COUNT!+1
  )
SET HOSTIP=%var1%
SET SUBNETMASK=%var2%

ECHO HOSIP: %HOSTIP%
ECHO SUBNETMASK: %SUBNETMASK%

::IP-Adresse aufteilen
set HOSTIP=%HOSTIP:.= % 
SET COUNT=1
(for %%a in (%HOSTIP%) do ( 
   SET i!COUNT!=%%a
   SET /a COUNT=!COUNT!+1
))

::SUBNETMASKE AUFTEILEN
set SUBNETMASK=%SUBNETMASK:.= % 
SET COUNT=1
(for %%a in (%SUBNETMASK%) do ( 
   SET m!COUNT!=%%a
   SET /a COUNT=!COUNT!+1
))

::NETWORK
SET /A "OCTET1= %i1% & %m1%"
SET /A "OCTET2= %i2% & %m2%"
SET /A "OCTET3= %i3% & %m3%"
SET /A "OCTET4= %i4% & %m4%"
echo NETWORK: %OCTET1%.%OCTET2%.%OCTET3%.%OCTET4%


::BROADCAST
SET /A "OCTET1= %i1% & %m1% | 255-%m1%"
SET /A "OCTET2= %i2% & %m2% | 255-%m2%"
SET /A "OCTET3= %i3% & %m3% | 255-%m3%"
SET /A "OCTET4= %i4% & %m4% | 255-%m4%"
echo BROADCAST: %OCTET1%.%OCTET2%.%OCTET3%.%OCTET4%

::FIRSTIP
SET /A "FIRSTIPOCTET1= %i1% & %m1%"
SET /A "FIRSTIPOCTET2= %i2% & %m2%"
SET /A "FIRSTIPOCTET3= %i3% & %m3%"
SET /A "FIRSTIPOCTET4= (%i4% & %m4%) + 1"
echo FIRSTIP: %FIRSTIPOCTET1%.%FIRSTIPOCTET2%.%FIRSTIPOCTET3%.%FIRSTIPOCTET4%

::LASTIP
SET /A "LASTIPOCTET1= %i1% & %m1% | 255-%m1%"
SET /A "LASTIPOCTET2= %i2% & %m2% | 255-%m2%"
SET /A "LASTIPOCTET3= %i3% & %m3% | 255-%m3%"
SET /A "LASTIPOCTET4= (%i4% & %m4% | 255-%m4%)-1"
echo LASTIP: %LASTIPOCTET1%.%LASTIPOCTET2%.%LASTIPOCTET3%.%LASTIPOCTET4%

::PING ALL IPS
SET /A FIRSTIPOCTET4=108
SET /A LASTIPOCTET4=115
SET START=%FIRSTIPOCTET4%
SET END=%LASTIPOCTET4%
SET IPSTART=%START%



goto zweiteIDEE

:ersteIDEE
::ERGEBNISSE IN EIN ARRAY HINZUFÜGEN + AUSGABE
SET COUNTER=0
FOR /L %%a in (%START%,1,%END%) do (
    ping -n 1 192.168.2.!IPSTART! | findstr "TTL=" > nul || SET LISTE[!COUNTER!].STATUS=OFFLINE 
    SET LISTE[!COUNTER!].IP=192.168.2.!IPSTART!
    ECHO LISTE[!COUNTER!].IP SCANNING
    SET /A COUNTER +=1
    SET /A IPSTART +=1
    
)
ECHO %COUNTER%
SET /A END=%COUNTER%-1
for /l %%n in (0,1,%END%) do ( 
    if [!LISTE[%%n].STATUS!] == [] (
        ECHO ONLINE !LISTE[%%n].IP!
    ) else (echo !LISTE[%%n].STATUS!: !LISTE[%%n].IP!)
)

:zweiteIDEE
::ERGEBNISSE IN DIREKT AUSGEBEN
FOR /L %%a in (%START%,1,%END%) do (
    ping -n 1 192.168.2.!IPSTART! | findstr "TTL=" > nul
    IF not errorlevel 1 (
        ECHO 192.168.2.!IPSTART! ONLINE
    ) ELSE (
        ECHO 192.168.2.!IPSTART! OFFLINE
    )
    SET /A IPSTART +=1
    
)
endlocal