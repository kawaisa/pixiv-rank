import os
import sys
import shutil
from pixivpy3 import AppPixivAPI, PixivError

# 填入获取到的TOKEN
REFRESH_TOKEN = "PIXIV_TOKEN"
OUTPUT_DIR = './dist'
TEMPLATE_PATH = './tpl/template.html'
MAX_ILLUSTS = 150

def fetch_pixiv_ranking(aapi, max_count):
    # 获取指定数量的每日插画排行
    all_illusts = []
    try:
        json_result = aapi.illust_ranking('day')
        while json_result and json_result.illusts and len(all_illusts) < max_count:
            all_illusts.extend(json_result.illusts)
            next_qs = aapi.parse_qs(json_result.next_url)
            if not next_qs:
                break
            json_result = aapi.illust_ranking(**next_qs)
    except PixivError as e:
        print(f"API Error: {e}")
        return []
    return all_illusts[:max_count]

def create_illust_html(illust):
    # 为单个插画对象生成HTML片段
    original_url = illust.meta_single_page.original_image_url or \
                   (illust.meta_pages[0].image_urls.original if illust.meta_pages else illust.image_urls.large)
    
    # 替换域名以使用反向代理
    large_url = illust.image_urls.large.replace('i.pximg.net', 'www.lollipop.workers.dev')
    original_url = original_url.replace('i.pximg.net', 'www.lollipop.workers.dev')

    return (
        f'<article class="thumb"> '
        f'<a href="{original_url}" class="image lazyload" data-src="{large_url}"> '
        f'<img class="lazyload" data-src="{large_url}" alt="{illust.title}"> '
        f'</a> '
        f'<h2>{illust.title}</h2> '
        f'<p>{illust.user.name} - <a href="https://pixiv.net/i/{illust.id}" target="_blank">pixiv.net/i/{illust.id}</a></p> '
        f'</article>'
    )

def main():
    aapi = AppPixivAPI()
    try:
        aapi.auth(refresh_token=REFRESH_TOKEN)
    except PixivError as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)

    print("Fetching illustrations from Pixiv...")
    illusts = fetch_pixiv_ranking(aapi, MAX_ILLUSTS)
    if not illusts:
        print("No illustrations found or API error.")
        return

    print(f"Generating HTML for {len(illusts)} illustrations...")
    main_content = ' '.join([create_illust_html(illust) for illust in illusts])

    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template_html = f.read()

        output_html = template_html.replace('{{main}}', main_content)
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(output_html)
        
        print(f"Successfully created index.html in {OUTPUT_DIR}")

    except FileNotFoundError:
        print(f"Error: Template file not found at {TEMPLATE_PATH}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
