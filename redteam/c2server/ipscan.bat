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
SET /A "OCTET1= %i1% & %m1%"
SET /A "OCTET2= %i2% & %m2%"
SET /A "OCTET3= %i3% & %m3%"
SET /A "OCTET4= (%i4% & %m4%) + 1"
echo FIRSTIP: %OCTET1%.%OCTET2%.%OCTET3%.%OCTET4%

::LASTIP
SET /A "OCTET1= %i1% & %m1% | 255-%m1%"
SET /A "OCTET2= %i2% & %m2% | 255-%m2%"
SET /A "OCTET3= %i3% & %m3% | 255-%m3%"
SET /A "OCTET4= (%i4% & %m4% | 255-%m4%)-1"
echo LASTIP: %OCTET1%.%OCTET2%.%OCTET3%.%OCTET4%



endlocal