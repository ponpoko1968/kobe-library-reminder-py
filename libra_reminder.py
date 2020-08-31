import os
import logging
import http.client
import libra_scraper
from datetime import datetime, timedelta, timezone
from slack_notifier import slack_notifier

logging.basicConfig(level=logging.WARNING)

def httpclient_logging_patch(level=logging.WARNING):
    """Enable HTTPConnection debug logging to the logging framework"""

    def httpclient_log(*args):
        httpclient_logger.log(level, " ".join(args))

    # mask the print() built-in in the http.client module to use
    # logging instead
    http.client.print = httpclient_log
    # enable debugging
    http.client.HTTPConnection.debuglevel = 0

httpclient_logger = logging.getLogger("http.client")

def main():
    httpclient_logging_patch()
    logging.getLogger().setLevel(logging.WARNING)
    httpclient_logger.setLevel(logging.WARNING)
    httpclient_logger.propagate = True
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = True
    l = libra_scraper.libra_scraper()
    (user, passwd, url) =  (os.getenv('LIBRA_REMINDER_USER'), os.getenv('LIBRA_REMINDER_PASSWD'), os.getenv('LIBRA_REMINDER_SLACK_URL'))
    page = l.login(user, passwd)
    (result, book_list) = l.parse_list(page)
    notifier = slack_notifier(url, book_list)
    if not result:
        notifier.message("*ページの取得に失敗しました*")
        return
    if len(book_list) == 0:
        notifier.message("貸し出し中の本はありません")
        return
    JST = timezone(timedelta(hours=+9), 'JST')
    delta = book_list[0].due_date - datetime.now(JST)
    if delta.days <= 4:
        notifier.notify()
    else:
        notifier.message("貸し出し期限が近づいている本はありません")

def lambda_handler(event, context):
    main()
    return 0


if __name__ == "__main__":
    main()
