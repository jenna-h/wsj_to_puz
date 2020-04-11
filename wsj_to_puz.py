from selenium import webdriver
import time
import subprocess
import argparse
import unicodedata

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

driver = webdriver.Chrome('/usr/local/bin/chromedriver')

def visit_wsj_crossword(link):
    driver.get(link)

    title = driver.find_element_by_xpath('//*[@id="crossword-holder"]/div[1]/div/h1/span').text
    authorship = driver.find_element_by_xpath('//*[@id="crossword-holder"]/div[1]/div/h2/span[1]/span').text

    # IF YOU USE WINDOWS, change the / to a \\
    filepath = '{}/{}.txt'.format(BASE_DIRECTORY, title.replace(' ', '_').replace('/', ''))
    f = open(filepath, 'w')

    f.write(HEADING.format(title, authorship))

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

    across_clues = parse_clue_element_text(across_clues_element.text)
    down_clues = parse_clue_element_text(down_clues_element.text)

    f.write('<ACROSS>\n')
    for clue in across_clues:
        f.write(clue + '\n')
    f.write('<DOWN>\n')
    for clue in down_clues:
        f.write(clue + '\n')

    f.write('''<NOTEPAD>
This .puz file was written by Jenna Himawan.''')

    driver.close()

    return filepath

def parse_clue_element_text(element_text):
    clues = []
    across_clues_and_numbers = element_text.split('\n')
    # get only the even lines; these are the clues
    for i in range(1, len(across_clues_and_numbers), 2):
        clues.append(decode(across_clues_and_numbers[i]))
    return clues

def decode(fancy_text):
    strip_accents = unicodedata.normalize('NFKD', fancy_text) \
                    .encode('ASCII', 'ignore') \
                    .decode('utf-8')
    return strip_accents.replace('“', '"').replace('”', '"')

def open_across_lite(filepath):
    subprocess.run(['open', '-a', 'Across Lite', filepath])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert a WSJ crossword puzzle to a .puz file')
    parser.add_argument('url', type=str, nargs=1,
                        help='the URL to the WSJ puzzle')
    args = parser.parse_args()
    filepath = visit_wsj_crossword(args.url[0])
    open_across_lite(filepath)
    
