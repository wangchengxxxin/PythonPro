#coding=utf-8
'''
Created on 2014��9��25��

@author: Wang
''' 
import urllib
import urllib2
import re
import time
import thread
from urllib2 import HTTPError, URLError

class Spider:
    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False
        
    def GetPage(self, page):
        myUrl = "http://www.qiushibaike.com/hot/page/" + page 
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        headers = { 'Connection': 'Keep-Alive',
                    'Accept': 'text/html, application/xhtml+xml, */*',
                    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko' }
        req = urllib2.Request(myUrl, headers = headers)
        try:
            rec = urllib2.urlopen(req)
        except HTTPError, e:
            print '打开url出现错误'
            print 'Error code: ', e.code
        except URLError, e:
            print 'URLError reason: ', e.reason

        myPage = rec.read()
        #转成Unicode编码
        unicodePage = myPage.decode("utf-8")
        
        #整个页面读取出来之后   再读出所需要的信息
       # myItems = re.findall('<div.*?class="content".*?title="(.*?)">(.*?)</div>', unicodePage, re.S)
        myItems = re.findall('<div.*?class="content".*?title="(.*?)">(.*?)</div>', unicodePage, re.S)
        items = []
        for item in myItems:
            items.append([item[0].replace("\n",""), item[1].replace("\n", "")])
        return items
    
    def LoadPage(self):
        while self.enable:
            if len(self.pages) < 2:
                try:
                    myPage = self.GetPage(str(self.page))
                    self.page += 1
                    self.pages.append(myPage)
                except HTTPError, e:
                    print '无法链接糗事百科', e.code
            else:
                time.sleep(1)   
                
    def ShowPage(self, nowPage, page):
        for item in nowPage:
            print u'第%d页'  % page,item[0], item[1]
            myInput = raw_input()
            if myInput == 'quit':
                self.enable = False
                break
            
    def Start(self):
        self.enable = True
        page = self.page
        
        print u'正在下载网页   请等待。。。'
        
        thread.start_new_thread(self.LoadPage, ())
      
        #self.LoadPage()            
        while self.enable:
            if self.pages:
                nowPage = self.pages[0]
                del self.pages[0]
                self.ShowPage(nowPage, page)
                page += 1
                
                
print u"""
---------------------------------------  
   程序：糗百爬虫  
   版本：0.3  
   作者：why  
   日期：2014-06-03  
   语言：Python 2.7  
   操作：输入quit退出阅读糗事百科  
   功能：按下回车依次浏览今日的糗百热点  
---------------------------------------  
"""  

print u'请按下回车浏览今日的糗百内容'
raw_input(' ')
myModel = Spider()
myModel.Start()
                  
            
        
        