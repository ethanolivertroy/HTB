# Hack the Box — Nibbles

In this walkthrough, we will be exploring the "Nibbles" machine from Hack the Box, without using Metasploit.

![](https://cdn-images-1.medium.com/max/1600/1*Onn-BJuNI9nwCNGdPO9_Lw.png)

## Reconnaissance

We begin with our reconnaissance phase, where we gather as much information as possible about the target.

### Nmap Scan

We start with an Nmap scan to identify the open ports and running services on the target machine. We run the following command:

```
nmap -sC -sV -oN nmap_scan.txt 10.10.10.75
```

Where:

-   `sC` runs default scripts
-   `sV` performs version detection
-   `oN` saves the output in a text file named `nmap_scan.txt`
-   `10.10.10.75` is the IP address of the target machine

From the scan results, we see that the target machine has an HTTP service running on port 80.

![](https://cdn-images-1.medium.com/max/1600/1*GRmcaLa6rwd59_1HwuRhxQ.png)

### Gobuster Scan

We now run a Gobuster scan to enumerate directories and files on the web server. We run the following command:

```
gobuster dir -u http://10.10.10.75/ -w /usr/share/wordlists/dirb/common.txt -x txt,php,html -o gobuster_scan.txt
```

Where:

-   `dir` specifies a directory/file busting mode
-   `u` specifies the URL to scan
-   `w` specifies the wordlist to use
-   `x` specifies the file extensions to search for
-   `o` specifies the output file name
-   `10.10.10.75` is the IP address of the target machine

![](https://cdn-images-1.medium.com/max/1600/1*i9GhDZbQgNBlqlxUCo-FEw.png)

### View Page Source

![](https://cdn-images-1.medium.com/max/1600/1*5iuHsI0dECd7cvXn2t40LQ.png)

We see that there is a `/nibbleblog` directory.

## Exploitation

We visit the page and see that it is a blogging platform.

![](https://cdn-images-1.medium.com/max/1600/1*CUklQUlSTqFD7YYD9vUfQQ.png)

### More Gobuster

We find a readme

![](https://cdn-images-1.medium.com/max/1600/1*203bDGah-1CCvPwmGC2x7w.png)

The readme gives us version info

![](https://cdn-images-1.medium.com/max/1600/1*jvTqOnnE6l8HfNamxv4DSw.png)

We search for exploits related to Nibbleblog and find a remote code execution vulnerability.

[https://packetstormsecurity.com/files/133425/NibbleBlog-4.0.3-Shell-Upload.html](https://packetstormsecurity.com/files/133425/NibbleBlog-4.0.3-Shell-Upload.html)

The vulnerability is in the `params.inc.php` file, which takes a user input and passes it to the `eval()` function without any sanitization.

We can exploit this vulnerability to execute arbitrary code on the server.

### Manual Exploitation

Login into the admin dashboard

![](https://cdn-images-1.medium.com/max/1600/1*63u_3w8Y-C69yoOCpcnaOw.png)

We create a PHP reverse shell script and upload it to the server using the Nibbleblog file upload feature.

[https://pentestmonkey.net/tools/web-shells/php-reverse-shell](https://pentestmonkey.net/tools/web-shells/php-reverse-shell)

![](https://cdn-images-1.medium.com/max/1600/1*KykFqcmvSZkG45p0XTbkDw.png)

We then start a netcat listener on our machine and visit the uploaded PHP file in the browser.

In the browser, navigate to the image we just uploaded to run the reverse shell script.

http://10.10.10.75/nibbleblog/content/private/plugins/my_image/php-reverse-shell.php

I had to change the file name to just image.php for the shell to pop

![](https://cdn-images-1.medium.com/max/1600/1*lSRHLJpzFYcyHq-rv5polQ.png)

We get a shell on the server and can now explore the file system.

Let’s upgrade to a better shell:

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

After a little navigating, we find the user flag

![](https://cdn-images-1.medium.com/max/1600/1*e5nZp06kx1cI4J0EOSjjlQ.png)

## Privilege Escalation

We also saw a file named “personal.zip”. We unzip it.

We run the `sudo -l` command to check if we have any sudo privileges.

We see that we can run `/home/nibbler/personal/stuff/monitor.sh` as root which was in the zip file.

If we call a shell in that script, we can run it as root.

We modify a monitor.sh file to open a shell as root:

![](https://cdn-images-1.medium.com/max/1600/1*zNTw0FsEqk52o1DDaTk3Yw.png)

Once we are root we can navigate and find that flag

![](https://cdn-images-1.medium.com/max/1600/1*6JAAvVjMLg19ZzV27pciwA.png)

## Conclusion

In this walkthrough, we explored the Nibbles machine from Hack the Box and exploited a remote code execution vulnerability to gain access to the server. We then escalated our privileges to root by modifying a monitoring script that ran with sudo privileges.
