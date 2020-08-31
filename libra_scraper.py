import logging
import re
import mechanicalsoup as ms
import requests
import datetime
class lending_book:
    def __init__(self, title, due_date, author, publisher, is_extendable, is_reserved, is_extended, misc):
        self.title = title
        self.due_date = due_date
        self.author = author
        self.is_extendable = is_extendable
        self.is_extended = is_extended
        self.is_reserved = is_reserved
        self.misc = misc


class libra_scraper():
    def login(self, user_name: str, password:str):
        browser = ms.StatefulBrowser(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36")
        browser.set_verbose(1)
        login_page = browser.open("https://www.lib.city.kobe.jp/opac/opacs/lending_display")
        login_form = browser.select_form()
        login_form.input({'user[login]': user_name, 'user[passwd]': password, "act_login": 'ログイン'})
        list_page: ms.Browser.submit = browser.submit_selected()
        return list_page

    def parse_list(self, list_page)->(bool, list):
        def is_extendable(element):
            return len(element.find_all('input')) > 0
        table = list_page.soup.find(class_='table_wrapper lending')
        if not table:
            return (False, [])
        rows = table.find('table').find_all('tr') 
        lending_books = []
        for row in rows[1:len(rows)]: 
            cols = row.find_all('td') 
            if len(cols)>0: 
                [_,_is_extendable,whole_book_title,due,is_extended,is_reserved,is_missing,ids,misc]=cols 
                [book_title, book_type, series, author, publisher] = re.split('\/', whole_book_title.text)
                due_date = datetime.datetime.strptime(due.text+'+0900','%Y%m%d%z')
                #print('|'.join([book_title,'{}'.format(is_extendable(_is_extendable)), datetime.datetime.strftime(due_date, '%y/%m/%d')]))
                lending_books.append(lending_book(book_title, due_date, author, publisher,is_extendable, is_reserved.text, is_extended, misc.text))
        return (True, lending_books)
