import requests
from bs4 import BeautifulSoup
import pandas as pd

sign = input("what's yer sign ").lower()

if sign == 'aries':
    sign = 1
elif sign == 'taurus':
    sign = 2
elif sign == 'gemini':
    sign = 3
elif sign == 'cancer':
    sign = 4
elif sign == 'leo':
    sign = 5
elif sign == 'virgo':
    sign = 6
elif sign == 'libra':
    sign = 7
elif sign == 'scorpio':
    sign = 8
elif sign == 'sagittarius':
    sign = 9
elif sign == 'capricorn':
    sign = 10
elif sign == 'aquarius':
    sign = 11
elif sign == 'pisces':
    sign = 12
else:
    sign = 0

if sign == 0:
    print('come back when you can spell your sign right, jeez')
else:
    url = f'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={sign}'

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.h1

    date = soup.strong

    horoscope = date.next_sibling

    traits = soup.find('p', class_ = 'italicize')

    print()
    print(f'~~~{title.text.strip()}~~~')
    print(traits.text.strip())
    print(date.text.strip())
    print(horoscope.text.strip().replace('- ', ''))
    print()
    
