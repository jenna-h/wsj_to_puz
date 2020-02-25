from selenium import webdriver
import time

PUZZLE = # PUT A LINK TO A PUZZLE HERE
BASE_DIRECTORY = # WHERE DO YOU WANT THE .txt FILE TO GO?

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

    title = driver.find_element_by_xpath('//*[@id="crossword-holder"]/div[1]/div/h1/span')
    authorship = driver.find_element_by_xpath('//*[@id="crossword-holder"]/div[1]/div/h2/span[1]/span')

    # IF YOU USE WINDOWS, change the / to a \\
    f = open('{}/{}.txt'.format(BASE_DIRECTORY, title.text.replace(' ', '_').replace('/', '')), 'w')

    f.write(HEADING.format(title.text, authorship.text))

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

def parse_clue_element_text(element_text):
    clues = []
    across_clues_and_numbers = element_text.split('\n')
    # get only the even lines; these are the clues
    for i in range(1, len(across_clues_and_numbers), 2):
        clues.append(decode(across_clues_and_numbers[i]))
    return clues

def decode(fancy_text):
    # replace smart quotes and apostrophes
    return fancy_text.replace('“', '"').replace('”', '"').replace("’", "'")

visit_wsj_crossword(PUZZLE)
