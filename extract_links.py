from bs4 import BeautifulSoup, SoupStrainer
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import unquote, urlparse


class ExtractLinks():

    def __init__(self, config):
        self.base_url = config['base_url']
        if self.base_url[-1] != '/':
            self.base_url += '/'
        self.auth = False
        if(config['http_user'] and config['http_pass']):
            self.auth = HTTPBasicAuth(config['http_user'], config['http_pass'])
        if config['ssl_verify'] == False or config['ssl_verify'].lower() == 'false':
            self.ssl_verify = False
        else:
            self.ssl_verify = True

    def get_raw_page(self, url):
        if(self.auth):
            response = requests.get(
                url, auth=self.auth, verify=self.ssl_verify)
        else:
            response = requests.get(url, verify=self.ssl_verify)
        page_content = str(BeautifulSoup(response.content, "html.parser"))
        return page_content

    def get_all_relative_links(self, page_content):
        link_elements = BeautifulSoup(
            page_content, "html.parser", parse_only=SoupStrainer('a'))
        links = map(lambda link: unquote(link['href']),
                    filter(lambda link: link.has_attr('href'), link_elements))
        links = filter(lambda link: not link.endswith('../'), links)
        return tuple(links)

    def get_main_dir_urls(self):
        raw_page = self.get_raw_page(self.base_url)
        all_links = self.get_all_relative_links(raw_page)
        # dir_links = filter(lambda link: link.endswith('/'), all_links)
        output = list()
        for dir_path in all_links:
            output.append(dir_path)
        return output

    def get_recursive_links(self, relative_path=''):
        if relative_path != '' and relative_path[-1] != '/':
            return [relative_path]
        links = list()
        raw_page = self.get_raw_page(self.base_url + relative_path)
        all_relative_links = self.get_all_relative_links(raw_page)
        dir_links = filter(lambda link: link[-1] == '/', all_relative_links)
        file_links_relative = list(
            filter(lambda link: link[-1] != '/', all_relative_links))
        for link in file_links_relative:
            links.append(unquote(relative_path + link))
        for dir_link in dir_links:
            links += self.get_recursive_links(relative_path + dir_link)
        return links
