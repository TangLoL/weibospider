import re
import time
import pandas as pd
from weibospider.common import Properties
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#登录

class weiboSpider:

    def __init__(self, file_name):
        print('----------------初始化浏览器------------------')
        p = Properties.Properties(file_name)
        self.linklist = list()
        self.userName = p.get('userName')
        self.password = p.get('password')
        self.keyword = p.get('keyword')
        self.starttime = p.get('time')
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.setting.userAgent'] = (p.get('useragent'))
        self.DRIVER = webdriver.PhantomJS(executable_path=p.get('phtomjsAdd'),desired_capabilities=dcap)
        self.DRIVER.set_window_size(1200, 600)

    def urlPj(self):

        pass


    def login(self):
        print('--------------正在登录---------------')
        self.DRIVER.get('https://weibo.com')
        WebDriverWait(self.DRIVER, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pl_login_form"]/div/div[3]/div[6]/a'))
        )
        self.DRIVER.save_screenshot('weibospider/common/picture/login.png')
        self.DRIVER.find_element_by_xpath('//*[@id="loginname"]').send_keys(self.userName)
        self.DRIVER.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys(self.password)
        self.DRIVER.find_element_by_xpath('//*[@id="loginname"]').send_keys(self.userName)
        #查看数否需要输入验证码
        vertify = self.DRIVER.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]').get_attribute("style")
        if (vertify != ''):
            self.DRIVER.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
            WebDriverWait(self.DRIVER, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="v6_pl_content_publishertop"]/div/div[2]/textarea'))
            )
        else:
            self.DRIVER.save_screenshot('weibospider/common/picture/vertifycode.png')
            yzm = input()
            self.DRIVER.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').send_keys(yzm)
            self.DRIVER.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
            WebDriverWait(self.DRIVER, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="v6_pl_content_publishertop"]/div/div[2]/textarea'))
            )
        self.DRIVER.save_screenshot('weibospider/common/picture/after.png')
        print(self.DRIVER.current_url)
        linkpare = re.findall('u/\d*?/home', self.DRIVER.current_url, re.S)
        if (len(linkpare) != 0):
            print('登录成功')
        else:
            print('登录失败')
            self.DRIVER.save_screenshot('weibospider/common/picture/failer.png')
        pass


    def blogparse(self):
        print('---------------------拉取微博信息开始-----------------------------')
        self.DRIVER.get(
            'http://s.weibo.com/weibo/kfc&Refer=STopic_box?c=spr_sinamkt_buy_hyww_weibo_p113')
        self.DRIVER.implicitly_wait(10)
        # 打开全部内容
        alist = self.DRIVER.find_elements_by_xpath(
            '//div[@class="feed_content wbcon"]/p[@class="comment_txt"]/a[@class="WB_text_opt"]')
        print(len(alist))
        for a in alist:
            a.click()
            time.sleep(0.7)
        # 检验是否合格
        commentfulllist = self.DRIVER.find_elements_by_xpath(
            '//div[@class="feed_content wbcon"]/p[@class="comment_txt" and @node-type="feed_list_content_full"]')
        print(len(commentfulllist))

        length = len(self.DRIVER.find_elements_by_xpath('//div[@class="WB_cardwrap S_bg2 clearfix"]'))

        ll = list()

        for i in range(length):
            map = dict()
            print('-------------------------本页第' + str(i + 1) + '条博客---------------------------------')
            # 昵称
            try:
                name = self.DRIVER.find_element_by_xpath(
                    '//div[@class="WB_cardwrap S_bg2 clearfix"]['+str(i+1)+']//div[@class="feed_content wbcon"]/a[@class="W_texta W_fb"]'
                ).text
                print(name)
                map['昵称'] = name
                # 认证
                try:
                    verify = self.DRIVER.find_element_by_xpath(
                        '//div[@class="WB_cardwrap S_bg2 clearfix"][' + str(
                            i + 1) + ']//div[@class="feed_content wbcon"]/a[@alt]'
                    ).get_attribute("alt")
                except:
                    verify = '无'
                map['认证'] = verify
                # 内容 + 发送位置
                try:
                    commentplace = self.DRIVER.find_element_by_xpath(
                        '//div[@class="WB_cardwrap S_bg2 clearfix"][' + str(
                            i + 1) + ']//div[@class="feed_content wbcon"]/p[@class="comment_txt"][last()]'
                    ).text.replace('\n', '').replace('收起全文d', '')
                    coms = commentplace.split('|')
                    comment = coms[0]
                    location = '无'
                    if (len(coms) > 1):
                        location = coms[1]
                except:
                    comment = '无'
                    location = '无'
                map['发布内容'] = comment
                map['发布位置'] = location
                # 图片
                try:
                    self.DRIVER.find_element_by_xpath('//div[@class="WB_cardwrap S_bg2 clearfix"][' + str(
                        i + 1) + ']//div[@class="feed_content wbcon"]/div[@class="WB_media_wrap clearfix"]//img[@class="bigcursor"]')
                    picture = 'true'
                except:
                    picture = 'false'
                map['图片'] = picture
                # 视频
                try:
                    self.DRIVER.find_element_by_xpath(
                        '//div[@class="WB_cardwrap S_bg2 clearfix"][' + str(
                            i + 1) + ']//div[@class="feed_content wbcon"]/div[@class="WB_media_wrap clearfix"]//div[@class="media_box_video_1"]')
                    video = 'true'
                except:
                    video = 'false'
                map['视频'] = video
                # 时间
                fbtime = self.DRIVER.find_element_by_xpath(
                    '//div[@class="WB_cardwrap S_bg2 clearfix"][' + str(
                        i + 1) + ']//div[@class="feed_from W_textb"]/a[@node-type="feed_list_item_date"]').text
                map['发布时间'] = fbtime
                # 发送端
                terminal = self.DRIVER.find_element_by_xpath(
                    '//div[@class="WB_cardwrap S_bg2 clearfix"][' + str(
                        i + 1) + ']//div[@class="feed_from W_textb"]/a[@rel="nofollow"]').text
                map['发布终端'] = terminal
                # 转发数
                forwardNum = self.DRIVER.find_element_by_xpath(
                    '//div[@class="WB_cardwrap S_bg2 clearfix"][' + str(
                        i + 1) + ']//div[@class="feed_action clearfix"]//a[@action-type="feed_list_forward"]/span/em').text
                if (forwardNum == ''):
                    forwardNum = '0'
                map['转发数'] = forwardNum
                # 评论数
                commentNum = self.DRIVER.find_element_by_xpath(
                    '//div[@class="WB_cardwrap S_bg2 clearfix"][' + str(
                        i + 1) + ']//div[@class="feed_action clearfix"]//a[@action-type="feed_list_comment"]'
                ).text.replace('评论', '').replace('\'', '')
                if (commentNum == ''):
                    commentNum = '0'
                map['评论数'] = commentNum
                # 点赞数
                likeNum = self.DRIVER.find_element_by_xpath(
                    '//div[@class="WB_cardwrap S_bg2 clearfix"][' + str(
                        i + 1) + ']//div[@class="feed_action clearfix"]//a[@action-type="feed_list_like"]/span/em').text
                if (likeNum == ''):
                    likeNum = '0'
                map['点赞数'] = likeNum
                # link
                link = self.DRIVER.find_element_by_xpath(
                    '//div[@class="WB_cardwrap S_bg2 clearfix"][' + str(
                        i + 1) + ']//div[@class="feed_content wbcon"]/a[@class="W_texta W_fb"]'
                ).get_attribute("href")
                self.linklist.append(link)
            except:
                continue
                pass

            ll.append(map)

        column = ['发布时间','昵称','发布内容','图片','视频','发布位置','发布终端',
          '转发数','评论数','点赞数','认证']
        blogdf = pd.DataFrame(ll,columns=column)

        return blogdf
        pass

    def personalparse(self):
        print('########################开始拉取个人信息################################')
        personallist = list()
        i=1
        length = len(self.linklist)
        for link in self.linklist:
            xxmap = dict()
            self.DRIVER.get(link)
            # obj.get('http://weibo.com/u/2000412191?refer_flag=1001030103_')
            nc2 = self.DRIVER.find_element_by_xpath('//div[@class="pf_username"]/h1').text
            xxmap['昵称2'] = nc2
            # 关注数
            focusNum = self.DRIVER.find_element_by_xpath(
                '//div[@class="PCD_counter"]/div/table/tbody/tr/td[1]//strong').text
            xxmap['关注数'] = focusNum
            # 粉丝数
            fansNum = self.DRIVER.find_element_by_xpath(
                '//div[@class="PCD_counter"]/div/table/tbody/tr/td[2]//strong').text
            xxmap['粉丝数'] = fansNum
            # 发布微博数
            blogTotalNum = self.DRIVER.find_element_by_xpath(
                '//div[@class="PCD_counter"]/div/table/tbody/tr/td[3]//strong').text
            xxmap['发送微博数'] = blogTotalNum
            WebDriverWait(self.DRIVER, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="Pl_Core_UserInfo__7"]/div/div/a'))
            )
            l = self.DRIVER.find_element_by_xpath(
                '//div[@class="PCD_person_info"]/a[@class="WB_cardmore S_txt1 S_line1 clearfix"]'
            ).get_attribute('href')
            self.DRIVER.get(l)
            # 基本信息模块
            try:
                xq = self.DRIVER.find_elements_by_xpath('//div[@class="WB_cardwrap S_bg2"]//li[@class="li_1 clearfix"]')
                for x in xq:
                    ss = x.text.replace('\n', '')
                    if (ss.startswith('所在地')):
                        # 所在地
                        xxmap['所在地'] = ss.split('：')[1]
                    if (ss.startswith('性别')):
                        # 性别
                        xxmap['性别'] = ss.split('：')[1]
                    if (ss.startswith('注册时间')):
                        # 注册时间
                        xxmap['注册时间'] = ss.split('：')[1]
            except:
                xxmap['所在地'] = '非个人微博'
                xxmap['性别'] = '非个人微博'
                xxmap['注册时间'] = '非个人微博'

            # 微博等级
            level = self.DRIVER.find_element_by_xpath('//div[@class="level_box S_txt2"]/a/span').text.replace('Lv.', '')
            xxmap['微博等级'] = level
            # 会员等级
            try:
                hylevel = self.DRIVER.find_element_by_xpath('//div[@class="pf_wrap"]/div/div[@class="pf_username"]/a/em').get_attribute(
                    "class")[-1]
            except:
                hylevel = '无'
                pass
            xxmap['会员等级'] = hylevel
            # 简介
            introduce = self.DRIVER.find_element_by_xpath('//div[@class="pf_wrap"]/div/div[@class="pf_intro"]').text
            xxmap['个人简介'] = introduce
            print('##################拉取成功第'+str(i)+'人，共'+str(length)+'人########################')
            personallist.append(xxmap)
            i+=1

        column = ['昵称2','所在地','性别','注册时间','关注数','粉丝数','发送微博数','微博等级','会员等级','个人简介']
        persondf = pd.DataFrame(personallist,columns=column)
        return persondf
        pass

    def combine(self,blog,person):
        print('-----------------合并微博与个人信息------------------')
        df = pd.merge(blog, person, left_on='昵称', right_on='昵称2')
        print(df)
        del df['昵称2']
        df.to_csv('dd.csv', mode='a', index=None)

if __name__ == '__main__':
    time1 = time.time()
    w = weiboSpider('file/file.properties')
    w.login()
    blogdf = w.blogparse()
    persondf = w.personalparse()
    w.combine(blogdf,persondf)
    print(time.time() - time1)
    pass








