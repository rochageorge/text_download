NOME_DO_CANDIDATO = 'George Rocha'
EMAIL_DO_CANDIDATO = 'georgebezs@gmail.com'

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from time import sleep
from typing import Dict, List, Tuple

from jsonpath_ng import jsonpath, parse

from datetime import date

import requests

MAIN_FOLDER = Path(__file__).parent.parent


def request_journals(start_date, end_date):
    url = 'https://engine.procedebahia.com.br/publish/api/diaries'

    r = requests.post(url, data={"cod_entity": '50', "start_date": start_date,
                                 "end_date": end_date})
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 400:
        sleep(10)
        return request_journals(start_date, end_date)
    return {}


def download_jornal(edition, path):
    url = 'http://procedebahia.com.br/irece/publicacoes/Diario%20Oficial' \
          '%20-%20PREFEITURA%20MUNICIPAL%20DE%20IRECE%20-%20Ed%20{:04d}.pdf'.format(int(edition))
    r = requests.get(url, allow_redirects=True)
    if r.status_code == 200:
        with open(path, 'wb') as writer:
            writer.write(r.content)
        return edition, path
    return edition, ''


def download_mutiple_jornals(editions, paths):
    threads = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for edition, path in zip(editions, paths):
            threads.append(executor.submit(download_jornal, edition, path))

        results = []
        for task in as_completed(threads):
            results.append(task.result())

    results = [[r for r in results if r[0] == e][0] for e in editions]
    return [r[1] for r in results]


class JournalDownloader:
    def __init__(self):
        self.pdfs_folder = MAIN_FOLDER / 'pdfs'
        self.jsons_folder = MAIN_FOLDER / 'out'

        self.pdfs_folder.mkdir(exist_ok=True)
        self.jsons_folder.mkdir(exist_ok=True)
        
    # ----------------------------------------------------------------------------------------------------------------    
    def get_day_journals(self, year: int, month: int, day: int) -> List[str]:
        # TODO: get all journals of a day, returns a list of JSON paths
        
        # get today's date
        today = date.today()
        
        # convert dates to datetime format
        start_date = date(year, month, day)
        
        # end_date = start_date because the function gets the journals from a day
        end_date = start_date
        
        # assertions to make sure the dates are in the right date range
        assert today >= start_date, "Dates can't be in the future." 
        assert start_date.year >= 1970, "Dates can't be before 1970."  
        
        # request the journals in the date period
        rq = request_journals(start_date, end_date)
        
        # parse way to find the editions
        path_edition = parse("$.diaries[*].edicao")
        
        # list to append the editions
        edition = []
        
        # append each edition value found in the request
        for match in path_edition.find(rq):
            edition.append(str(match.value))
        
        # list assurance
        my_list = list(edition)
        
        # return of list with all editions from the selected period
        return my_list

    def get_month_journals(self, year: int, month: int) -> List[str]:
        # TODO: get all journals of a month, returns a list of JSON paths
        
        # count the days of the month, the quantity of days in a month can vary
        day = (date(year, month+1, 1) - date(year, month, 1)).days      
        
        # convert dates to datetime format
        start_date = date(year, month, 1)
        end_date = date(year, month, day)
        
        # get today's date
        today = date.today()
        
        # assertions to make sure the dates are in the right date range       
        assert today.month >= month, "Month can't be in the future." 
        assert start_date.year >= 1970, "Dates can't be before 1970."  
        
        # request the journals in the date period
        rq = request_journals(start_date, end_date)
        
        # parse way to find the editions
        path_edition = parse("$.diaries[*].edicao")

        # list to append the editions
        edition = []

        # append each edition value found in the request
        for match in path_edition.find(rq):
            edition.append(str(match.value))

        # list assurance
        my_list = list(edition)
        
        # return of list with all editions from the selected period
        return my_list

    def get_year_journals(self, year: int) -> List[str]:
        # TODO: get all journals of a year, returns a list of JSON paths
              
        # convert dates to datetime format
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        
        # get today's date
        today = date.today()
        
        # assertions to make sure the dates are in the right date range       
        assert today.year >= year, "Year can't be in the future." 
        assert start_date.year >= 1970, "Dates can't be before 1970."  
        
        # request the journals in the date period
        rq = request_journals(start_date, end_date)
        
        # parse way to find the editions
        path_edition = parse("$.diaries[*].edicao")

        # list to append the editions
        edition = []

        # append each edition value found in the request
        for match in path_edition.find(rq):
            edition.append(str(match.value))

        # list assurance
        my_list = list(edition)
        
        # return of list with all editions from the selected period
        return my_list

    @staticmethod
    def parse(response: Dict) -> List[Tuple[str, str]]:
            # TODO: parses the response and returns a tuple list of the date and edition

            # parse way to find the editions and dates
            path_edition = parse("$.diaries[*].edicao")
            path_data = parse("$.diaries[*].data")

            # list to append the editions and dates
            data, edition = [], []
            
            # append each date value found in the request
            for match in path_data.find(response):
                data.append(str(match.value))
            
            # append each edition value found in the request
            for match in path_edition.find(response):
                edition.append(str(match.value))    
            
            # creation of a list of tuples
            my_tuple = list(zip(data, edition))
            
            # return of list with all editions and date from the selected dictionnaire
            return my_tuple

    def download_all(self, editions: List[str]) -> List[str]:
        # TODO: download journals and return a list of PDF paths. download in `self.pdfs_folder` folder
        #  OBS: make the file names ordered. Example: '0.pdf', '1.pdf', ...
        
        # list for path appending
        path_list = []
        
        # creation of the path for each file
        for i in range(len(editions)):
            name = str(i) + '.pdf'
            save_path = self.pdfs_folder / name
            path_list.append(save_path)
        
        # calls the function provided to download the mulitple journals
        download_mutiple_jornals(editions, path_list)
        
        # returns a list with the paths
        return path_list
    
    # ----------------------------------------------------------------------------------------------------------------    
    
    def dump_json(self, pdf_path: str, edition: str, date: str) -> str:
        if pdf_path == '':
            return ''
        output_path = self.jsons_folder / f"{edition}.json"
        data = {
            'path': str(pdf_path),
            'name': str(edition),
            'date': date,
            'origin': 'Irece-BA/DOM'
        }
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data,
                                  indent=4, ensure_ascii=False))
        return str(output_path)
