# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
import json
import time
import os


def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    print('*' * 100)
    print('国家统计局行政区划爬虫')
    print('http://h4ck.org.cn')
    print('obaby@mars')
    print('*' * 100)

from requests.adapters import HTTPAdapter

def http_get_with_retry(url):
    timeout = 10

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.149 Safari/537.36'
    }
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    try:
        r = s.get(url, timeout=timeout, headers=headers)
        r.encoding = 'utf-8'
        html_content = r.text
        return html_content
    except requests.exceptions.RequestException as e:
        print(e)
        return None

def http_get(url):
    timeout = 10

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.149 Safari/537.36'
    }

    try:
        res = requests.get(url, headers=headers,
                           timeout=timeout)
    except:
        try:
            res = requests.get(url, headers=headers,
                               timeout=timeout)
        except:
            res = requests.get(url, headers=headers,
                               timeout=timeout)
    res.encoding = 'utf-8'
    html_content = res.text
    return html_content

def get_main_page():
    province_list = []
    html_content =http_get('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/index.html')
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find('table')  # ,_class='')
    province_list_href = soup.find_all('td')
    for i in province_list_href:
        try:
            # print(i)
            name = i.text
            url = i.find('a')['href']
            if '\xa0' in name or '版权所有' in name:
                # print('ignore')
                pass
            else:
                pd = {'name': name,
                      'url': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/' + url}
                # print(pd)
                province_list.append(pd)
        except:
            pass
    return province_list


def get_city_pages(url):
    city_list = []
    html_content =http_get(url)
    soup = BeautifulSoup(html_content, "html.parser")
    province_list_href = soup.find_all('tr')
    baseurl = '/'.join(url.split('/')[:-1]) + '/'
    for i in province_list_href:
        tds = i.find_all('td')
        try:
            # print(i)
            code = tds[0].text
            name = tds[1].text

            url = i.find('a')['href']
            if '\xa0' in name or '版权所有' in name or '统计用' in name or name == '':
                # print('ignore')
                pass
            else:
                pd = {'name': name,
                      'code': code,
                      'url': baseurl + url}  # 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/'
                print(pd)
                city_list.append(pd)
        except:
            pass
    return city_list


def get_villagetr_list(url):
    vl = []
    html_content =http_get(url)
    soup = BeautifulSoup(html_content, "html.parser")
    province_list_href = soup.find_all('tr')
    for i in province_list_href:
        tds = i.find_all('td')
        try:
            # print(i)
            code = tds[0].text
            type = tds[1].text
            name = tds[2].text
            # url = i.find('a')['href']
            if '\xa0' in name or '版权所有' in name or '统计用' in name or name == '' or '城乡分类代码' in name or '名称' in name:
                # print('ignore')
                pass
            else:
                pd = {'name': name,
                      'code': code,
                      'type': type,
                      }
                print(pd)
                vl.append(pd)
        except:
            pass
    # time.sleep(1)
    return vl


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()
    print('[*] 获取省份信息：')
    pl = get_main_page()
    print('[*] 省份数量：', len(pl))
    count = 1
    for p in pl:
        try:
            if os.path.isfile(p['name'] +".json"):
                print('[E] 文件已经存在，跳过。')
                continue
            print('[*] 开始解析：', '第', count, '个', p['name'])
            count += 1
            cl = get_city_pages(p['url'])
            for c in cl:
                ccl = get_city_pages(c['url'])
                print('[*] 开始解析：', c['name'])
                for l in ccl:
                    print('[*] 开始解析：', l['name'])
                    town_list = get_city_pages(l['url'])
                    for t in town_list:
                        villagetr = get_villagetr_list(t['url'])
                        t['villagetr'] = villagetr
                    l['town'] = town_list

                c['country'] = ccl
            p['city'] = cl
            # break
            with open(p['name'] +".json", "w") as file_handle:
                json.dump(p, file_handle, ensure_ascii = False)
        except:
            print('[E] 发生异常，继续下一省份')
    print('[D] 全部完成.')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
