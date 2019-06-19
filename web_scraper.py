import sys
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def external_links(webpage_url):
    # get the raw html of the webpage url
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = Request(webpage_url, headers=headers)
    webpage_content = urlopen(req)

    # don't include the original url
    # urls take have this, are internal urls
    excluded_url = re.findall("//(.*?)\.", webpage_url)[0]
    end = re.findall("\.(.*?)(?:/|$)", webpage_url)[0]

    excluded_url += "." + end  # e.g. domain.com

    # print(excluded_url)

    # save links in a list
    ext_links = []

    bs = BeautifulSoup(webpage_content, features="lxml")

    # external links should start with http, https, ftp, ftps or www
    # and not include the excluded url
    for link in bs.findAll('a', attrs={'href': re.compile("^((http|ftp)s?|www)://(?!" + excluded_url + ").*$")}):
        try:
            ext_links.append(link.get('href'))
        except KeyError:
            # in case of href missing
            pass

    return ext_links


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the URL of the webpage. [Usage] -> python3 web_scraper.py webpage_url")
        sys.exit(1)

    webpage = str(sys.argv[1])
    print('Webpage is:', webpage)

    print("External links are:")
    [print(link) for link in external_links(webpage_url=webpage)]
