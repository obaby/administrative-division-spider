# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
import json
import time

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def get_main_page():
    province_list = []
    res = requests.get('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/index.html')
    res.encoding = 'utf-8'
    html_content = res.text
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
    res = requests.get(url)
    res.encoding = 'utf-8'
    html_content = res.text
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
    res = requests.get(url)
    res.encoding = 'utf-8'
    html_content = res.text
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
    time.sleep(1)
    return vl


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print('[*] 获取省份信息：')
    pl = get_main_page()
    print('[*] 省份数量：', len(pl))
    count = 1
    for p in pl:
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
    print('[D] 最终数据：')
    print(pl)
    with open("record.json", "w") as f:
        json.dump(pl, f)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
