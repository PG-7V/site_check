import lxml.html
import requests
import csv
from multiprocessing import Pool
import time
from source import file_for_read, file_output

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
        order = ['url', 'title', 'desc', 'h1', 'tel', 'mail', 'inst', 'fb',
                 'ok', 'tw', 'yot', 'vib', 'sk', 'wh', 'tg', 'vk']
        writer = csv.DictWriter(file, delimiter=';', fieldnames=order)
        writer.writerow(data)

def get_page_data(text, url):

    try:
        root_element = lxml.html.fromstring(text)
        try:
            title = over_in(str(root_element.xpath("//title/text()")))

        except:
            title = False

        try:
            desc = over_in(str(root_element.xpath("//meta[@name='description']/@content/text()")))
        except:
            desc = False

        if title and desc:
            try:
                h1 = over_in(str(root_element.xpath("//h1/text()")))
            except:
                h1 = ''

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

            try:
                inst = str(root_element.xpath("//*[contains(@href, 'instagram.com')]/@href"))
            except:
                inst = ''

            try:
                fb = str(root_element.xpath("//*[contains(@href, 'facebook.com')]/@href"))
            except:
                fb = ''

            try:
                ok = str(root_element.xpath("//*[contains(@href, 'ok.ru')]/@href"))
            except:
                ok = ''

            try:
                tw = str(root_element.xpath("//*[contains(@href, 'twitter.com')]/@href"))
            except:
                tw = ''

            try:
                yot = str(root_element.xpath("//*[contains(@href, 'youtube.com')]/@href"))
            except:
                yot = ''

            try:
                vib = str(root_element.xpath("//*[contains(@href, 'viber')]/@href"))
            except:
                vib = ''

            try:
                sk = str(root_element.xpath("//*[contains(@href, 'skype')]/@href"))
            except:
                sk = ''

            try:
                wh1 = root_element.xpath("//*[contains(@href, 'whatsapp')]/@href")
            except:
                wh1 = ''

            try:
                wh2 = root_element.xpath("//*[contains(@href, 'wa.me')]/@href")
            except:
                wh2 = ''

            wh = str(wh1) + ',' + str(wh2)

            try:
                tg1 = root_element.xpath("//*[contains(@href, 't.me')]/@href")
            except:
                tg1 = ''

            try:
                tg2 = root_element.xpath("//*[contains(@href, 'telegram.me')]/@href")
            except:
                tg2 = ''

            tg = str(tg1) + ',' + str(tg2)

            try:
                vk1 = root_element.xpath("//*[contains(@href, 'vk.me')]/@href")
            except:
                vk1 = ''
            try:
                vk2 = root_element.xpath("//*[contains(@href, 'vk.com')]/@href")
            except:
                vk2 = ''
            vk = str(vk1) + ',' + str(vk2)


            data = {
                'url': url,
                'title': title,
                'desc': desc,
                'h1': h1,
                'mail': mail,
                'tel': tel,
                'inst': inst,
                'fb': fb,
                'ok': ok,
                'tw': tw,
                'yot': yot,
                'vib': vib,
                'sk': sk,
                'wh': wh,
                'tg': tg,
                'vk': vk
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