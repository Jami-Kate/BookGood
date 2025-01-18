#import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the website we want to scrape
url = "https://www.timeanddate.com/astronomy/finland/helsinki"

# Use the requests library to fetch the content of the webpage
# This sends an HTTP GET request to the specified URL and stores the response
response = requests.get(url)

# Parse the content of the webpage using BeautifulSoup
# The response.content contains the raw HTML of the page
# We pass it to BeautifulSoup, specifying the HTML parser to process it
soup = BeautifulSoup(response.content, 'html.parser')

soup = soup.find('tbody').find_parent() # Keeps everything from the first <h2> onward
timeHeaders = soup.find_all('th')  


#I need to split the times but only the ones that include time and direction, aka not the first nor last
i = 1

finalTimes = []
finalTimes.append({
        'title': timeHeaders[0].text.strip(),
        'time': timeHeaders[0].find_next('td').text.strip(),
        'direction': 'n/a',
    })


while i < 5:
    time = timeHeaders[i]
    title = time.text.strip()
    timeAndDirTag = time.find_next('td')  # This assumes categories are grouped
    timeAndDir = timeAndDirTag.text.strip() if timeAndDirTag else "NG"
    timeExact, dirWords = timeAndDir.split('↑ ')
    finalTimes.append({
        'title': title,
        'time': timeExact,
        'direction': dirWords,
    })
    i = i + 1

finalTimes.append({
        'title': timeHeaders[5].text.strip(),
        'time': timeHeaders[5].find_next('td').text.strip(),
        'direction': 'n/a',
    })

# Create a DataFrame for better visualization
times_df = pd.DataFrame(finalTimes)

# Display the DataFrame
print("Sun and Moon times in Helsinki, Finland today:")
times_df.head()
