import logging as log
import os
from constants import FILES_PATH


import scrapper as sc
from gcp import upload_to_cloud, gcs_to_bq


def parse_urls(urls):
    dict_of_quotes = {}
    for item in urls:
        log.info(f'scrapping URLS: {urls.index(item) + 1}th of {len(urls)} pages, {item}')
        tag = item[32:len(item) - 6]
        dict_of_quotes[tag] = sc.parse_phrases(item)
    return dict_of_quotes


def upload_files_to_cloud():
    list_of_files = os.listdir(FILES_PATH)
    for file in list_of_files:
        log.info(f'uploading to cloud storage {file}')
        local_file_path = FILES_PATH + file
        upload_to_cloud("parser", local_file_path, file)
        gcs_to_bq(file)


def main():
    log.basicConfig(format='%(levelname)s:%(message)s', level='INFO')
    log.info('run')
    urls = sc.get_top_ten_tags()
    log.info('got list of URLS')
    # scrapping urls into dict
    dict_of_quotes = parse_urls(urls)
    # write to files
    sc.write_phrases_to_file(dict_of_quotes, 'csv')
    # upload to gcp and bigquery
    upload_files_to_cloud()
    log.info('all done')

if __name__ == '__main__':
    main()
