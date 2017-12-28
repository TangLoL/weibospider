import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


time1 = time.time()
#浏览器1登录

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap['phantomjs.page.setting.userAgent'] = ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
obj = webdriver.PhantomJS(executable_path='E:\\Source\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe',desired_capabilities=dcap)
obj.set_window_size(1200, 600)

obj.get('https://weibo.com')
element = WebDriverWait(obj, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="pl_login_form"]/div/div[3]/div[6]/a'))
    )
obj.save_screenshot('weibospider/spiderScript/picture/login.png')
obj.find_element_by_xpath('//*[@id="loginname"]').send_keys('1026198058@qq.com')
obj.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('T1026198058')
obj.find_element_by_xpath('//*[@id="loginname"]').send_keys('1026198058@qq.com')
obj.save_screenshot('weibospider/spiderScript/picture/middle.png')
vertify =  obj.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]').get_attribute("style")
if(vertify != ''):
    obj.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
else:
    obj.save_screenshot('weibospider/spiderScript/picture/vertifycode.png')
    yzm = input()
    obj.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').send_keys(yzm)
    obj.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
# obj.save_screenshot('weibospider/common/picture/after1.png')
print(obj.current_url)
strs = re.findall('u/\d*?/home',obj.current_url,re.S)

if(len(strs) != 0):
    print('登录成功')
else:
    print('登录失败')
    obj.save_screenshot('weibospider/spiderScript/picture/failer.png')

#######################################################################################
obj.get('http://s.weibo.com/weibo/kfc&Refer=STopic_box?c=spr_sinamkt_buy_hyww_weibo_p113')
#打开全部内容
alist = obj.find_elements_by_xpath('//div[@class="feed_content wbcon"]/p[@class="comment_txt"]/a[@class="WB_text_opt"]')
print(len(alist))
for a in alist:
    a.click()
    time.sleep(0.7)
#检验是否合格
commentfulllist = obj.find_elements_by_xpath('//div[@class="feed_content wbcon"]/p[@class="comment_txt" and @node-type="feed_list_content_full"]')
print(len(commentfulllist))

length = len(obj.find_elements_by_xpath('//div[@class="WB_cardwrap S_bg2 clearfix"]'))

ll = list()
linklist = list()

for i in range(length):
    map = dict()
    print('-------------------------本页第'+ str(i+1) +'条博客---------------------------------')
    #昵称
    name = obj.find_element_by_xpath('//div[@class="WB_cardwrap S_bg2 clearfix"][4]//div[@class="feed_content wbcon"]/a[@class="W_texta W_fb"]').text
    map['昵称'] = name
    #认证
    try:
        verify = obj.find_element_by_xpath(
            '//div[@class="WB_cardwrap S_bg2 clearfix"]['+ str(i+1) +']//div[@class="feed_content wbcon"]/a[@alt]'
        ).get_attribute("alt")
    except:
        verify = '无'
    map['认证'] = verify
    #内容 + 发送位置
    try:
        commentplace = obj.find_element_by_xpath(
            '//div[@class="WB_cardwrap S_bg2 clearfix"]['+str(i+1)+']//div[@class="feed_content wbcon"]/p[@class="comment_txt"][last()]'
                                            ).text.replace('\n','').replace('收起全文d','')
        coms = commentplace.split('|')
        comment = coms[0]
        location = '无'
        if(len(coms) > 1):
            location = coms[1]
    except:
        comment = '无'
        location = '无'
    map['发布内容'] = comment
    map['发布位置'] = location
    #图片
    try:
        obj.find_element_by_xpath('//div[@class="WB_cardwrap S_bg2 clearfix"]['+str(i+1)+']//div[@class="feed_content wbcon"]/div[@class="WB_media_wrap clearfix"]//img[@class="bigcursor"]')
        picture = 'true'
    except:
        picture = 'false'
    map['图片'] = picture
    #视频
    try:
        obj.find_element_by_xpath(
            '//div[@class="WB_cardwrap S_bg2 clearfix"]['+str(i+1)+']//div[@class="feed_content wbcon"]/div[@class="WB_media_wrap clearfix"]//div[@class="media_box_video_1"]')
        video = 'true'
    except:
        video = 'false'
    map['视频'] = video
    #时间
    fbtime = obj.find_element_by_xpath(
        '//div[@class="WB_cardwrap S_bg2 clearfix"]['+str(i+1)+']//div[@class="feed_from W_textb"]/a[@node-type="feed_list_item_date"]').text
    map['发布时间'] = fbtime
    #发送端
    terminal = obj.find_element_by_xpath(
        '//div[@class="WB_cardwrap S_bg2 clearfix"]['+str(i+1)+']//div[@class="feed_from W_textb"]/a[@rel="nofollow"]').text
    map['发布终端'] = terminal
    #转发数
    forwardNum = obj.find_element_by_xpath(
        '//div[@class="WB_cardwrap S_bg2 clearfix"]['+str(i+1)+']//div[@class="feed_action clearfix"]//a[@action-type="feed_list_forward"]/span/em').text
    if(forwardNum == ''):
        forwardNum = '0'
    map['转发数'] = forwardNum
    # 评论数
    commentNum = obj.find_element_by_xpath(
        '//div[@class="WB_cardwrap S_bg2 clearfix"]['+str(i+1)+']//div[@class="feed_action clearfix"]//a[@action-type="feed_list_comment"]'
    ).text.replace('评论','').replace('\'','')
    if(commentNum == ''):
        commentNum = '0'
    map['评论数'] = commentNum
    #点赞数
    likeNum = obj.find_element_by_xpath(
        '//div[@class="WB_cardwrap S_bg2 clearfix"]['+str(i+1)+']//div[@class="feed_action clearfix"]//a[@action-type="feed_list_like"]/span/em').text
    if(likeNum == ''):
        likeNum = '0'
    map['点赞数'] = likeNum
    #link
    link = obj.find_element_by_xpath(
            '//div[@class="WB_cardwrap S_bg2 clearfix"]['+str(i+1)+']//div[@class="feed_content wbcon"]/a[@class="W_texta W_fb"]'
    ).get_attribute("href")
    linklist.append(link)
    ll.append(map)
