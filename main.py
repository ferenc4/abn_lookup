from builtins import Exception, input, str

import requests
# https://3583bytesready.net/2016/08/17/scraping-data-python-xpath/
from lxml import html
import re


# //*[@id="content-matching"]/div/div/table/tbody/tr[1]
# //*[@id="content-matching"]/div/div/table/tbody/tr[1]/th[1]
# //*[@id="content-matching"]/div/div/table/tbody/tr[2]/td[1]/a

# &#10;&#13;                                Matching names&#10;&#13;
def main():
    should_continue = True
    while should_continue:
        company_name = input("Enter the company name: ")
        response = requests.get("https://abr.business.gov.au/Search/ResultsActive?SearchText=" + company_name +
                                "&AllNames=False&EntityName=False&BusinessName=False&TradingName=False&NarrowSearch=False&SearchType=ActiveAbns&AllStates=True&ACT=False&NSW=False&NT=False&QLD=False&TAS=False&SA=False&VIC=False&WA=False&PostcodeDisplayName=Postcode%20(required%20for%20DGR%20%26%20Charity%20search%20options%20if%20Name%20is%20blank)%3A&HideBreadcrumbs=False&HideSearchBox=False&HideLeftSideBar=False&ShowHelp=False&IsHomePage=False&NoIndex=False&ShowVersionNumber=False")
        status = response.status_code
        expected_status = 200
        if status != expected_status:
            raise Exception("Expected status code to be " + expected_status + ", but it was " + status)
        tree = html.fromstring(response.content)
        col = 0
        row = 0
        bsb = ""
        company_ary = []
        for cell in tree.xpath('//*[@id="content-matching"]/div/div/table/tbody/tr/td'):
            if col == 0:
                bsb = cell.getchildren()[0].text_content().strip()
            elif col == 1 or col == 2 or col == 3:
                company_ary.append(re.sub("\\s+", " ", cell.text_content().strip()))
            if col == 3:
                print(bsb + " | " + ", ".join(str(x) for x in company_ary))
                bsb = ""
                company_ary = []
            col = (col + 1) % 4
            row += 1
        exit_input = input("Enter 'e' to exit, or any other key to continue: ")
        should_continue = exit_input == 'q'


if __name__ == "__main__":
    main()
