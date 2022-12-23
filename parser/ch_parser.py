import csv
import re

import lxml as lxml
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

from text_analyses.cleaning import no_eng

#body - i need to connect a list into one string



class Parser():

    def __init__(self, link,soup):
        self.link = link
        self.soup = soup

    def connecter(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.link)
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        self.soup = soup

        selects = self.soup.find_all('span', class_="tr")
        for match in selects:
            match.decompose()


    def get_links(self):
        links = []
        for l in self.soup.find_all('span', class_='elementor-heading-title elementor-size-default'):
            n = l.find('a')
            x = re.search('ht(.*?)"', str(n))
            x = x.group(0)
            x = str(x)
            x = x.replace('"','')
            #links.append(n)
            if x not in links:
                links.append(x)

        return links


    def getting_text(self):

        words = ['Already', 'subscriber', 'Mark']

        body = []

        def check_all(sentence, ws):
            """Returns True if all the words are present in the sentence"""
            return all(re.search(r'\b{}\b'.format(w), sentence) for w in ws)

        for p in self.soup.find_all("div", class_="elementor-widget-container"):
            textList = p.find_all("p")
            str_to_check = str(textList)

            if any(check_all(str_to_check, word.split('+')) for word in words):
                break
            for res in textList:
                res = str(res.text)
                body.append(res)

        body = (' '.join(body).split(','))[0]
        return body

    def getting_title_eng(self):
        title = self.soup.find('h1').text
        return title

    def getting_title_ch(self):
        title = self.soup.find('h2').text
        return title

    def getting_hsk(self):
        list_hsk = []
        info = self.soup.find('ul', class_='elementor-inline-items elementor-icon-list-items elementor-post-info')
        line =str(info.text).strip()
        answer = []

        for i in line:
            try:
                x = int(i)
                answer.append(x)
            except:
                pass
        try:
            answer = answer[0]
        except:
            answer = 'None'

        return answer

    def got_all_info(self):
        body = self.getting_text()
        title_eng = self.getting_title_eng()
        title_ch = self.getting_title_ch()
        hsk_level = self.getting_hsk()

        info = {
            'title_ch': title_ch,
            'title_eng': title_eng,
            'body': body,
            'hsk_level': hsk_level,
            'link': self.link
        }
        return info



def save_csv(results):
    keys = results[0].keys()

    with open('adv.csv', 'w', encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

def page_generator(num, basic_link):
    link_list = []
    for page in range(1, num + 1):
        link = basic_link + str(page)
        link_list.append(link)
    return link_list

################################################
# PARSING HERE

beg_links = page_generator(16,'https://mandarinbean.com/category/beginner/page/')
int_links = page_generator(28,'https://mandarinbean.com/category/intermediate/page/')
ad_links = page_generator(26,'https://mandarinbean.com/category/advanced/page/')

list_of_level = [ad_links]

page_to_scr = []

for level in list_of_level:
    for i in level:
        parser_one = Parser(i, 'soup')
        parser_one.connecter()
        page_links = parser_one.get_links()
        for x in page_links:
            page_to_scr.append(x)



fin = []

for link in page_to_scr:
    parser_one = Parser(link, 'soup')
    parser_one.connecter()
    results = parser_one.got_all_info()
    fin.append(results)

save_csv(fin)







# #
#

#print(f'title is:{title_eng} or {title_ch}\nbody is {body}\nHSK level is:{hsk_level}')