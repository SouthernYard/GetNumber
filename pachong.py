from bs4 import BeautifulSoup
import requests
import re


class GetPhoneNumber(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.117 Safari/537.36'
        }

    def get_phone_num(self, seg_phone_num):
        url = 'http://so.qqdna.com/mobile/shanghai_' + seg_phone_num + '.html'
        res = requests.get(url)
        res.encoding = 'gb2312'
        bf = BeautifulSoup(res.text, 'lxml')
        return str(self.filter_data(bf.body.table.tr.td))

    @staticmethod
    def filter_data(original_data):
        rr = re.compile(r'[1][0-9][0-9]{9}')
        list_string_data = str(rr.findall(str(original_data))[2:])
        filtered_data = list_string_data.replace(r'[', '')
        filtered_data = filtered_data.replace(r']', '')
        filtered_data = filtered_data.replace(r"', '", '\n')
        filtered_data = filtered_data.replace(r"'", '')
        return filtered_data


class GetPhoneSegment(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.117 Safari/537.36'
        }
        self.url = 'http://so.qqdna.com/city/shanghai/shanghai.php'

    def get_seg_num(self):
        res = requests.get(self.url)
        res.encoding = 'gb2312'
        bs = BeautifulSoup(res.text, 'lxml')
        all_seg = bs.findAll('li')
        return self.filter_data(all_seg)

    @staticmethod
    def filter_data(original_data):
        rr = re.compile(r'[1][0-9]+')
        list_string_data = rr.findall(str(original_data))
        data_remove_dup = list(set(list_string_data))
        data_remove_dup.sort(key=list_string_data.index)
        return data_remove_dup


if __name__ == '__main__':
    get_phone_seg = GetPhoneSegment()
    seg_num_list = get_phone_seg.get_seg_num()
    get_num = GetPhoneNumber()
    print("号码段数量：" + str(len(seg_num_list)))
    for seg_num in seg_num_list:
        data = get_num.get_phone_num(seg_num)
        fo = open(seg_num + '.txt', 'w')  # a: 追加， w: 覆盖
        fo.write(data)
        fo.close()


