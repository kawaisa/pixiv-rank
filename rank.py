#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import linecache
from pixivpy3 import *

sys.dont_write_bytecode = True

_REFRESH_TOKEN = "PIXIV_TOKEN"
_TEST_WRITE = False

def make_dir():
    os.makedirs('./tmp', exist_ok=True)

def create_html(aapi):

    def create_temp_html(illust_id, illust_title, illust_user_name, illust_image_large, illust_image_original):
        image_id = str(illust_id)
        image_title = str(illust_title)
        image_author = str(illust_user_name)
        image_large = str(illust_image_large.replace('i.pximg.net', 'i.pixiv.cat'))
        image_original = str(illust_image_original.replace('i.pximg.net', 'i.pixiv.cat'))
        main_temp_html = open('./tmp/main_temp.html', 'a')
        main_temp_html.write('<article class="thumb"> ')
        main_temp_html.write('<a href="' + image_original + '" class="image lazyload" data-src="' + image_large + '" ')
        main_temp_html.write('<img class="lazyload" data-src="' + image_large + '" alt="' + image_title + '"> ')
        main_temp_html.write('</a> ')
        main_temp_html.write('<h2>' + image_title + '</h2> ')
        main_temp_html.write('<p>' + image_author + ' - <a href="https://pixiv.net/i/' + image_id + '" target="_blank">pixiv.net/i/' + image_id + '</a></p> ')
        main_temp_html.write('</article>\n')
        main_temp_html.close()

    def return_temp_html(amount):
        for index in range(amount):
            illust = json_result.illusts[index]
            illust_id = illust.id
            illust_title = illust.title
            illust_user_name = illust.user.name
            illust_image_large = illust.image_urls.large
            illust_image_original = illust.meta_single_page.original_image_url or illust.meta_pages[0].image_urls.original
            create_temp_html(illust_id, illust_title, illust_user_name, illust_image_large, illust_image_original)

    # json_result = aapi.illust_ranking('day', date='1970-01-01')
    json_result = aapi.illust_ranking('day')
    illust_amount = len(json_result.illusts)
    return_temp_html(illust_amount)

    while True:
        illust_temp = illust_amount

        next_qs = aapi.parse_qs(json_result.next_url)
        json_result = aapi.illust_ranking(**next_qs)
        illust_amount = len(json_result.illusts)
        return_temp_html(illust_amount)

        illust_amount += illust_temp

        if illust_amount >= 150:
            break
        else:
            continue

    for line_number in range(1, 151):
        main_html = open('./tmp/main.html', 'a')
        main_html.write(linecache.getline('./tmp/main_temp.html', line_number).strip() + ' ')
        main_html.close()

    main_tpl = open('./tmp/main.html', 'r')
    main_tpl_html = main_tpl.read()
    main_tpl.close()
    template_tpl = open('./tpl/template.html', 'r')
    template_tpl_html = template_tpl.read()
    template_tpl.close()
    index_html = open('./dist/index.html', 'w')
    index_html.write(template_tpl_html.replace('{{main}}', main_tpl_html))
    index_html.close()

def remove_dir():
    shutil.rmtree('./tmp', ignore_errors=True)

def main():
    aapi = AppPixivAPI()
    aapi.auth(refresh_token=_REFRESH_TOKEN)
    make_dir()
    create_html(aapi)
    remove_dir()

if __name__ == '__main__':
    main()
