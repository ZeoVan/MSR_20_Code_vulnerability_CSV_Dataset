#coding=utf8
import sys
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import datetime
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Global Variables

vulnCount = 0;

codeLinkCount = 0;
data_log = open("CVE-Scraper_all.dat", "w+") # volatile extra data storage [JSON]

# Error log writer
error_log = open("./Logs/main_log_all.log", "a+")


def log_data(CVEID, CVEPage, CWEID, knownExploits, vulnClassification,
             publishDate, updateDate, score, accessGained, attackOrigin,
             complexity, authenticationRequired, confidentiality, integrity,
             availability,summary,codeLink):
    global vulnCount
    print("Logging cell data...")
    vulnCount = vulnCount + 1
    print("VULNERABILITIES FOUND: " + str(vulnCount))
    data_log.write('{\n\t"CVE ID":\"' + CVEID + '\",\n\t"CVE Page":\"' +
                   CVEPage + '\",\n\t"CWE ID":\"' + CWEID +
                   '\",\n\t"Known Exploits":\"' + knownExploits +
                   '\",\n\t"Vulnerability Classification":\"' +
                   vulnClassification + '\",\n\t"Publish Date":\"' + publishDate
                   + '\",\n\t"Update Date":\"' + updateDate +
                   '\",\n\t"Score":\"' + score + '\",\n\t"Access Gained":\"' +
                   accessGained + '\",\n\t"Attack Origin":\"' + attackOrigin +
                   '\",\n\t"Complexity":\"' + complexity +
                   '\",\n\t"Authentication Required":\"' +
                   authenticationRequired + '\",\n\t"Confidentiality":\"' +
                   confidentiality + '\",\n\t"Integrity":\"' + integrity +
                   '\",\n\t"Availability":\"' + availability +
                   '\",\n\t"Summmary":\"' + summary +
                   '\",\n\t"codeLink":\"' + codeLink + '\"\n}\n\n')

    print('{\n\t"CVE ID":\"' + CVEID + '\",\n\t"CVE Page":\"' +
          CVEPage + '\",\n\t"CWE ID":\"' + CWEID +
          '\",\n\t"Known Exploits":\"' + knownExploits +
          '\",\n\t"Vulnerability Classification":\"' +
           vulnClassification + '\",\n\t"Publish Date":\"' + publishDate
           + '\",\n\t"Update Date":\"' + updateDate +
           '\",\n\t"Score":\"' + score + '\",\n\t"Access Gained":\"' +
           accessGained + '\",\n\t"Attack Origin":\"' + attackOrigin +
           '\",\n\t"Complexity":\"' + complexity +
           '\",\n\t"Authentication Required":\"' +
           authenticationRequired + '\",\n\t"Confidentiality":\"' +
           confidentiality + '\",\n\t"Integrity":\"' + integrity +
           '\",\n\t"Availability":\"' + availability + '\"\n}\n\n')

def find_code_link(CVEPage):
    # each cve example on each page
    global codeLinkCount
    try:
        cveSoup = BeautifulSoup(urlopen(Request(CVEPage, headers={'User-Agent': 'Mozilla/5.0'})).read(), 'html.parser')
        linkStr = ""
        referTable = cveSoup.find('table', {'id': 'vulnrefstable'}, class_='listtable')
        row = referTable.findAll('td', class_="r_average")
        for cell in row:
            link = cell.find('a')['href']

            #for chrome
            #if "stable-channel-update" in link and "chrome" in link:

            #for android
            #if "android.googlesource.com" in link:

            if "github.com" in link and "commit" in link:
                codeLinkCount += 1
                linkStr += cell.find('a')['href']
                print("codeLinkCount:" + str(codeLinkCount))
        return linkStr
    except:
        return ""



# Log errors to the file specified by error_log
def log_message(msg):
    timestamp = str(datetime.datetime.now())
    error_log.write(timestamp + ":\t" + msg + "\n")

