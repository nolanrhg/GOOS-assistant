from bs4 import BeautifulSoup
import requests
import re # regular expressions library

#################################################
## Purpose: Find all links to annual reports   ##
##          on EDGAR for company corresponding ##
##          to ticker.                         ##
#################################################
def get_ap_links(cik):
    
    f20f_links = []

    edgar_entry_url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + cik + "&type=20-F&dateb=&owner=include&count=100"
    webpage = requests.get(edgar_entry_url).content
    soup = BeautifulSoup(webpage, 'lxml')
    links = soup.find_all('a', href = re.compile(r"Archives\S*"))

    for link in links:
        f20f_links.append("https://www.sec.gov" + link.get('href'))

    print(f20f_links)

get_ap_links("1690511")
