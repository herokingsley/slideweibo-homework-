# coding=UTF-8

import urllib
import urllib2
import cookielib
import re
import json
import base64
import rsa
import binascii
import weiboconstconfig
import SlideMyPage
import SlideSearch
import SlidePeople

class User:
    def __init__(self,username,uid):
        self.username = username
        self.uid = uid

#deal with http 3XX error
class RedirectHandler(urllib2.HTTPRedirectHandler):
    def __init__(self):
        pass

    """docstring for RedirctHandler"""
    def http_error_301(self, req, fp, code, msg, headers):
        print "abc"
        print headers["Location"]
        self.location = headers["Location"];
        return self.location

    def http_error_302(self, req, fp, code, msg, headers):
        print "redirect url: %s" % headers["Location"]
        self.location = headers["Location"];
        return self.location

#微博爬虫类
class WebWeiboSlider:

    def __init__(self):
        cj = cookielib.LWPCookieJar()
        self.cookie_support = urllib2.HTTPCookieProcessor(cj)
        httpHandler = urllib2.HTTPHandler(debuglevel = 1)
        httpsHandler = urllib2.HTTPSHandler(debuglevel = 1);
        self.opener = urllib2.build_opener(self.cookie_support,httpHandler,httpsHandler,RedirectHandler)
        self.location = ""
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
        self.header = {
            'User-Agent':user_agent,
            'Referer':'http://weibo.com/',
            'Host':'login.sina.com.cn',
        }   
		self.slideMyMainPage = None
		self.slideSearch   = None
		self.slidePeople   = None

    #获取编码后的用户名
    def getUserName(self,username):
        username = urllib.quote(username)
        u = base64.encodestring(username)
        print u
        return u

    #获取编码后的密码
    def getPwd(self,pwd, servertime, nonce,pubkey):
        #pubkey="EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443"
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey,65537)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)
        passwd = rsa.encrypt(message, key)
        passwd = binascii.b2a_hex(passwd)
        print passwd
        return passwd

    #登录
    def login(self,uname,pwd):
        data = dict(weiboconstconfig.postdata)         
        d = self.prelogin()
        user = self.getUserName(uname)
        pwd = self.getPwd(pwd,d["servertime"],d["nonce"],d["pubkey"])
        loginurl = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)'
        
        data["su"] = user
        data["sp"] = pwd
        data["rsakv"] = d["rsakv"]
        data["nonce"] = d["nonce"]
        data["servertime"] = d["servertime"]
        data = urllib.urlencode(data)
        req = urllib2.Request(loginurl,data, headers = self.header)    
        response = self.opener.open(req)    
        loginpage = response.read()   
        print loginpage
        s = "replace\(\'(.*)\'\)"
        self.header["Host"] = "passport.weibo.com"
        pattern = re.compile(s);
        ss = pattern.search(loginpage).group(1)
        print ss
        ss = urllib.unquote(ss)
        print ss
        self.header["Referer"] = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
        self.header["Pragma"] = "no-cache"
        try:
            req = urllib2.Request(ss,headers = self.header)
            response = self.opener.open(req,timeout = 10)
            self.location = response
            #page = response.read()
            #print page
        except urllib2.HTTPError,e:
            self.header["Host"] = "weibo.com" 
            print self.location
            req = urllib2.Request(self.location,headers = self.header)
            response = self.opener.open(req) 
            #获取重定向后的url
            self.location = response
            print self.location
            print str(e.code) + "hehhe"
        url = "http://www.weibo.com"
        self.header["Host"] = "www.weibo.com"
        try :
            req = urllib2.Request(url,headers = self.header)
            res =  self.opener.open(req)
            self.location = res
            self.location = "http://" + self.header["Host"] + self.location
            req = urllib2.Request(self.location,headers = self.header)
            res = self.opener.open(req)
            pp = res.read()
            print pp
   #pp = res.read()
        except urllib2.URLError,e:
            pass
    
    def prelogin(self):
        preloginurl = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1398736413824'
        try:
            req = urllib2.Request(preloginurl,data = "abc=abc",headers = self.header)    
            response = self.opener.open(req)    
            the_page = response.read()
            pattern = re.compile("\((.*)\)")
            s = pattern.search(the_page).group(1)
            d = json.loads(s)
            print d
            return d
        except urllib2.URLError,e:
            print "hehhehe"
            print e.code
            pass
    def downloadWeibo(self,page,section):
        url = "http://weibo.com/aj/mblog/fsearch?_wv=5&page=1&count=15&pre_page=1"
        req = urllib2.Request(url,headers = self.header)
        resp = self.opener.open(req)
        kk =  resp.read()
        dd = unicode(json.loads(kk))

        restr = r'<div .*?class="WB_feed_type.*?>.*?<div class="WB_screen.*?>.*?<div.*?class="WB_text.*?>.*?<div.*?class="WB_func.*?></div.*?>.*?</div>\\n\\t.*?\\t\\t\\t\\t\\n\\t'
        #restr = r"\\n"
        temp = r'<div .*?class=\"WE_feed_type.*?>.*?<div'
        weibo = re.compile(restr)
        arr = weibo.findall(dd)
        for i in arr:
            print i
            print '\n\n'
        #print weibo.group()
        #print dd
        #print len(arr)

if __name__ == "__main__":
    #usr = getUserName("ez_wzr_homework@163.com")
    #psw = getPwd("19921023",1398092882,"HK8YCF","EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443");
    weibo =  WebWeiboSlider()
    weibo.login('ez_wzr_homework@163.com','19921023')
    weibo.downloadWeibo('','')
#header["Host"] = "weibo.com"
