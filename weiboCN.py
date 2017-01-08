# encoding: UTF-8
import re
import requests
import getComment
import sys
import pymongo
reload(sys)
sys.setdefaultencoding( "utf-8" )

connection = pymongo.MongoClient()
tdb = connection.weibo
dbInsert = tdb.weiboContent

def getContent(StrPage):
    cook = {
	"Cookie": "your cookies"}
    url = 'http://weibo.cn/1401527553/profile?keyword=renew&hasori=0&haspic=0&endtime=20161231&advancedfilter=1&page=' + StrPage
    html = requests.get(url, cookies = cook)

    regexOriginal = re.compile(ur'<div class="c" id="M_([\d\w]{9})"><div><span class="ctt">(.*?)</span>.*?cmtfrm" class="cc">评论\[(\d{1,2})\]</a>.*?class="ct">(\d{2}月\d{2}日|[\d-]{10}) ([\d:]{5,8})&nbsp;来自(.*?)</span>')
    regexRepost = re.compile(ur'<div class="c" id="M_([\d\w]{9})"><div><span class="cmt">转发了&nbsp;<a href="(.*?)</a>.*?class="ctt">(.*?)</span>&nbsp;.*?class="cmt">转发理由:</span>(.*?)&nbsp;&nbsp;<a href="http://weibo.cn/attitude.*?class="cc">评论\[(\d{1,2})\]</a>.*?class="ct">(\d\d月\d\d日|[\d-]{10}) ([\d:]{5,8})&nbsp;来自(.*?)</span></div></div>')
    regexDeleted = re.compile(ur'<div class="c" id="M_([\d\w]{9})"><div><span class="cmt">转发了微博：</span><span class="ctt">(抱歉，此微博已被作者删除).*?class="cmt">转发理由:</span>(.*?)&nbsp;&nbsp;<a href="http://weibo.cn/attitude.*?class="cc">评论\[(\d{1,2})\]</a>.*?class="ct">(\d\d月\d\d日|[\d-]{10}) ([\d:]{5,8})&nbsp;来自(.*?)</span></div></div>')

    originalContent = re.findall(regexOriginal, html.text)
    repostContent = re.findall(regexRepost, html.text)
    deletedContent = re.findall(regexDeleted, html.text)
    originalTextCode = ''
    print 'Original WEIBO'
    originalKey = ['code', 'post', 'numComment', 'date', 'time', 'wherefrom']
    repostKey = ['code', 'originalAuthor', 'originalContent', 'repostContent', 'numComment', 'date', 'time', 'wherefrom']
    
    
    for i in range(len(originalContent)):
        text = ''
        originalList = []
        for j in range(6):
            originalList.append(originalContent[i][j].encode("utf8"))
            print originalContent[i][j].encode("utf8")
            text = text + str(originalContent[i][j]) + '\n'
        originalDict = dict(zip(originalKey, originalList))

        numComment = int(originalContent[i][2])
        if numComment != 0:
            print 'have comment!'
            originalTextCode = originalTextCode + str(originalContent[i][0]) + '/'
            originalDict['comment']=getComment.getComment(str(originalContent[i][0]))
        dbInsert.insert(originalDict)         
        textContent = open('textWeibo.txt','a')
        textContent.write(text)
        textContent.write("\n++++++++++++++++++++++++++++++++++\n")
        textContent.close()
        print '++++++++++++++++++++++++++++++++++'
    print 'aa'
    print originalTextCode
    f = open('weiboContentCode.txt','a')
    f.write(originalTextCode)
    f.close()
    #原文被删除的微博
    for i in range(len(deletedContent)):
        text = ''
        originalList = []
        for j in range(6):
            originalList.append(deletedContent[i][j].encode("utf8"))
            print deletedContent[i][j].encode("utf8")
            text = text + str(deletedContent[i][j]) + '\n'
        originalDict = dict(zip(originalKey, originalList))

        numComment = int(deletedContent[i][3])
        if numComment != 0:
            print 'have comment!'
            originalTextCode = originalTextCode + str(deletedContent[i][0]) + '/'
            originalDict['comment'] = getComment.getComment(str(deletedContent[i][0]))
        dbInsert.insert(originalDict)
        textContent = open('deleted.txt', 'a')
        textContent.write(text)
        textContent.write("\n++++++++++++++++++++++++++++++++++\n")
        textContent.close()
        print '++++++++++++++++++++++++++++++++++'
    print 'aa'
    print originalTextCode
    f = open('weiboContentCode.txt', 'a')
    f.write(originalTextCode)
    f.close()

    print '*************************'
    print 'Repost WEIBO'
    repostTextCode = ''
    for i in range(len(repostContent)):
        repostList = []
        text = ''
        for j in range(8):
            repostList.append(repostContent[i][j].encode("utf8"))
            print repostContent[i][j].encode("utf8")
            text = text + str(repostContent[i][j]) + '\n'
        repostDict = dict(zip(repostKey, repostList))
                
        numComment = int(repostContent[i][4])
        if numComment != 0:
            print 'have comment!'
            repostTextCode = repostTextCode + str(repostContent[i][0]) + '/'
            repostDict['comment']=getComment.getComment(str(repostContent[i][0]))
        dbInsert.insert(repostDict)             
        textContent = open('textWeibo.txt','a')
        textContent.write(text)
        textContent.write("\n++++++++++++++++++++++++++++++++++\n")
        textContent.close()
        print '++++++++++++++++++++++++++++++++++'
    print repostTextCode
    f = open('repostContentCode.txt','a')
    f.write(repostTextCode)
    f.close()
    print  len(repostContent)+len(originalContent) + len(deletedContent)


if __name__ == "__main__":
    for Page in range(1,4):
        StrPage = str(Page)
        getContent(StrPage)
        print Page