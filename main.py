#!/usr/bin/env python3
import configparser
import sys
import argparse

from dbop import DB_OP
from aria2api import Aria2_API
from extract_links import ExtractLinks


def main(config_file):
    # config_file = 'settings.conf'

    config = configparser.ConfigParser()
    config.read(config_file)

    el = ExtractLinks(config['source'])
    db = DB_OP(config['database']['file'])
    aria2api = Aria2_API(config['aria2c'])

    for main_link in el.get_main_dir_urls():
        print(main_link)
        print('DB Status: ', db.exists_in_db(main_link))
        if not db.exists_in_db(main_link):
            links = el.get_recursive_links(main_link)
            for link in links:
                print ("  ADD: ", el.base_url + link)
                aria2api.add_link_preserve_dir(el.base_url + link)
        db.add_link(main_link)
    db.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="increase output verbosity")
    args = parser.parse_args()
    print(args.config)
    if (args.config):
        main(args.config)
