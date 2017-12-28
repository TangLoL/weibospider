import time
from weibospider.spiderScript import weibo

time1 = time.time()
w = weibo.weiboSpider('weibospider/spiderScript/file/file.properties')
w.login()
blogdf = w.blogparse()
persondf = w.personalparse()
w.combine(blogdf,persondf)
print(time.time() - time1)





if __name__ == '__main__':
    time1 = time.time()
    w = weibo.weiboSpider('file/file.properties')
    w.login()
    blogdf = w.blogparse()
    persondf = w.personalparse()
    w.combine(blogdf,persondf)
    print(time.time() - time1)
    pass