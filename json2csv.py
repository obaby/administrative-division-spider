import json
import pandas as pd
import sys, getopt


def json_to_csv(file_name, out_file=None):
    print('[*] 开始处理：', file_name)
    try:
        with open(file_name, 'r', encoding='gbk') as f:
            jd = json.load(f, encoding='gbk')
    except:
        with open(file_name, 'r') as f:
            jd = json.load(f)
    lines = []
    citys = jd['city']
    for c in citys:
        countrys = c['country']
        for cc in countrys:
            towns = cc['town']
            for t in towns:
                villagetrs = t['villagetr']
                for v in villagetrs:
                    line = {
                        'province_name': jd['name'],
                        # 'province_code': jd['code'],
                        'city_name': c['name'],
                        'city_code': c['code'],
                        'town_name': cc['name'],
                        'town_code': cc['code'],
                        'villagetr_name': t['name'],
                        'villagetr_code': t['code'],
                        'street_name': v['name'],
                        'street_code': v['code'],
                        'street_type': v['type']
                    }
                    lines.append(line)
                    # print(line)

    # print(lines)
    df = pd.read_json(json.dumps(lines))
    if out_file:
        df.to_csv(out_file, index=False)
    else:
        out_file = './csv2022/' + file_name.split('.')[0] + '.csv'
        df.to_csv('./csv2022/' + file_name.split('.')[0] + '.csv', index=False)
    print('[*] 保存文件', out_file)


def print_help():
    print('*' * 100)
    print('国家统计局行政区划爬虫 Json转CSV')
    print('http://h4ck.org.cn')
    print('obaby@mars')
    print('Usage: json2csv -a -i <inputfile> -o <outputfile>')
    print(' -a 转换当前目录下所有json文件')
    print(' -i json文件')
    print(' -o 转换后的csv文件')
    print('*' * 100)


def convert_all():
    import os
    file_dir = os.getcwd()  # 你的文件路径
    file_list = os.listdir(file_dir)
    for f in file_list:
        if f.endswith('.json'):

            json_to_csv(f)



def main(argv):
    inputfile = None
    outputfile = None
    try:
        opts, args = getopt.getopt(argv, "hai:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt == '-a':
            convert_all()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if inputfile:
        json_to_csv(inputfile, outputfile)
    else:
        print_help()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
