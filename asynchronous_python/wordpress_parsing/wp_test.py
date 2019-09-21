from bs4 import BeautifulSoup
import time
import requests

pars_plugins = list()


def get_html(url):
    res = requests.get(url)
    return res


def get_posts(response):
    soup = BeautifulSoup(response.text, 'lxml')
    plugins = soup.findAll('article', class_='plugin-card')
    headers = list()
    for plugin in plugins:
        h2 = plugin.find('h2').text.strip()
        headers.append(h2)
    return headers


def main():
    urls = [f'https://ru.wordpress.org/plugins/browse/blocks/page/{i}/' for i in range(1, 21)]
    for i in urls:
        pars_plugins.extend(get_posts(get_html(i)))


if __name__ == '__main__':
    t0 = time.time()
    main()
    print(time.time() - t0)
