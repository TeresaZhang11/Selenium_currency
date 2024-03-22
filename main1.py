from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import sys
import time

currency_code = {'GBP':'英镑',
'HKD':'港币',
'USD':'美元',
'CHF':'瑞士法郎',
'SGD':'新加坡元',
'SEK':'瑞典克朗',
'DKK':'丹麦克朗',
'NOK':'挪威克朗',
'JPY':'日元',
'CAD':'加拿大元',
'AUD':'澳大利亚元',
'EUR':'欧元',
'MOP':'澳门元',
'PHP':'菲律宾比索',
'THP':'泰国铢',
'NZD':'新西兰元',
'KRW':'韩元',
'SUR':'卢布',
'MYR':'林吉特',
'TWD':'新台币',
'ESP':'西班牙比塞塔',
'ITL':'意大利里拉',
'ANG':'荷兰盾',
'BEF':'比利时法郎',
'FIM':'芬兰马克',
'IDR':'印尼卢比',
'BRL':'巴西里亚尔',
'AED':'阿联酋迪拉姆',
'INR':'印度卢比',
'ZAR':'南非兰特',
'SAR':'沙特里亚尔',
'TRY':'土耳其里拉'}

#convert YYYYMMDD to YYYY-MM-DD
#改变日期格式
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y%m%d")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format")
        sys.exit(1)

#check if command line valid
#检查命令行长度是否正确
if len(sys.argv) != 3:
    print("invalid command")
    sys.exit(1)



date_key = format_date(sys.argv[1])
currency_key = sys.argv[2]

#检查货币是否可以查询到
try:
    currency_key = currency_code[currency_key]
except:
    print("invalid currency code")
    sys.exit(1)
print(currency_key)

service = Service(excutable_path="chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://www.boc.cn/sourcedb/whpj/")

#input date 输入日期
date_input = driver.find_element(By.ID, 'erectDate')
date_input.click()
date_input.send_keys(date_key)
time.sleep(1)

#wait for calendar popup exist 等待日历弹窗
calendar = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[id="calendarPanel"]')))
close = calendar.find_element(By.ID, 'calendarClose')
close.click()

#select currency 选择货币
currency_input = driver.find_element(By.ID, "pjname")
currency_input.click()
currency_option = Select(currency_input)
currency_option.select_by_value(currency_key)
currency_input.send_keys(Keys.ENTER)

#click on search 开始搜索
button = WebDriverWait(driver, 10).until(
    #ensure select the correct search icon
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.invest_t input[type='button']"))
)
button.click()

#wait for search completion 等待搜索完成
WebDriverWait(driver, 10).until(EC.url_to_be("https://srh.bankofchina.com/search/whpj/search_cn.jsp"))

#find the 1st row we want
#找到div class = BOC_main publish -> table -> tbody -> tr class = "odd"
rows = driver.find_element(By.CSS_SELECTOR, "div.BOC_main.publish table tbody tr.odd")
columns = rows.find_elements(By.TAG_NAME, "td")
price = columns[3].text

with open("result.txt", "w") as file:
    file.write(price)

driver.quit()




