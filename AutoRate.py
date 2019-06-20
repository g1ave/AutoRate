from selenium import webdriver
from time import sleep
import threading
import concurrent.futures


def autopk(link):
    driver1 = webdriver.Chrome(executable_path='/Users/qw/Workspace/chromedriver', chrome_options=options)
    driver1.get(link)   # 因为此时还没有设置 cookies 所以还不能打开页面
    driver1.add_cookie(cookie1)
    driver1.add_cookie(cookie2)
    driver1.get(link)
    radios = driver1.find_elements_by_class_name('answer_radio')

    # print(radios)
    for i in range(0, len(radios), 5):
        sleep(3)
        try:
            radios[i].click()
        except Exception as e:
            print(e)
        finally:
            sleep(1)
            radios[i].click()

    textarea = driver1.find_elements_by_tag_name('textarea')

    for i in textarea:
        sleep(3)
        i.send_keys("老师讲得不错，没有什么意见。谢谢老师！")

    submit = driver1.find_element_by_xpath('//*[@id="r_content"]/div[2]/div/table/tbody/tr[2]/td/input[1]')
    submit.click()
    driver1.close()


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(executable_path='/Users/qw/Workspace/chromedriver', chrome_options=options)

    cookie1 = {
        'name': 'username',
        'value': '2016112678'
    }
    cookie2 = {
        'name': 'JSESSIONID',
        'value': '80F08FB617A9298A523675EAEE7FA4E7'
    }

    start_url = "http://jwc.swjtu.edu.cn/service/login.html"

    URL = "http://jwc.swjtu.edu.cn/vatuu/AssessAction?setAction=list"

    script = '''var div = document.getElementsByClassName('answerDiv'); 
                        var txtarea = document.getElementsByTagName('textarea'); 
                        for (var i = 0; i < div.length; i++){
                            div[i].style.display = 'block';
                        }
                        for (var i = 0; i < txtarea.length; i++){
                            txtarea[i].style.display = 'block';
                        }
                    '''
    # time.sleep(3)
    driver.get(start_url)
    cookies = driver.get_cookies()
    print(cookies)
    driver.add_cookie(cookie1)
    driver.add_cookie(cookie2)
    driver.get(URL)

    links = driver.find_elements_by_link_text("填写问卷")
    while links is not None:
        links = [link.get_attribute('href') for link in links]
        print(links)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            executor.map(autopk, links)

        driver.get(URL)
        links = driver.find_elements_by_link_text("填写问卷")

    driver.close()
