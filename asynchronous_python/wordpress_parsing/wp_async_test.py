import time
import aiohttp
import asyncio
import lxml.html as html

pars_plugins = list()


async def get_html(url, session):
    async with session.get(url, allow_redirects=True) as response:
        response = await response.read()
        pars_plugins.extend(get_posts(response))


def get_posts(response):
    page = html.fromstring(response)
    headers = page.xpath(".//main[@id='main']//article//h2//a/text()")
    return headers


async def main():
    urls = (f'https://ru.wordpress.org/plugins/browse/blocks/page/{i}/' for i in range(1, 21))

    async with aiohttp.ClientSession() as session:
        tasks = list()
        for url in urls:
            task = asyncio.create_task(get_html(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = time.time()
    asyncio.run(main())
    print(time.time() - t0)
