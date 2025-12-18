# Nmap

Syntax:
```nmap <scan types> <options> <target>``` 

Network Scan
```
sudo nmap 10.129.2.0/24 -sn -oA tnet | grep for | cut -d" " -f5

-sn no port scan
```

Quick TCP Scan
```nmap -sS -Pn -n --disable-arp-ping -T4  --max-retries=2 -sV -p- 10.129.14.103```

Show Status
```--stats-every=5s```

Vuln, Exploit
```nmap --script vuln, exploit -p 80,143 10.129.14.103```

#Banner
```whatweb http://10.129.146.191```

# Infrastructure Enumeration 
HTTPS -> SSL Certificate\
Subdomain finder -> Certificate into crt.sh 
```
curl -s https://crt.sh/\?q\=inlanefreight.com\&output\=json | jq .
```

Nur Domains 
```
curl -s https://crt.sh/\?q\=inlanefreight.com\&output\=json | jq . | grep name | cut -d":" -f2 | grep -v "CN=" | cut -d'"' -f2 | awk '{gsub(/\\n/,"\n");}1;' | sort -u
```

Prüfen ob Domaine erreichbar ist (Keine third party hosts, nicht im Scope)
```
for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f1,4;done
```

Shodan - IP List\
IP-Adressen werden im Internet gesucht. Ergebnis: Verbundene IoT-Geräte

```
nunle@htb[/htb]$ for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f4 >> ip-addresses.txt;done
nunle@htb[/htb]$ for i in $(cat ip-addresses.txt);do shodan host $i;done
```

DNS Records
```
dig any [...]
```





