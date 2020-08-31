import os
import logging
import http.client
import libra_scraper
from slack_notifier import slack_notifier

logging.basicConfig(level=logging.DEBUG)

def httpclient_logging_patch(level=logging.DEBUG):
    """Enable HTTPConnection debug logging to the logging framework"""

    def httpclient_log(*args):
        httpclient_logger.log(level, " ".join(args))

    # mask the print() built-in in the http.client module to use
    # logging instead
    http.client.print = httpclient_log
    # enable debugging
    http.client.HTTPConnection.debuglevel = 1

httpclient_logger = logging.getLogger("http.client")    

def main():
    httpclient_logging_patch()
    logging.getLogger().setLevel(logging.DEBUG)
    httpclient_logger.setLevel(logging.DEBUG)
    httpclient_logger.propagate = True
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    l = libra_scraper.libra_scraper()
    page = l.login(os.getenv('LIBRA_REMINDER_USER'),os.getenv('LIBRA_REMINDER_PASSWD'))
    (result, book_list) = l.parse_list(page)
    if result:
        notifier = slack_notifier(book_list)
        notifier.notify(os.getenv('LIBRA_REMINDER_SLACK_URL'))

if __name__ == "__main__":
    main()