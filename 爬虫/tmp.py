# -*-ccoding:utf-8 -*-
"""
Crawling pictures by selenium and urllib 
"""

import time
import re
import os
import sys
import urllib
import shutil
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains

# open phantomJs
driver = webdriver.PhantomJS(executable_path="D:\\Program Files (x86)\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
wait = ui.WebDriverWait(driver, 10)

#Download one Picture
def loadPicture(pic_url, pic_path):
    pic_name = os.path.basename(pic_url) #delete path, get the filename
    urllib.urlretrieve(pic_url, pic_path + pic_name)

#Visit the picture page and get <script>(.*?)</script>  original
def getScript(elem_url,path):
    print(elem_url)
    print(path)
    ''''' 
    #Error: Message: Error Message => 'Element does not exist in cache' 
    driver.get(elem_url) 
    pic_url = driver.find_element_by_xpath("//div[@id='wrap']/div/div[2]/a") 
    print pic_url.text 
    '''
    #By urllib to download the original pics
    count = 1
    html_content = urllib.request.urlopen(elem_url).read()
    print(html_content)
    html_content = html_content.decode("utf-8")#for solve cannot use a string pattern on a bytes-like object
    html_script = r'<script>(.*?)</script>'
    m_script = re.findall(html_script,html_content,re.S|re.M)
    # m_script = re.findall(html_script,html_content)
    for script in m_script:
        res_original = r'"original":"(.*?)"' #原图
        m_original = re.findall(res_original,script)
        for pic_url in m_original:
            loadPicture(pic_url, path)
            count = count + 1
    else:
        print('Download ' + str(count) + ' Pictures')

# Get the title of the url
def getTitle(key, url):
    try:
        # print ket,type(key)
        count = 0
        print('Function getTitle(key,url)')
        driver.get(url)
        wait.until(lambda driver:driver.find_element_by_xpath("//div[@class='masonry']/div/div[2]/a"))
        elem_title = driver.find_elements_by_xpath("//div[@class='masonry']/div/div[2]/a")
        for title in  elem_title:
            #title.text0unicode key-str=> unicode
            # print key,title.text
            elem_url = title.get_attribute("href")
            if key in title.text:
                # print key,title.text
                path = "E:\\Picture_DM\\" + title.text + "\\"
                if os.path.isfile(path):  # Delete file
                    os.remove(path)
                elif os.path.isdir(path):  # Delete dir
                    shutil.rmtree(path, True)
                os.makedirs(path)  # create the file directory
                count = count + 1
                # print elem_url
                getScript(elem_url, path)  # visit pages
    except Exception as e:
        print('Error:', e)
    finally:
        print('Find ' + str(count) + ' pages with key\n')

# Enter function
def main(key):
    # create Folder
    basePathDictory = '/res/'
    if not os.path.exists(basePathDictory):
        os.mkdir(basePathDictory)
    # input the key for search str => unicode => utf-8
    print('Ready to start the download')
    starttime = datetime.datetime.now()
    num = 1
    while num <= 73:
        url = 'http://pic.yxdown.com/list/0_0_' + str(num) + '.html'
        print('第' + str(num) + '页', 'url:' + url)
        # Determine whether the title contains key
        getTitle(key, url)
        time.sleep(2)
        num = num + 1
    else:
        print('Download Over!!!')

        # get the runtime
    endtime = datetime.datetime.now()
    print('The Running time : ', (endtime - starttime).seconds)



main("")