
import pandas as pd
from IPython.display import display, HTML
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("headless")
options.add_experimental_option("detach", True)

path = 'D:\chromedriver_win32'  # replace this with your own path to chromedriver7
browser = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

dict = {'hymn': [], 'chapter': [], 'topic': [], 'text': []}


def appendContent(link):
    browser.get(link)

    try:
        hymn = browser.find_element(By.TAG_NAME, "h3").text
        chapter = browser.find_element(By.TAG_NAME, "h4").text
    except:
        hymn = ""
        chapter = ""

    topics = browser.find_elements(By.XPATH, '//h4/span/parent::*')
    for t in topics:
        try:
            span = t.find_element(By.TAG_NAME, "span")
            topicName = span.text
        except:
            topicName = ""
            pass

        text_content = ''

        try:
            immediate_ps = t.find_elements(By.XPATH, 'following-sibling::*')
        except:
            immediate_ps = None

        if immediate_ps:
            for p in immediate_ps:

                try:
                    isSpan = p.find_element(By.TAG_NAME, "span")
                except:
                    isSpan = None

                if p.tag_name == 'p':
                    text_content += p.text + '\n'
                elif p.tag_name == 'h5':
                    text_content += p.text + '\n'
                elif p.tag_name == 'h4' and isSpan:
                    break
                elif p.tag_name == 'h4':
                    text_content += p.text + '\n'
                elif p.tag_name == 'hr':
                    break

        dict['hymn'].append(hymn)
        dict['chapter'].append(chapter)
        dict['topic'].append(topicName)
        dict['text'].append(text_content)

    try:
        link = browser.find_element(
            By.PARTIAL_LINK_TEXT, "Next").get_attribute("href")
    except:
        link = None


vedic_hymn_p1_link = 'https://www.sacred-texts.com/hin/sbe32/sbe'
vedic_hymn_p1_start = 3215
vedic_hymn_p1_end = 3263

vedic_hymn_p2_link = 'https://www.sacred-texts.com/hin/sbe46/sbe'
vedic_hymn_p2_start = 46003
vedic_hymn_p2_end = 46132

current = 2

if current == 1:
    for i in range(vedic_hymn_p1_start, vedic_hymn_p1_end+1):
        appendContent(vedic_hymn_p1_link + str(i) + '.htm')

if current == 2:
    for i in range(vedic_hymn_p2_start, vedic_hymn_p2_end+1):
        appendContent(vedic_hymn_p2_link + str(i) + '.htm')


df = pd.DataFrame(dict)
df.to_csv('vedic_hymn_part_'+str(current)+'.csv', index=False)
print('done')
browser.quit()
