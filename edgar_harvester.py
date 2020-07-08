from bs4 import BeautifulSoup # for easy data extraction from HTML
import requests # for downloading webpages
import re # for regular expressions
import sys # for reading command line args

###########################
## Ticker to CIK dictionary
###########################
t2c_dict = {"GOOS" : "1690511", "UPS" : "1090727", "SNAP" : "1564408"}

#################################################
## Purpose: Find all links to annual reports   ##
##          on EDGAR for company corresponding ##
##          to ticker. If company is domestic, ##
##          the annual report is called a      ##
##          10-K; otherwise it is called a     ##
##          20-F.                              ##
#################################################
def get_ap_links(ticker, domestic = True):

    ##################################### 
    # Storage for links to annual reports
    #####################################
    ap_links = []
    
    #####################
    # Determine form type
    #####################
    form_type = "10-K" if domestic else "20-F" 
    
    #######################
    # Convert ticker to cik
    #######################
    cik = t2c_dict[ticker]
    
    ################################################
    # SEC page where annual report links are located
    ################################################
    edgar_entry_url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + cik + \
                      "&type=" + form_type + "&dateb=&owner=include&count=100"

    ##################################################
    # Use BeautifulSoup to extract annual report links
    # from HTML of SEC page
    ##################################################
    webpage = requests.get(edgar_entry_url).content
    soup = BeautifulSoup(webpage, 'lxml')
    links = soup.find_all('a', href = re.compile(r"Archives\S*"))
    
    #####################
    # store all the links
    #####################
    for link in links:
        ap_links.append("https://www.sec.gov" + link.get('href'))

    print(ap_links)
    print(len(ap_links))

##############################
# Get ticker from command line
##############################
if (len(sys.argv) < 2):
	print("\nUsage: python3 edgar_harvester.py <TICKER>\n")
	exit()

tckr = sys.argv[1]

###################
# Test the function 
###################
get_ap_links(tckr, domestic = False)
