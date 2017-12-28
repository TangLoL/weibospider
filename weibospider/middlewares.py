# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.conf import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class WeibospiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)





class AJAXDownloaderMiddleware():

    def __init__(self):
        print(settings['USER_AGENT'])
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (settings['USER_AGENT'])
        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'],desired_capabilities=dcap)
        print('phantomjs is starting ...............')
        self.browser.set_window_size(1200,600)
        self.browser.get('https://weibo.com/login.php')
        self.browser.implicitly_wait(10)
        print(self.browser.current_url)
        self.browser.find_element_by_xpath('//*[@id="loginname"]').send_keys(settings['USERNAME'])
        self.browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys(settings['PASSWORD'])
        str = self.browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]').get_attribute("style")
        if(str == ''):
            print('you can find a picture in file pwd \n')
            print('please insert the vertification code : ')
            yzm = input()
            self.browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').send_keys(yzm)
        self.browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="v6_pl_content_publishertop"]/div/div[2]/textarea'))
        )
        self.browser.save_screenshot('E:\\ww.png')
        print('此时的URL为 ：'+self.browser.current_url)

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s


    def process_request(self,request,spider):
        print("phantomjs is running ....")
        try:
            print("访问" + request.url)
            self.browser.get(request.url)
            self.browser.implicitly_wait(10)
            alist = self.browser.find_elements_by_xpath('//div[@class="feed_content wbcon"]/p[@class="comment_txt"]/a[@class="WB_text_opt"]')
            print(str(len(alist)))
            for a in alist:
                a.click()
                time.sleep(0.7)
            commentfulllist = self.browser.find_elements_by_xpath('//div[@class="feed_content wbcon"]/p[@class="comment_txt" and @node-type="feed_list_content_full"]')
            print(str(len(commentfulllist)))
            pagelength = len(self.browser.find_elements_by_xpath('//div[@class="W_pages"]//li'))
            print('-----------------此网页有'+str(pagelength)+'页----------------')
            if(pagelength > 0):
                self.browser.find_element_by_xpath('//div[@class="W_pages"]/span/a').click()
            s_body = self.browser.page_source
            print(self.browser.current_url)
            return HtmlResponse(request.url, body= s_body,encoding='utf-8')
        except Exception as e:
            print(e)
            print("xxxxxxxxxxxxxxxxxxx")
            self.browser.quit()


    def spider_opened(self, spider):spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        self.browser.quit()
        spider.logger.info('Spider closed: %s' % spider.name)

