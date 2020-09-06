import datetime
import requests
from typing import List
import libra_scraper
import json
import locale

Books = List[libra_scraper.lending_book]
class slack_notifier:
    def __init__(self, url:str, books: Books)->str:
        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
        self.json = dict()
        self.url = url
        blocks = list()
        blocks.append( { 
            'type': 'section', 
            'text': {
                'type': 'mrkdwn', 
                'text' : "*返却期限が近づいている資料があります*"
            }
        })
        blocks.append({'type': 'divider'})
        for book in books:
            is_reserved = '' if book.is_reserved ==  'なし' else '予約あり'
            is_extended = book.misc
            JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
            now = datetime.datetime.now(JST)
            if now > book.due_date:
                book_title = '*{}*'.format(book.title)
            else:
                book_title = book.title
            due = datetime.datetime.strftime(book.due_date, '%Y/%m/%d (%a)')
            blocks.append({
                'type': 'section',
                'text':{
                    'type' :  'mrkdwn',
                    'text': "{0} {1} {2} {3}".format(book_title, due, is_reserved, book.misc)
                }
            })
        blocks.append({'type': 'divider'})            
        self.json['blocks'] = blocks
        self.json['text'] = '*返却期限が近づいている資料があります*'
        
    def notify(self):

        json_data = json.dumps(self.json)
        result = requests.post(self.url, json_data, headers={'Content-Type': 'application/json'})
    
    def message(self, message):
        json_data = dict()
        blocks = list()
        blocks.append( { 
            'type': 'section', 
            'text': {
                'type': 'mrkdwn', 
                'text' : message
            }})
        json_data['text'] = message
        json_data['blocks'] = blocks
        result = requests.post(self.url, json.dumps(json_data), headers={'Content-Type': 'application/json'})