import lxml.html
import requests
import csv
from multiprocessing import Pool
import time
from config import file_for_read, file_output

start_time = time.time()

#оставить запросы title, mail and tel.
#Разбираюсь с отображением активности в гит и почта "62360059+PG-7V@users.noreply.github.com"


def over_in(over):
    bl = ['\n\n', '\n', '\r', '\r\n', '\t', '\r\n\t', ';']
    for i in bl:
        over = over.replace(f'{i}', '')
    return over



def get_html(url):

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
               'accept': 'text/html',
               'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

    try:
        url = 'http://' + url
        r = requests.get(url, headers=headers, timeout=0.5)
        if r.status_code == 200:
            return r.text
    except:
        return None


def writer_csv(data):
    with open(file_output, 'a') as file:
        order = ['url', 'title', 'desc', 'tel']
        writer = csv.DictWriter(file, delimiter=';', fieldnames=order)
        writer.writerow(data)

def get_page_data(text, url):

    try:
        root_element = lxml.html.fromstring(text)
        try:
            title = over_in(str(root_element.xpath("//title/text()")))
            # TODO: only title, description, mail and phone
        except:
            title = False

        try:
            desc = over_in(str(root_element.xpath("//meta[@name='description']/@content/text()")))
        except:
            desc = False

        if title and desc:

            try:
                mail1 = root_element.xpath("//a[contains(@href, '@')]/@href")
            except:
                mail1 = ''

            try:
                mail2 = root_element.xpath("//*[contains(@href, 'mailto:')]/@href")
            except:
                mail2 = ''
            mail = str(mail1) + ',' + str(mail2)
            mail = mail.replace('mailto:', '')

            try:
                tel = str(root_element.xpath("//*[contains(@href, 'tel:')]/@href")).replace('tel:', '')
            except:
                tel = ''




            data = {
                'url': url,
                'title': title,
                'desc': desc,
                'mail': mail,
                'tel': tel,
                }
            writer_csv(data)

    except:
        return None


def make_all(url):
    text = get_html(url)
    if text:
        get_page_data(text, url)


def main():
    fds = open(file_for_read, 'r', encoding='utf-8')

    urls = []
    for line in fds:
        urls.append(line.strip())
    fds.close()

    with Pool(20) as p:
        p.map(make_all, urls)


if __name__ == '__main__':
    main()
    print("--- %s seconds ---" % (time.time() - start_time))