import requests
from bs4 import BeautifulSoup
import re

sign = input("what's yer sign ").lower()

if sign == 'aries':
    signNumber = 1
elif sign == 'taurus':
    signNumber = 2
elif sign == 'gemini':
    signNumber = 3
elif sign == 'cancer':
    signNumber = 4
elif sign == 'leo':
    signNumber = 5
elif sign == 'virgo':
    signNumber = 6
elif sign == 'libra':
    signNumber = 7
elif sign == 'scorpio':
    signNumber = 8
elif sign == 'sagittarius':
    signNumber = 9
elif sign == 'capricorn':
    signNumber = 10
elif sign == 'aquarius':
    signNumber = 11
elif sign == 'pisces':
    signNumber = 12
else:
    print('come back when you can spell your sign right, jeez')
    exit() # added this so that the script stops running if there's a typo

url = f'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={signNumber}'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Scrape traits of sign
traits = soup.find('p', class_ = 'italicize')

# Scrape sign
title = soup.h1

# Scrape today's date
date = soup.strong

# Scrape today's horoscope text
horoscope = date.next_sibling

# Scrape traits of sign
traits = soup.find('p', class_ = 'italicize')

# Print horoscope and strip text of html markup
print()
print(f'~~~{title.text.strip()}~~~')
print(traits.text.strip())
print(date.text.strip())
print(horoscope.text.strip().replace('- ', ''))
print()

# CELEBRITY PART STARTS HERE (SONJA)
print(f"But wait! There's more. Did you know these famous people are also {sign}?")    
url = f"https://www.horoscope.com/celebrities/{sign}/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
intro = soup.find('p').get_text()

names = []
h3_tags = soup.find_all('h3')
for h3 in h3_tags:
    a_tag = h3.find('a')  # Find the <a> tag within the <h3>
    names.append(a_tag.get_text())  # Get the text content of the <a> tag
     
birthdays = []
divs = soup.find_all('div', class_="module-celebrities-item-detail")
for div in divs:
    birthdays.append(div.get_text(strip=True))  

texts = []
divs = soup.find_all('div', class_='module-celebrities-item-content') 
for div in divs: # Extract text from each <div>
    text = div.get_text(strip=True)  
    text = re.sub(r'Photo:.*$', '', text).strip() # Remove the mention of "Photo by X"
    firstSign = text.find(f"{sign}") # Look for first mention of {sign} and cuts everything before that 
    if firstSign != -1: # if mention of {sign} was found 
        texts.append(text[firstSign + len(f"{sign}"):].strip()) # Removes the first mention of {sign}

print(intro)
print("")
for i in range(len(names)):
    print(f"Name: {names[i]} \nBirthday: {birthdays[i]} \n{texts[i]}")
    print("---"*50)