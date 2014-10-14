#coding=utf-8
'''
Created on 2014��9��25��

@author: Wang
''' 
import urllib2
import re
import string

class HTML_Tool:  
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片  
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")  
      
    # 用非 贪婪模式 匹配 任意<>标签  
    EndCharToNoneRex = re.compile("<.*?>")  
  
    # 用非 贪婪模式 匹配 任意<p>标签  
    BgnPartRex = re.compile("<p.*?>")  
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")  
    CharToNextTabRex = re.compile("<td>")  
  
    # 将一些html的符号实体转变为原始符号  
    replaceTab = [("<","<"),(">",">"),("&","&"),("&","\""),(" "," ")]  
      
    def Replace_Char(self,x):  
        x = self.BgnCharToNoneRex.sub("",x)  
        x = self.BgnPartRex.sub("\n    ",x)  
        x = self.CharToNewLineRex.sub("\n",x)  
        x = self.CharToNextTabRex.sub("\t",x)  
        x = self.EndCharToNoneRex.sub("",x)  
  
        for t in self.replaceTab:    
            x = x.replace(t[0],t[1])    
        return x  

class TiebaSpider:
    def __init__(self, url):
        self.myUrl = url + '?see_lz=1'
        self.datas = [] 
        self.myTool = HTML_Tool()
        
        
    def tieba(self):
        mypage = urllib2.urlopen(self.myUrl).read().decode("gbk")
        #计算应该发了多少页
        pageCount = self.getPage(mypage)
        title = self.findTitle(mypage)
        print u'文章标题： ' + title
        self.saveData(self.myUrl,title, pageCount)
        
    def getPage(self, page):
        myMatch = re.search(r'class="red">(\d+?)</span>', page, re.S)
        if myMatch:
            endPage = int(myMatch.group(1))
            print u'爬虫报告：发现楼主共有%d页内容' % endPage
        else:
            endPage = 0
            print u'爬虫报告：无法找出楼主发布内容的页数'
        return endPage
    
    def findTitle(self, page):
        myMatch = re.search(r'<h1.*?>(.*?)</h1>', page, re.S) 
        title = u'暂无标题'
        if myMatch:
            title = myMatch.group(1)
        else:
            print u'爬虫报告：无法加载文章标题'
        title = title.replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('>','').replace('<','').replace('|','')  
        return title
    
    def saveData(self, url, title, endPage):
        self.getDate(url, endPage)
        f = open(title+'.txt', 'w+')
        try:
            f.writelines(self.datas)
        except:
            print u'不能写入文件'
        finally:
            print u'不能运行到这里'
        f.close()
        print u'爬虫报告：文件已下载到本地'
        print u'请按任意键退出'
        raw_input();
    
    def getDate(self, url, endPage):
        url = url + '&pn='
        for i in range(2, endPage+1):
            print u'爬虫报告：爬虫%d页正在抓取...' % i
            myPage = urllib2.urlopen(url + str(i)).read()
            self.deal_data(myPage.decode('gbk'))
            
    def deal_data(self, myPage):
        myItems = re.findall('id="post_content.*?>(.*?)</div>', myPage, re.S)
        print myItems
        for item in myItems:
            #data = self.myTool.Replace_Char(item.replace("\n","").encode('gbk'))  
            data = item.encode('gbk')
            self.datas.append(data+'\n')
        
#-------- 程序入口处 ------------------  
print u"""#--------------------------------------- 
#   程序：百度贴吧爬虫 
#   版本：0.5 
#   作者：why 
#   日期：2013-05-16 
#   语言：Python 2.7 
#   操作：输入网址后自动只看楼主并保存到本地文件 
#   功能：将楼主发布的内容打包txt存储到本地。 
#--------------------------------------- 
"""  

# 以某小说贴吧为例子  
# bdurl = 'http://tieba.baidu.com/p/2296712428?see_lz=1&pn=1'  

print u'请输入贴吧的地址最后的数字串：'  
bdurl = 'http://tieba.baidu.com/p/769249760'# + str(raw_input(u'http://tieba.baidu.com/p/'))   
  
#调用  
mySpider = TiebaSpider(bdurl)  
mySpider.tieba()         
                
                
                
            
        
        