from selenium import webdriver
import argparse
import time

# what character do we use to signify a black square?
BLACK_CHARACTER = '-'

# what character do we use to signify an unfilled square?
BLANK_CHARACTER = ' '

# how long should we wait for page load?
WAIT_TIME = 2

driver = webdriver.Chrome('/usr/local/bin/chromedriver')

def dfc_to_gsheet(link):
    driver.get(link)
    # wait for page to load
    time.sleep(WAIT_TIME)

    grid_element = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div[1]/div/div[2]/div/div/div/div/div[1]/div[2]/table/tbody')

    text = ''

    for row in grid_element.find_elements_by_xpath('.//tr'):
        row_text = []
        # get the text from all the td's from each row
        for td in row.find_elements_by_xpath('.//td'):
            if td.text == '':
                if len(td.find_elements_by_class_name('black')) == 0:
                    row_text.append(BLANK_CHARACTER)
                else:
                    row_text.append(BLACK_CHARACTER)
            else:
                row_text.append(letters_only(td.text))
        text += '\t'.join(row_text) + '\n'

    driver.close()
    
    return text

def letters_only(text):
    letters = ''
    for char in text:
        if char.isalpha():
            letters += char
    return letters

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Move a DownForAcross crossword puzzle to a Google Sheet')
    parser.add_argument('url', type=str, nargs=1,
                        help='the URL to the DownForAcross puzzle')
    args = parser.parse_args()
    print(dfc_to_gsheet(args.url[0]))
