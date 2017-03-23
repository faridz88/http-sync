import xmlrpc.client as xmlrpcClient
from urllib.parse import unquote, urlparse


class Aria2_API():

    def __init__(self, config):
        self.token = config['token']
        self.base_download_path = config['base_download_path']
        if self.base_download_path[-1] != '/':
            self.base_download_path += '/'
        self.xmlrpc_api = xmlrpcClient.ServerProxy(
            'http://' + config['host'] + ':' + str(config['port']) + '/rpc')

    def add_to_queue(self, url, path):
        try:
            opts = dict(dir=path, pause='true', header=[
                        'Accept-Language: ja', 'Accept-Charset: utf-8'])
            self.xmlrpc_api.aria2.addUri('token:' + self.token, [url], opts)
        except:
            print("ERR url:", url, "path:", path)

    def add_link_preserve_dir(self, url):
        path = self.base_download_path + \
            '/'.join(unquote(urlparse(url).path[1:]).split('/')[0:-1]) + '/'
        self.add_to_queue(url, path)
        # print('Path: "{0}" Url: "{1}"'.format(path, url))
