# -*-coding:utf-8-*-
import time
import urlparse
import urllib
import urllib2
from ju_setting import STATIC_ROOT
from utils.log import get_file_logger


def check_url(url):
    """
    如果 url头部没有加上http://则补充上，然后进行正则匹配，看url是否合法。
    """
    if not isinstance(url, str):
        return ''
    url_fields = list(urlparse.urlsplit(url))
    if url_fields[0] != 'http':
        url = 'http://' + url
    return url


class GetPageData(object):
    '''
    输入url抓取网页信息，并保存unicode格式的文本信息
    '''
    urls = []
    brand_names = []

    def __init__(self, url_list, brand_names=[]):
        for i in url_list:
            self.urls.append(check_url(i))
        for i in brand_names:
            self.brand_names.append(i)

        user_agent = 'Mozilla/6.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': user_agent}
        self.log = get_file_logger('ju_report')

    def get_page(self, url='', page_title=u'', decode_str='gbk'):
        """
        将url对应的界面数据以及名称打包成结果返回
        """
        try:
            page = ''
            if not url.strip():
                raise Exception('url is None')
            req = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(req)
            html = response.read()
            page = html.decode(decode_str)
        except Exception, e:
            self.log.error(e)
            return None

        result = {
            'data': page,
            'title': page_title,
        }
        return result

    def get_pages(self, page_title=u'', decode_str='gbk'):
        """
        针对ajax返回结果集
        """
        data = []
        for i in self.urls:
            try:
                if not i.strip():
                    raise Exception('i url is None')
                req = urllib2.Request(i, headers=self.headers)
                response = urllib2.urlopen(req)
                html = response.read()
                page = html.decode(decode_str)
                data.append(page)
            except Exception, e:
                self.log.error(e)
                continue
        return data

    def get_images(self, url='', brand_name=''):
        try:
            if not url.strip():
                raise Exception('url is None')
            dateline = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
            title = '/images' + brand_name
            path = STATIC_ROOT
            new_path = os.path.join(path, title)
            if not os.path.isdir(new_path):
                os.makedirs(new_path)
            urllib.urlretrieve(url, '%s/%s.jpg' % (new_path, brand_name+dateline))
            return True
        except Exception, e:
            self.log.error(e)
            return False
