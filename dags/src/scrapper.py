import os
import requests
from bs4 import BeautifulSoup
import logging as log
import json
import csv

from constants import FILES_PATH


def get_top_ten_tags() -> list:
    log.info('start parsing')
    """func returns urls with top ten tags to parse"""
    url = 'https://quotes.toscrape.com'
    res = requests.get(url)
    sp = BeautifulSoup(res.text, 'lxml')
    top_ten_tags = sp.find('h2', string="Top Ten tags").findParent()
    hrefs = top_ten_tags.findAll('a', class_='tag')
    urls_list = [url + str(i.get('href')) + 'page/' for i in hrefs]
    log.info(f'list created {len(urls_list)},details: {urls_list}')
    return urls_list


def parse_phrases(url: str) -> list:
    """func to parse phrases and authors from url into list"""
    list_of_quotes = []
    page = 1
    while True:
        res = requests.get(url + str(page))
        sp = BeautifulSoup(res.text, 'lxml')
        if 'No quotes found!' in str(sp.contents):
            return list_of_quotes
        else:
            phrases = sp.findAll('span', class_='text')
            authors = sp.findAll('small', class_='author')
            for counter, phrase in enumerate(phrases):
                list_of_quotes.append(
                    {"qoute": str(phrase.text).replace("“", "").replace("”", ""), "author": authors[counter].text})
            page += 1


def write_phrases_to_file(dict_of_quotes: dict, fformat: str = 'json'):
    """function collect phrases to files named like dict keys"""
    os.makedirs(FILES_PATH, exist_ok=True)
    for key in dict_of_quotes.keys():
        log.info(f'writing {key} qoutes')
        file = f'{FILES_PATH}{key}_quotes_of_great_men.{fformat}'
        with open(file, 'w') as f:
            if fformat == 'json':
                json.dump(dict_of_quotes[key], f, indent=4)
            elif fformat == 'txt': #TODO fix dict keys in string
                    for value in dict_of_quotes[key]:
                        f.write(f'{value} \n')
            elif fformat == 'csv':
                    writer = csv.writer(f)
                    writer.writerow(['tag', 'author', 'quote'])
                    for items in dict_of_quotes[key]:
                        list_of_qoutes = items
                        writer.writerow([key, list_of_qoutes["author"], list_of_qoutes["qoute"]])


if __name__ == '__main__':
    pass
    # with open('tmp/tmp.json', 'r') as f:
    #     dict_of_quotes = json.load(f)
    #     write_phrases_to_file(dict_of_quotes, 'json')
