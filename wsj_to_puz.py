import argparse
import re
import ssl
import subprocess
import unicodedata

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_DIRECTORY = '/Users/jennahimawan/Desktop'

# part of the Across Lite formatting
HEADING = '''<ACROSS PUZZLE>
<TITLE>
{} - WSJ Crossword Contest (NO CHECKER FUNCTIONALITY)
<AUTHOR>
{}
<COPYRIGHT>

<SIZE>
15x15
<GRID>
'''

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome('/usr/local/bin/chromedriver', options = chrome_options)

def get_crossword_html(link):
    curl = subprocess.run(['curl', link], capture_output = True, encoding = 'UTF-8')
    crossword_html = re.findall('https://www.wsj.com/puzzles/crossword/.*index.html', curl.stdout)[0]
    return crossword_html

def visit_wsj_crossword(link):
    driver.get(link)

    title = decode(driver.find_element_by_xpath('//*[@id="crossword-holder"]/div[1]/div/h1/span').text)
    authorship = driver.find_element_by_xpath('//*[@id="crossword-holder"]/div[1]/div/h2/span[1]/span').text

    # IF YOU USE WINDOWS, change the / to a \\
    filepath = '{}/{}.txt'.format(BASE_DIRECTORY, title.replace(' ', '_').replace('/', ''))
    f = open(filepath, 'w')

    f.write(HEADING.format(title, authorship.replace('By ', '')))

    grid_element = driver.find_element_by_xpath('//*[@id="ourpuzzle"]/table/tbody')
    for row in grid_element.find_elements_by_xpath('.//tr'):
        # get the text from all the td's from each row
        for td in row.find_elements_by_xpath('.//td'):
            if 'blank' in td.get_attribute('class'):
                f.write('.')
            else:
                f.write('X')
        f.write('\n')

    across_clues_element = driver.find_element_by_xpath('//*[@id="acrossholder"]/div/ul')
    down_clues_element = driver.find_element_by_xpath('//*[@id="downholder"]/div/ul')

    across_clues = parse_clue_element_text(across_clues_element.get_attribute('textContent'))
    down_clues = parse_clue_element_text(down_clues_element.get_attribute('textContent'))
    
    f.write('<ACROSS>\n')
    for clue in across_clues:
        f.write(clue + '\n')
    f.write('<DOWN>\n')
    for clue in down_clues:
        f.write(clue + '\n')
    
    answer_info = driver.find_element_by_xpath('//*[@id="crossword-holder"]/article[4]/div/p[1]').get_attribute('textContent').replace(' See the complete guide to the crossword contest here.', '')

    f.write('''<NOTEPAD>
{}
This .puz file was written by Jenna Himawan.'''.format(answer_info))

    driver.close()

    return filepath

def parse_clue_element_text(element_text):
    clues = []
    clues_and_numbers = element_text.split('\n')
    clues_and_numbers = list(filter(lambda line : not line in {'', 'A. undefined'}, clues_and_numbers))
    # get only the even lines; these are the clues
    for i in range(1, len(clues_and_numbers), 2):
        clues.append(decode(clues_and_numbers[i].strip()))
    return clues

def decode(fancy_text):
    strip_quotes = fancy_text.replace('“', '"').replace('”', '"').replace('’', "'")
    return unicodedata.normalize('NFKD', strip_quotes) \
                    .encode('ASCII', 'ignore') \
                    .decode('utf-8')

def open_across_lite(filepath):
    subprocess.run(['open', '-a', 'Across Lite', filepath])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert a WSJ crossword puzzle to a .puz file')
    parser.add_argument('url', type=str, nargs=1,
                        help='the URL to the WSJ puzzle')
    args = parser.parse_args()
    crossword_html = get_crossword_html(args.url[0])
    filepath = visit_wsj_crossword(crossword_html)
    open_across_lite(filepath)
    