# Does the heavy lifting of breaking down the CVE tables
def record_cve_data(pageURL):
    log_message("scrape extracting from: " + pageURL + "\n")
    pageSoup = BeautifulSoup(urlopen(Request(pageURL,
                             headers={'User-Agent': 'Mozilla/5.0'})).read(),
                             'html.parser')

    pageTable = pageSoup.find('table', class_ = "searchresults sortable")
    for row, summarys in zip(pageTable.findAll('tr', class_ = "srrowns"), pageTable.findAll('td', class_ = "cvesummarylong")):
        print(row)

        # Temp variables to hold data that will be stored.
        CVEID = "NULL"
        CVEPage = "NULL"
        CWEID = "NULL"
        knownExploits = "NULL"
        vulnClassification = "NULL"
        publishDate = "NULL"
        updateDate = "NULL"
        score = "NULL"
        accessGained = "NULL"
        attackOrigin = "NULL"
        complexity = "NULL"
        authenticationRequired = "NULL"
        confidentiality = "NULL"
        integrity = "NULL"
        availability = "NULL"
        summary = "NULL"

        index = 0
        for cell in row.findAll('td'):
            print("<" + str(cell.next) + ">")
            # Push scraped cell data into organized variables
            if(index == 1):
                CVEPage = ("https://www.cvedetails.com" +
                          (cell.find('a'))['href'])
                CVEID = cell.find('a').next
            if(index == 2):
                try:
                    CWEID = "CWE-"+str(cell.find('a').next).strip("\r\n\t")
                except:
                    CWEID = str(cell.next).strip("\r\n\t")
            if(index == 3):
                knownExploits = str(cell.next).strip("\r\n\t")
            if(index == 4):
                vulnClassification = str(cell.next).strip("\r\n\t")
            if(index == 5):
                publishDate = str(cell.next).strip("\r\n\t")
            if(index == 6):
                updateDate = str(cell.next).strip("\r\n\t")
            if(index == 7):
                score = cell.find('div').next
            if(index == 8):
                accessGained = str(cell.next).strip("\r\n\t")
            if(index == 9):
                attackOrigin = str(cell.next).strip("\r\n\t")
            if(index == 10):
                complexity = str(cell.next).strip("\r\n\t")
            if(index == 11):
                authenticationRequired = str(cell.next).strip("\r\n\t")
            if(index == 12):
                confidentiality = str(cell.next).strip("\r\n\t")
            if(index == 13):
                integrity = str(cell.next).strip("\r\n\t")
            if(index == 14):
                availability = str(cell.next).strip("\r\n\t")

            print("---")
            index += 1
        summary = str(summarys.next).strip("\r\n\t")
        # List all values gained from this row
        print("\n\n")
        print("===")
        print("CVE ID:\t\t\t\t" + CVEID)
        print("CVE Page:\t\t\t" + CVEPage)
        print("CWE ID:\t\t\t\t" + CWEID)
        print("Number of Exploits:\t\t\t" + knownExploits)
        print("Vulnerability Classification:\t" + vulnClassification)
        print("Publish Date:\t\t\t" + publishDate)
        print("Update Date:\t\t\t" + updateDate)
        print("CVSS Score:\t\t\t" + score)
        print("Access Gained:\t\t\t" + accessGained)
        print("Attack Origin:\t\t\t" + attackOrigin)
        print("Complexity:\t\t\t" + complexity)
        print("Authentication Required:\t" + authenticationRequired)
        print("Confidentiality:\t\t" + confidentiality)
        print("Integrity:\t\t\t" + integrity)
        print("Availability:\t\t\t" + availability)
        print("Summary:\t\t\t" + summary)
        print("===\n\n")

        codeLink = find_code_link(CVEPage)

        log_data(CVEID, CVEPage, CWEID, knownExploits, vulnClassification,
            publishDate, updateDate, score, accessGained, attackOrigin,
            complexity, authenticationRequired, confidentiality, integrity,
            availability,summary,codeLink)


def scrape_cve_data():
    # grab the CVE Details page and throw it in beautifulSoup.

    #For android
    #pageURL = "https://www.cvedetails.com/product/19997/Google-Android.html?vendor_id=1224"

    # For chrome
    # pageURL = "https://www.cvedetails.com/product/15031/Google-Chrome.html?vendor_id=1224"

    pageURL = "https://www.cvedetails.com/browse-by-date.php"
    log_message("Scrape starting up... root page: " + pageURL)
    catalogSoup=BeautifulSoup(urlopen(Request(pageURL,
                              headers={'User-Agent': 'Mozilla/5.0'})).read(),
                              'html.parser')

    # Scrape the browse-by-date page to gather all of the different month's links
    catalogTable = catalogSoup.find('table', class_='stats')
    yearlyReports = []
    for row in catalogTable.findAll('th'):
        for year in row.findAll('a', href=True):
            print("Found year at: https://www.cvedetails.com" + year['href'] + "\n")
            yearlyReports.append("https://www.cvedetails.com" + year['href'])

    print("\n === Years discovered. Grabbing pages for each year ===\n\n")

    # discover the pages for each year and pass on those pages to be dissected
    for yearURL in yearlyReports:
        yearTableSoup = BeautifulSoup(urlopen(Request(yearURL,
                                      headers={'User-Agent': 'Mozilla/5.0'}))\
                                      .read(), 'html.parser')

        pageIndex = yearTableSoup.find('div', {'id':'pagingb'}, class_='paging')
        for page in pageIndex.findAll('a', href=True):
            pageURL = ("https://www.cvedetails.com" + page['href'])
            record_cve_data(pageURL)


###############################################################################
# MAIN
###############################################################################
def main(argv):
    print("\n==== CVE-Scraper ====")
    print("==== Main.py ====\n")
    print("PYTHON VERSION:\t\t" + sys.version)
    log_message("CVE-Scraper Starting up...")

    scrape_cve_data()
    log_message("Scrape complete")

if __name__ == '__main__':
    main(sys.argv[1:])