# encoding: UTF-8
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def deleteWeibo(code):   # 参数为每条微博对应的唯一的一个字符串，使用weibo.cn打开一条微博的评论就能看到
    cook = {
        "Cookie": "your cookies"}

    url = 'http://weibo.cn/mblog/del?type=del&id=' + code + '&act=delc&rl=1&st=20b719'
    html = requests.get(url, cookies=cook)

    if html.text.find('删除成功!') != -1:
        print 'DELETED*!'
    else:
        print "NOT DEL"
    return 0

if __name__ == "__main__":
    num = 0
    for code in open("code.csv"):
        print code
        clearCode = code.strip()
        deleteWeibo(clearCode)
        num += 1
        print num
