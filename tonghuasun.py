import json
import os
import time
import re
import requests
import pandas as pd
from lxml import etree


class T:

    def __init__(self):
        self.time = time.strftime("%Y%m%d%H%M%S", time.localtime())

        self.url = 'http://stock.10jqka.com.cn/hsdp_list/'
        self.url_list = ['http://news.10jqka.com.cn/today_list/', 'http://news.10jqka.com.cn/cjzx_list/',
                         'http://news.10jqka.com.cn/cjkx_list/', 'http://news.10jqka.com.cn/guojicj_list/',
                         'http://news.10jqka.com.cn/jrsc_list/', 'http://news.10jqka.com.cn/fortune_list/',
                         'http://news.10jqka.com.cn/cjkx_list/', 'http://yuanchuang.10jqka.com.cn/ycall_list/']
        self.url_list1 = ['http://news.10jqka.com.cn/fortune_list/']

        self.file_name = 'date_parm1.txt'
        self.file_name1 = ''
        self.data = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
        }

    # 校验文件是否存在不存在生成，存在数据为空提醒
    def chek_file(self, file_name):
        if not os.path.isfile(file_name):
            with open(file_name, 'w'):
                print('自动生成 %s 文件，请在里面添加url数据。。' % file_name)
                time.sleep(10)
        elif os.path.getsize(file_name) == 0:
            print('%s 文件数据为空，请添加url数据。。' % file_name)
            time.sleep(10)
        else:
            return True

    # 生成时间戳为名字的文件夹
    def establish_folder(self):
        os.mkdir(str(self.time))

    # 再时间戳文件夹里生成数据文件
    def write_file(self, file_name, content_list):
        # print('content_list：' + str(content_list))
        file_name = file_name + str(self.time) + '.xlsx'
        df = pd.DataFrame(content_list)
        df.to_excel(file_name, engine='xlsxwriter')

    # 读取指定txt文件中数据
    def rand_txt(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            url_list = []
            while True:
                url = str(f.readline()).replace('\n', '')

                if url == '' or url == None:
                    break
                else:
                    url_list.append(url)
        return url_list

    # 获取请求响应
    def get_data(self, url, headers):
        try:
            print(url)
            response = requests.get(url, timeout=2, headers=headers).content.decode('gbk', errors='ignore')
            return response
        except requests.Timeout as e:
            print(e)
            return self.get_data(url, headers)

    def get_data1(self, url, headers):
        try:
            print(url)
            response = requests.get(url, headers=headers).content.decode('gbk', errors='ignore')
            tz_url = re.findall('''<meta http-equiv="Refresh" content="1;URL=(.*?)">''', response)
            if len(tz_url) != 0:
                print(tz_url[0])
                # if 'stockstar' in tz_url[0] or 'finance.sina' in tz_url[0]:
                #     response = requests.get(tz_url[0],timeout=5, headers=headers).content.decode('utf-8', errors='ignore')
                #     return response
                # else:
                response = requests.get(tz_url[0], timeout=5, headers=headers).content.decode('utf-8', errors='ignore')
                return response
            else:
                return response
        except requests.Timeout as e:
            print(e)
            return self.get_data(url, headers)
        except Exception as e:
            return '500'

    def analysis_json(self, json_data):
        data = json.loads(json_data)

    def analysis_html(self, html_data):
        elemet = etree.HTML(html_data)
        ele_list = elemet.xpath('''//div[@class='list-con']/ul/li''')
        url_list = []

        for ele in ele_list:
            data = {}
            url = ele.xpath('''./span[@class='arc-title']/a/@href''')[0]
            title = ele.xpath('''./span[@class='arc-title']/a/text()''')[0]
            date = ele.xpath('''./span[@class='arc-title']/span/text()''')[0]

            data["url"] = url
            data["title"] = title
            data["date"] = date
            print(data)
            url_list.append(data)
        return url_list

    def analysis_html1(self, html_data):
        try:
            if '无法找到网页' in html_data:
                return ''
            # print(html_data)
            element = etree.HTML(html_data)
            content = ''
            if len(content) == 0:
                print("============1================")
                content = element.xpath('''string(//div[@class='main-text atc-content'])''').replace(u'\u3000',
                                                                                                     u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============2================")
                content = element.xpath('''string(//div[@class='txtdiv'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============3================")
                content = element.xpath('''string(//div[@class='rich_media_content '])''').replace(u'\u3000',
                                                                                                   u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============4================")
                content = element.xpath('''string(//div[@class='txtdiv'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============5================")
                content = element.xpath('''string(//div[@class='article-content fontSizeSmall BSHARE_POP'])''').replace(
                    u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============6================")
                content = element.xpath('''string(//div[@class='article'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============7================")
                content = element.xpath('''string(//div[@class='nml_arti'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============8================")
                content = element.xpath('''string(//div[@class='g-articl-text'])''').replace(u'\u3000', u' ').strip()
                print(str(content))

            if len(content) == 0:
                print("============9================")
                content = element.xpath('''string(//div[@id='ozoom'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============10================")
                content = element.xpath('''string(//div[@class='newstextbox'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============11================")
                content = element.xpath('''string(//div[@class='t-context f16 picture'])''').replace(u'\u3000',
                                                                                                     u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============12================")
                content = element.xpath('''string(//div[@id='ContentBody'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============13================")
                content = element.xpath('''string(//div[@class='m-articleContent'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============14================")
                content = element.xpath('''string(//div[@class='article-content'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============15================")
                content = element.xpath('''string(//div[@class='txtContent'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============16================")
                content = element.xpath('''string(//div[@class='t3'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============17================")
                content = element.xpath('''string(//div[@class='newsdetatext'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============18================")
                content = element.xpath('''string(//div[@class='txtdiv clearfix'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============19================")
                content = element.xpath('''string(//div[@class='news_txt'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============20================")
                content = element.xpath('''string(//div[@class='art_context'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============21================")
                content = element.xpath('''string(//div[@class='contenttext auto'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============22================")
                content = element.xpath('''string(//div[@class='content_zw bgwhite'])''').replace(u'\u3000',
                                                                                                  u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============23================")
                content = element.xpath('''string(//div[@class='xw_cont'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============23================")
                content = element.xpath('''string(//div[@class='content-article'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============24================")
                content = element.xpath('''string(//div[@class='news_content'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============25================")
                content = element.xpath('''string(//div[@class='content-lcq'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============26================")
                content = element.xpath('''string(//div[@class='newscontents'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============27================")
                content = element.xpath('''string(//div[@class='bgray neirong'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============28================")
                content = element.xpath('''string(//div[@class='left_zw'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============29================")
                content = element.xpath('''string(//div[@class='content'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============30================")
                content = element.xpath('''string(//div[@class='c-article__detail'])''').replace(u'\u3000',
                                                                                                 u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============31================")
                content = element.xpath('''string(//div[@class='htyj_nrbody'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============32================")
                content = element.xpath('''string(//div[@class='arccon'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============33================")
                content = element.xpath('''string(//div[@class='container_full main_cont'])''').replace(u'\u3000',
                                                                                                        u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============34================")
                content = element.xpath('''string(//div[@style='text-indent:2em;'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============35================")
                content = element.xpath('''string(//div[@class='article-content mar-t-20'])''').replace(u'\u3000',
                                                                                                        u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============36================")
                content = element.xpath('''string(//div[@class='mleft'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============37================")
                content = element.xpath('''string(//div[@id='multi-text'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============38================")
                content = element.xpath('''string(//div[@class='articleBox cfix mb20'])''').replace(u'\u3000',
                                                                                                    u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============39================")
                content = element.xpath(
                    '''string(//div[@class='article-detail-inner article-relevance w660 ov'])''').replace(u'\u3000',
                                                                                                          u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============40================")
                content = element.xpath('''string(//div[@class='xx_boxsing'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============41================")
                content = element.xpath('''string(//div[@class='u-mainText'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            if len(content) == 0:
                print("============42================")
                content = element.xpath('''string(//div[@class='div_content'])''').replace(u'\u3000', u' ').strip()
                print(str(content))
            return content
        except AttributeError:
            return ''

    def analysis_html2(self, html_data):
        if '无法找到网页' in html_data:
            return ''
        print(html_data)
        elemet = etree.HTML(html_data)

        content = elemet.xpath('''string(//div[@class='txtdiv'])''')

        return content

    def factory(self):
        if self.chek_file(self.file_name):
            data_list = []
            try:
                date_list = self.rand_txt(self.file_name)
                for date in date_list:
                    for url in self.url_list:
                        url1 = url + str(date) + '/'
                        html_data = self.get_data(url1, self.headers)
                        url_list = self.analysis_html(html_data)
                        print(url_list)
                        for data in url_list:
                            html_data1 = self.get_data1(data['url'], self.headers)
                            if html_data1 == '500':
                                continue
                            content = self.analysis_html1(html_data1)
                            data['date'] = str(date[0:4]) + '年' + data['date']
                            data['content'] = content
                            print(data)
                            data_list.append(data)
                            time.sleep(1)
                        time.sleep(1)
                self.write_file('data', data_list)
            except Exception as e:
                print(e)
                self.write_file('data1', data_list)


if __name__ == '__main__':
    t = T()
    t.factory()
