import scrapy
import logging
from weibospider.items import WeibospiderItem
from scrapy.crawler import CrawlerProcess

class WBSpider(scrapy.Spider):

    name = 'wbSpider'
    start_urls = [
        'http://s.weibo.com/weibo/%25E7%258E%258B%25E8%2580%2585%25E8%258D%25A3%25E8%2580%2580&region=custom:41:1000&typeall=1&suball=1&timescope=custom:2017-12-01-8:2017-12-01-8&Refer=g?c=spr_sinamkt_buy_hyww_weibo_p113'
        # 'http://s.weibo.com/weibo/kfc&typeall=1&suball=1&timescope=custom:2017-12-01:2017-12-02&Refer=g?c=spr_sinamkt_buy_hyww_weibo_p113'
        # 'http://s.weibo.com/weibo/kfc?topnav=1&wvr=6&c=spr_sinamkt_buy_hyww_weibo_t113'
        # 'https://weibo.com/xinlanghunan?refer_flag=1001030103_'
        # 'https://weibo.com/p/1005052132734472/info?mod=pedit_more'
        # 'https://weibo.com/2311694415/about'
    ]

    def parse(self,response):
        length = len(response.xpath('//div[@class="W_pages"]//li'))
        url = response.url
        for i in range(length):
            link = url + '&page=' + str(i+1)
            print(link)
            yield scrapy.Request(url=link,callback=self.parseblog)

    def parseblog(self, response):
        self.log('######################开始解析微博页############################',logging.INFO)
        bloglist = response.xpath('//div[@class="WB_cardwrap S_bg2 clearfix"]/div[@action-type="feed_list_item"]')
        for blog in bloglist:

            wbitem = WeibospiderItem()
            userName = blog.xpath('.//div[@class="feed_content wbcon"]/a[@class="W_texta W_fb"]/text()').extract()[0].strip()
            self.log('#############正在解析'+userName+'###############',logging.INFO)
            certifyl = blog.xpath('.//div[@class="feed_content wbcon"]/a[2]/@alt').extract()
            if(len(certifyl)==0):
                certifyStyle = '无'
            else:
                certifyStyle = certifyl[0]
            contentall = blog.xpath('.//div[@class="feed_content wbcon"]/p[@class="comment_txt"][last()]'
                                 ).xpath('string(.)').extract()[0].replace('\u200b','').strip()
            contentlist = contentall.split('|')
            if(len(contentlist) > 1):
                content = contentlist[0]
                blogLocation = contentlist[1]
            else:
                content = contentlist[0]
                blogLocation = '无'
            medial = blog.xpath('.//div[@class="feed_content wbcon"]//div[@class="media_box"]')
            if(len(medial) >= 1 ):
                media = '是'
            else:
                media = '否'
            transNum = blog.xpath('.//div[@class="feed_action clearfix"]//a[@action-type="feed_list_forward"]'
                                  ).xpath('string(.)').extract()[0].replace('转发','')
            commentNum = blog.xpath('.//div[@class="feed_action clearfix"]//a[@action-type="feed_list_comment"]'
                                  ).xpath('string(.)').extract()[0].replace('评论','')
            likesNum = blog.xpath('.//div[@class="feed_action clearfix"]//a[@action-type="feed_list_like"]'
                                  ).xpath('string(.)').extract()[0]
            link = 'https://'+ blog.xpath('.//div[@class="feed_content wbcon"]/a[@class="W_texta W_fb"]/@href').extract()[0]
            issueTime = blog.xpath('.//div[@class="feed_from W_textb"]/a[1]/@title').extract()[0]
            try:
                terminal = blog.xpath('.//div[@class="feed_from W_textb"]/a[2]/text()').extract()[0]
            except:
                terminal = ''
            wbitem['issueTime'] = issueTime
            wbitem['terminal'] = terminal
            wbitem['userName'] = userName
            wbitem['certifyStyle'] = certifyStyle
            wbitem['content'] = content
            wbitem['blogLocation'] = blogLocation
            wbitem['media'] = media
            wbitem['transNum'] = transNum
            wbitem['commentNum'] = commentNum
            wbitem['likesNum'] = likesNum
            # print(wbitem)
            # print(link)
            yield scrapy.Request(url=link,meta= {'item':wbitem} ,callback=self.personparse)

    def personparse(self,response):
        # print(response.url)
        print('解析个人主页')
        focusFansAndBolg = response.xpath('//div[@class="PCD_counter"]')
        focusFansAndBolglist = focusFansAndBolg[0].xpath('.//strong/text()').extract()
        wbitem=response.meta['item']
        # wbitem = WeibospiderItem()
        wbitem['focusNum'] = focusFansAndBolglist[0]
        wbitem['fansNum'] = focusFansAndBolglist[1]
        wbitem['blogTotalNum'] = focusFansAndBolglist[2]
        link = 'https://weibo.com' + response.xpath('//div[@class="PCD_person_info"]/a/@href').extract()[0].replace('//weibo.com','')
        # print(wbitem)
        # print(link)
        # print(wbitem)
        yield scrapy.Request(url=link,meta= {'item':wbitem} ,callback=self.personparsemore)

    def personparsemore(self,response):
        print('解析个人主页more')
        wbitem = response.meta['item']
        # wbitem = WeibospiderItem()

        xyxxlist = response.xpath('//*[@id="Pl_Official_PersonalInfo__58"]/div[1]//li[@class="li_1 clearfix"]'
                                  ).xpath('string(.)').extract()
        if(len(xyxxlist)!=0):
            for xyxx in xyxxlist:
                xyxxl = xyxx.split("：")
                if(xyxxl[0].strip() == '性别'):
                    wbitem['sex'] = xyxxl[1].strip()
                elif(xyxxl[0].strip() == '所在地'):
                    wbitem['userLocation'] = xyxxl[1].strip()
                elif(xyxxl[0].strip() == '注册时间'):
                    wbitem['regTime'] = xyxxl[1].strip()
                elif(xyxxl[0].strip() == '生日'):
                    wbitem['birthday'] = xyxxl[1].strip()
                else:
                    wbitem['birthday'] = ''
        else:
            wbitem['sex'] = '非个人微博'
            wbitem['userLocation'] = '非个人微博'
            wbitem['regTime'] = '非个人微博'
            wbitem['birthday'] = '非个人微博'

        blogLevel = response.xpath('//div[@class="PCD_person_detail"]//p[@class="level_info"]//span[@class="S_txt1"]/text()'
                       ).extract()[0].replace('Lv.','')

        introduction = response.xpath('//*[@id="Pl_Official_Headerv6__1"]//div[@class="PCD_header"]//div[@class="pf_intro"]/text()'
                                      ).extract()[0].strip()

        wbitem['blogLevel'] = blogLevel
        wbitem['introduction'] = introduction
        yield wbitem




process = CrawlerProcess({

    'DOWNLOADER_MIDDLEWARES':{'weibospider.middlewares.AJAXDownloaderMiddleware':543},
    'ITEM_PIPELINES' : {'weibospider.pipelines.WeibospiderPipeline': 100},
    'ROBOTSTXT_OBEY' : False,
    'RETRY_ENABLED' : True,
    'REDIRECT_ENABLED' : False,
    'LOG_LEVEL' : 'INFO',
    'DOWNLOAD_DELY' :0.25
})
process.crawl(WBSpider)
process.start()
