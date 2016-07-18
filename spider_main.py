#coding:utf8
from baike_spider import url_manager, html_downloader, html_parser, html_output
from bs4 import BeautifulSoup
import re

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloder =  html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.output = html_output.HtmlOutput()
        
    
    def craw(self, root_url):
        count = 1 
        #添加root url到管理器 
        self.urls.add_new_url(root_url)#添加单个url
        #当管理器中有url，就启动爬虫循环
        while self.urls.has_new_url():
            try:
                #在当前url中获取新的url
                new_url = self.urls.get_new_url()
                #打印爬取的是第几个url
                print "craw %d : %s" %(count,new_url)
                #启动下载器，下载页面
                html_cont = self.downloder.download(new_url)
#                print html_cont
#                if html_cont is not None:
#                    soup = BeautifulSoup(html_cont, "html.parser", from_encoding= "utf-8")
#                    links = soup.find_all("a",href = re.compile(r"/view/\d+.htm"))
#                    print links         
                #调用解析器，解析页面
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                #处理获取的url和数据
                self.urls.add_new_urls(new_urls) #添加批量url
                self.output.collect_data(new_data)                   
                if count == 100:
                    break
                count = count + 1
            #异常抛出
            except:
               print "craw faild"
        print "craw finished"    
        self.output.html_output()



if __name__=="__main__":
    root_url = "http://baike.baidu.com/view/21087.htm"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)