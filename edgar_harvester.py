import regex_lookup_values as rlv
from bs4 import BeautifulSoup # for easy data extraction from HTML
import requests # for downloading webpages
import re # for regular expressions
import sys # for reading command line args

'''
|||||||||||||||
|| FUNCTIONS ||
|||||||||||||||
'''

#################################################
##                                             ##
## Purpose: Find all links to annual reports   ##
##          on EDGAR for company corresponding ##
##          to ticker. If company is domestic, ##
##          the annual report is called a      ##
##          10-K; otherwise it is called a     ##
##          20-F.                              ##
##                                             ##
#################################################
def get_ar_links(ticker, domestic = True):

    #------------------------------------
    # Storage for links to annual reports
    #------------------------------------
    ar_links = []
    
    #--------------------
    # Determine form type
    #--------------------
    form_type = "10-K" if domestic else "20-F" 
    
    #-----------------------------------------------
    # SEC page where annual report links are located
    #-----------------------------------------------
    edgar_entry_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + ticker + \
                      "&type=" + form_type + "&dateb=&owner=include&count=100"

    #-------------------------------------------------
    # Use BeautifulSoup to extract annual report links
    # from HTML of SEC page
    #-------------------------------------------------
    webpage = requests.get(edgar_entry_url).content
    soup = BeautifulSoup(webpage, 'lxml')
    links = soup.find_all('a', href = re.compile(r"Archives\S*"))
    
    #--------------------
    # Store all the links
    #--------------------
    for link in links:
        url = "https://www.sec.gov" + link.get('href')
        webpage = requests.get(url).content
        soup = BeautifulSoup(webpage, 'lxml')
        link = soup.find('a', href = re.compile(r"" + rlv.GOOS_20F))
        ar_links.append("https://www.sec.gov" + link.get('href'))
    
    return ar_links


######################################################
##                                                  ##
## Purpose: Extract net income data point from each ##
##          annual report.                          ##
##                                                  ##
######################################################
def get_net_income_data(ar_links):

    net_income_regex = re.compile(r"\s*Net (income|loss)+\s*")

    for link in ar_links:
        form = requests.get(link).text
        for line in form.split("\n"):
            if re.match(net_income_regex, line):
                    print(line)

#-----------------------------
# Get ticker from command line
#-----------------------------
if (len(sys.argv) < 3):
    print("INSUFFICIENT ARGUMENTS\nUsage: python3 edgar_harvester.py <TICKER> foreign/domestic")
    exit()
elif (sys.argv[2] != "foreign" and sys.argv[2] != "domestic"):
    print("IS " + sys.argv[1] + " FOREIGN OR DOMESTIC?\nUsage: python3 edgar_harvester.py <TICKER> foreign/domestic")
    exit()

tckr = sys.argv[1]
#------------------
# Test the function 
#------------------
ar_links = get_ar_links(tckr, domestic = (sys.argv[2] == "domestic"))
print(ar_links)
