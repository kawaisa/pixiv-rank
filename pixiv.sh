#!/usr/bin/env bash

script_path=`dirname $0`
tmp_file_path=${script_path}/dist
html_file_path=${script_path}/page
history_file_path=${html_file_path}/`date +%Y%m%d -d -1day | cut -c 1-4`/`date +%Y%m%d -d -1day|cut -c 5-6`/`date +%Y%m%d -d -1day|cut -c 7-8`

mkdir -p ${history_file_path}
mv ${html_file_path}/index.html ${history_file_path}/index.html
mv ${tmp_file_path}/index.html ${html_file_path}/index.html
