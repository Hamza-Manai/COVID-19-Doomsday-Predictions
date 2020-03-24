import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import json
import re
import ast


class GraphsDataScrapper:
    TARGET_DOMAIN = "https://www.worldometers.info/coronavirus/"

    def get_data( self, path, case_type):
        url = GraphsDataScrapper.TARGET_DOMAIN + path
        req = requests.get(url)
        content = req.content.decode("utf-8")
        data_regex = r"data: \[[0-9,\,]*\]"
        data_matches = re.finditer(data_regex, content)

        if case_type == 0: 
            for match in data_matches:
                match_data = match.group().replace("data: ", "")
                return ast.literal_eval(match_data);
        elif case_type == 1:
            data_matches = list(data_matches)
            data_matches = data_matches[4:]
            for match in data_matches:
                match_data = match.group().replace("data: ", "")
                return ast.literal_eval(match_data);
        elif case_type == 2: 
            data_matches = list(data_matches)
            data_matches = data_matches[5:]
            for match in data_matches:
                match_data = match.group().replace("data: ", "")
                return ast.literal_eval(match_data);
        elif case_type == 3: 
            data_matches = list(data_matches)
            data_matches = data_matches[8:]
            for match in data_matches:
                match_data = match.group().replace("data: ", "")
                return ast.literal_eval(match_data);
        else: 
            return [];     
        
        return []





"""


def get_data( path = "coronavirus-cases"):
    url = GraphsDataGrabber.TARGET_DOMAIN + path
    req = requests.get(url)
    content = req.content.decode("utf-8") 

    data_regex = r"data: \[[0-9,\,]*\]"
    data_matches = re.finditer(data_regex, content)
    data_matches = list(data_matches)
    data_matches = data_matches[2:]
    for match in data_matches:
        match_data = match.group().replace("data: ", "")
        return ast.literal_eval(match_data)

    return []
print(get_data( path = "coronavirus-cases"))

"""