import logging
import re
import mechanicalsoup as ms
import requests


class libra_scraper():
    def login(self, user_name: str, password:str):
        def is_extendable(element):
            return len(element.find_all('input')) > 0
        browser = ms.StatefulBrowser(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36")
        browser.set_verbose(2)
        login_page = browser.open("https://www.lib.city.kobe.jp/opac/opacs/lending_display")
        login_form = browser.select_form()
        login_form.input({'user[login]': user_name, 'user[passwd]': password, "act_login": 'ログイン'})
        list_page: ms.Browser.submit = browser.submit_selected()

        table = list_page.soup.find(class_='table_wrapper lending')                              
        rows = table.find('table').find_all('tr') 
        for row in rows[1:len(rows)]: 
            cols = row.find_all('td') 
            if len(cols)>0: 
                [_,_is_extendable,whole_book_title,due,is_extended,is_reserved,is_missing,ids,misc]=cols 
                [book_title, book_type, series, author, publisher] = re.split('\/', whole_book_title.text)
                print('|'.join([book_title,'{}'.format(is_extendable(_is_extendable)), due.text]))