# encoding: UTF-8
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def getComment(contentToken):   # 参数为每条微博对应的唯一的一个字符串，使用weibo.cn打开一条微博的评论就能看到
    cook = {"Cookie": "your cookies"}

    url = 'http://weibo.cn/comment/' + contentToken
    html = requests.get(url, cookies=cook)
    allComment = []

    reGetComment = re.compile(ur'<div class="c" id="C.*?<a href=(.*?)</a>.*?<span class="ctt">(.*?)</span>.*?<span class="ct">(\d\d月\d\d日|[\d-]{10}) ([\d:]{4,10})&nbsp;来自(.*?)</span></div>')
    reGetPage = re.compile(ur'1/(\d+)页')
    content = re.findall(reGetComment, html.text)
    commentPage = re.findall(reGetPage, html.text)

    if len(commentPage) == 0:
        NumPage = 1
    else:
        NumPage = int(commentPage[0])
    filename = '微博的评论'
    for i in range(len(content)):
        oneComment = []
        for j in range(5):
            print content[i][j]
            oneComment.append(content[i][j])
            f = open(filename, 'a')
            f.write(str(content[i][j]))
            f.write('\n')
        f.write('--------------------------------\n')
        f.close()
        print '-------------------------------'
        allComment.append(oneComment)
    
    if NumPage >= 2:
        for page in range(2, NumPage+1):
            nextPageUrl = 'http://weibo.cn/comment/' + contentToken + '?page=' + str(page)
            html = requests.get(nextPageUrl, cookies=cook)
            content = re.findall(reGetComment, html.text)
            for i in range(len(content)):
                oneComment = []
                for j in range(5):
                    print content[i][j]
                    oneComment.append(content[i][j])
                    f2 = open(filename, 'a')
                    f2.write(str(content[i][j]))
                    f2.write('\n')
                f2.write('--------------------------------\n')
                f2.close()
                print '-------------------------------'
                allComment.append(oneComment)
    
    # print allComment
    print "DONE"
    return allComment