time2 = time.time()
blogdf = pd.DataFrame(ll)

personallist = list()
for link in linklist:
    xxmap = dict()
    obj.get(link)
    obj.get('http://weibo.com/u/2000412191?refer_flag=1001030103_')
    WebDriverWait(obj, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="Pl_Core_UserInfo__7"]/div/div/a'))
    )
    l = obj.find_element_by_xpath(
        '//div[@class="PCD_person_info"]/a[@class="WB_cardmore S_txt1 S_line1 clearfix"]'
    ).get_attribute('href')
    nc2 = obj.find_element_by_xpath('//div[@class="pf_username"]/h1').text
    xxmap['昵称2'] = nc2
    # 关注数
    focusNum = obj.find_element_by_xpath(
        '//div[@class="PCD_counter"]/div/table/tbody/tr/td[1]//strong').text
    xxmap['关注数'] = focusNum
    # 粉丝数
    fansNum = obj.find_element_by_xpath(
        '//div[@class="PCD_counter"]/div/table/tbody/tr/td[2]//strong').text
    xxmap['粉丝数'] = fansNum
    # 发布微博数
    blogTotalNum = obj.find_element_by_xpath(
        '//div[@class="PCD_counter"]/div/table/tbody/tr/td[3]//strong').text
    xxmap['发送微博数'] = blogTotalNum
    obj.get(l)
    #基本信息模块
    try:
        xq = obj.find_elements_by_xpath('//div[@class="WB_cardwrap S_bg2"]//li[@class="li_1 clearfix"]')

        for x in xq:
            ss = x.text.replace('\n','')
            if(ss.startswith('所在地')):
                #所在地
                xxmap['所在地'] = ss.split('：')[1]
            if(ss.startswith('性别')):
                #性别
                xxmap['性别'] = ss.split('：')[1]
            if (ss.startswith('注册时间')):
                #注册时间
                xxmap['注册时间'] = ss.split('：')[1]
    except:
        xxmap['所在地'] = '非个人微博'
        xxmap['性别'] = '非个人微博'
        xxmap['注册时间'] = '非个人微博'


    # 微博等级
    level = obj.find_element_by_xpath('//div[@class="level_box S_txt2"]/a/span').text.replace('Lv.','')
    xxmap['微博等级'] = level
    # 会员等级
    try:
        hylevel = obj.find_element_by_xpath('//div[@class="pf_wrap"]/div/div[@class="pf_username"]/a/em').get_attribute("class")[-1]
    except:
        hylevel = '-1'
        pass
    xxmap['会员等级'] = hylevel
    #简介
    introduce = obj.find_element_by_xpath('//div[@class="pf_wrap"]/div/div[@class="pf_intro"]').text
    xxmap['个人简介'] = introduce
    personallist.append(xxmap)
persondf = pd.DataFrame(personallist)

df = pd.merge(blogdf,persondf,left_on='name',right_on='userName')
columns = ['发布时间','昵称','发布内容','图片','视频','发布位置','发布终端',
          '转发数','评论数','点赞数','认证','所在地','性别','注册时间',
          '关注数','粉丝数','发送微博数','微博等级','会员等级','个人简介']
df.to_csv('dd.csv',mode='a',index=None,column = columns)
print(time.time() - time1)























obj.get('https://weibo.com/ttarticle/p/show?id=2309404186781451963072')
obj.get_cookies()


print("xxxx")
try:
    element = WebDriverWait(obj, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="loginname"]'))
    )
finally:
    obj.quit()

obj.find_element_by_xpath('//*[@id="loginname"]').clear()
obj.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').clear()
obj.find_element_by_xpath('//*[@id="loginname"]').send_keys('1026198058@qq.com')
obj.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('T1026198058')
obj.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').send_keys('fzxvv')
obj.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
obj.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]').get_attribute("style")

obj.get("http://s.weibo.com/weibo/kfc?topnav=1&wvr=6&c=spr_sinamkt_buy_hyww_weibo_t113")
print(obj.page_source)
obj.save_screenshot('weibospider/common/picture/test.png')
try:
    s = obj.find_element_by_xpath("//*[@id=\"pl_weibo_direct\"]/div/div[1]/div[2]/div[2]/div[1]/dl/div/div[3]/div[1]/p")
    print(s)
except Exception:
    print("xxxxxx ")
print(obj)