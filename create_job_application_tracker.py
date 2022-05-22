# SETUP

import json
import requests
import csv
from bs4 import BeautifulSoup

SEARCH_URL_TEMPLATE = 'https://www.glassdoor.com/Search/results.htm?keyword='

# HELPER FUNCTIONS

def buildSearchURL(company_name):
    s = ''
    for c in company_name:
        if c.isalnum():
            s += c
        elif c == ' ':
            s += '%20'
        elif c == '&':
            s += '%26'
        else:
            s += c
    search_url = SEARCH_URL_TEMPLATE + s
    return search_url

def scrapeSearchPage(search_url):
    html_text = requests.get(search_url).text
    soup = BeautifulSoup(html_text, 'lxml')
    companies = []
    for a in soup.findAll('a', {'class': 'company-tile d-flex flex-column flex-sm-row align-items-start p-std mb-sm-std css-poeuz4 css-1wh1oc8'}):
        # create dictionary
        company = {}
        # name
        name = a.h3.text
        company['name'] = name
        # industry
        div = a.find('div', {'class': 'd-flex flex-column flex-sm-row align-items-sm-center css-56kyx5'})
        span = div.find('span')
        span.extract()
        industry = span.text
        company['industry'] = industry
        # size
        size = div.text[:-10]
        company['size'] = size
        # hq
        div = a.findAll('div', {'class': 'css-56kyx5'})
        hq = div[1].text[18:]
        company['hq'] = hq
        # rating
        if a.strong:
            rating = a.strong.text[:3]
        else:
            rating = ''
        company['rating'] = rating
        # path
        company['path'] = a['href']
        # add company to companies
        companies.append(company)
    return companies

def getCompany(companies, path):
    for company in companies:
        if company['path'] == path:
            return company
    return None

def parsePath(input_url):
    if input_url.find('/Overview/') != -1:
        return input_url[25:]
    else:
        return ''

def parseName(input_url):
    if input_url.find('/Overview/') != -1:
        return input_url[46:input_url.find('-EI_')]
    else:
        return ''

def loadVariables(vars_file):
    with open(vars_file) as json_file:
        vars = json.load(json_file)
        return vars

def loadDatabase(data_file):
    with open(data_file) as json_file:
        data = json.load(json_file)
        return data

# MAIN FUNCTION

def createTracker(vars_file):
    vars = loadVariables(vars_file)
    input_file = vars["INPUT_FILE"]
    output_file = vars["OUTPUT_FILE"]
    error_file = vars["ERROR_FILE"]
    data_file = vars["DATA_FILE"]
    retries = vars["RETRIES"]
    update = vars["UPDATE"]
    data = loadDatabase(data_file)
    if update:
        print('CREATING TRACKER FROM EXISTING TRACKER')
    else:
        print('CREATING TRACKER FROM LIST OF URLS')
    with open(input_file, encoding='utf-8') as input_file:
        with open(output_file, 'w', newline='', encoding='utf-8') as output_file:
            with open(error_file, 'w', newline='', encoding='utf-8') as error_file:
                csv_reader = csv.reader(input_file, delimiter=',')
                csv_writer = csv.writer(output_file)
                csv_writer_error = csv.writer(error_file)
                csv_writer.writerow(['Tier', 'Company', 'Industry', 'Size', 'Location', 'Rating', 'Glassdoor', 'Position', 'Jobs', 'Status', 'Notes'])
                csv_writer_error.writerow(['Line', 'Company URL'])
                line = 1
                # iterate over all rows
                for input_row in csv_reader:
                    # skip header
                    if line == 1:
                        line += 1
                        continue
                    # skip empty rows
                    if not input_row:
                        line += 1
                        continue
                    # if updating, copy the input row as a template
                    if update:
                        output_row = input_row
                    else:
                        output_row = [''] * 7
                    # if updating, copy the url from the correct column
                    if update:
                        input_url = input_row[6]
                    else:
                        input_url = input_row[0]
                    print(line,'\t', input_url)
                    path = parsePath(input_url)
                    # if the company path is found in the database, copy the info to the output file
                    if path in data:
                        info = data[path]
                        output_row = [''] + info + ['https://www.glassdoor.com' + path]
                        print('DATABASE')
                    # otherwise search the company on glassdoor
                    else:
                        name = parseName(input_url)
                        search_url = buildSearchURL(name)
                        success = False
                        for attempt in range(retries + 1):
                            companies = scrapeSearchPage(search_url)
                            company = getCompany(companies, path)
                            # if the company is found on glassdoor, copy the info to the output file
                            if company:
                                success = True
                                name = company['name']
                                industry = company['industry']
                                size = company['size']
                                hq = company['hq']
                                rating = company['rating']
                                output_row[1] = name
                                output_row[2] = industry
                                output_row[3] = size
                                output_row[4] = hq
                                output_row[5] = rating
                                output_row[6] = input_url
                                break
                        if success:
                            print('SUCCESS')
                        else:
                            csv_writer_error.writerow([line, input_url])
                            print('FAIL')
                    csv_writer.writerow(output_row)
                    line += 1
    print('COMPLETE')

# SELECT WHICH FILE TO USE FOR THE INPUT VARIABLES
# (MODIFY THIS)

createTracker("my_files/variables_update.json")