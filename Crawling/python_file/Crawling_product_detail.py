from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd


#---------------- xpath가 존재하는지 확인 ---------------------
def isExistXpath(xpath, implicitly_wait_time=0, old_wait=25):
    driver.implicitly_wait(implicitly_wait_time)
    try:
        driver.find_element(By.XPATH, xpath)
    except Exception:
        return False
    finally:
        driver.implicitly_wait(old_wait)
    return True

#---------------- 전체 페이지 확인 ---------------------
def chech_total_page():
    num = 0
    page_break = True
    
    while 1:
        if num == 0:
            if isExistXpath('//*[@id="productListArea"]/div[5]/div/a'):
                driver.find_element(By.XPATH,'//*[@id="productListArea"]/div[5]/div/a').click()
                time.sleep(1)
                num += 10
            else:
                for i in reversed(range(11)):
                    page_xpath = '//*[@id="productListArea"]/div[5]/div/div/a[' + str(i+1) + ']'
                    if isExistXpath(page_xpath):
                        page = i+1
                        break
                else:
                    continue
                break
        else:
            if isExistXpath('//*[@id="productListArea"]/div[4]/div/a[2]'):
                driver.find_element(By.XPATH,'//*[@id="productListArea"]/div[4]/div/a[2]').click()
                time.sleep(1)
                num += 10
            else:
                for i in reversed(range(11)):
                    page_xpath = '//*[@id="productListArea"]/div[4]/div/div/a[' + str(i+1) + ']'
                    if isExistXpath(page_xpath):
                        page = i+1
                        break
                else:
                    continue
                break

    return page + num

#---------------- 핸드폰 크롤링 ---------------------
def phone_Crawling(driver):
    url = 'https://prod.danawa.com/list/?cate=12215709'  #핸드폰 자급제
    driver.get(url)
    curPage = 1  #시작 페이지
    total_page = chech_total_page()  #총 페이지

    prod_detail_total = []

    print('----- Phone Crawling Start ------')
    
    while curPage <= total_page:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        prod_items = soup.select('li.prod_item.prod_layer')
        print('----- Current Page : {}'.format(curPage), '------')

        prod_item_list = get_phone_items(prod_items)
        prod_detail_total.append(prod_item_list)

        curPage += 1

        if curPage > total_page:
            print('Crawling succeed!\n')
            print()
            break

        cur_css = 'div.number_wrap > a:nth-child({})'.format(curPage)
        WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR,cur_css))).click()    #페이지 넘기기

        del soup
        time.sleep(3)
    
    driver.close()

    total = []
    for temp in prod_detail_total:
        total += temp
    prod_detail_total = total

    data = pd.DataFrame(prod_detail_total)
    data.columns = ['Category','Product_name', 'model_name','company_name', '출시OS', '화면크기' ,'화면정보', '시스템', '램', '내장메모리', '통신', '카메라', '사운드', '보안/기능', '배터리', '규격', '이미지']
    data = data.drop_duplicates(subset='Product_ID', keep='first')
    
    data.to_excel('./file/danawa_crawling_phone_detail_result_class.xlsx', index =False)
    
    
#---------------- 핸드폰 컨텐츠 크롤링 ---------------------
def get_phone_items(prod_items):    
    prod_data = []
    
    for prod_item in prod_items:
        try:  #상품명, 기업명 크롤링
            product_name = prod_item.select('p.prod_name > a')[0].text.strip()
            product_name = product_name.replace(", 자급제", "").replace(", 공기계", "").replace("글로벌", "").replace("5G","").replace("LTE", "")
            product_name_list = product_name.split()
            company_name = product_name_list[0]
            del product_name_list[0]
            product_name = ' '.join(product_name_list)
        except:
            product_name = ""
        
        try:  #모델명 크롤링
            model_name = prod_item.select('span.cm_mark')[0].text.strip()
            model_name_list = model_name.split(':')
            del model_name_list[0]
            model_name = ''.join(model_name_list)
        except:
            model_name = ""

        try:  #상품 크롤링
            product_list = prod_item.select('div.spec_list')[0].text.strip()
            product_list = product_list.replace('보안/기능', '보안 및 기능')
            product_detail_list = product_list.split('/')

            release_os = ''
            screen_info = ''
            screen_size = ''
            system = ''
            ram = ''
            mem = ''
            connect = ''
            camera = ''
            sound = ''
            function = ''
            battery = ''
            size = ''
            
            for i in range(len(product_detail_list)):
                if '출시OS' in product_detail_list[i]:
                    idx_os = i
                elif '화면정보' in product_detail_list[i]:
                    idx_scr = i
                elif '시스템' in product_detail_list[i]:
                    idx_sys = i
                elif '통신' in product_detail_list[i]:
                    idx_conn = i
                elif '카메라' in product_detail_list[i]:
                    idx_cam = i
                elif '사운드' in product_detail_list[i]:
                    idx_sound = i
                elif '보안 및 기능' in product_detail_list[i]:
                    idx_func = i
                elif '배터리' in product_detail_list[i]:
                    idx_bat = i
                elif '규격' in product_detail_list[i]:
                    idx_size = i
        
            release_os_list = product_detail_list[idx_os]
            release_os = ''.join(release_os_list)
            release_os = release_os.replace(' 출시OS: ','').replace(' ', '')
        
            screen_info_list = product_detail_list[idx_scr:idx_sys]
            screen_info = ''.join(screen_info_list)
            screen_info = screen_info.replace(' 화면정보 ','').replace('  ', '/ ')
            
            screen_size = ''.join(screen_info_list[0])
            screen_size_list = screen_size.split('(')
            screen_size = ''.join(screen_size_list[1])
            screen_size = screen_size.replace(') ','')
            
            screen_list = screen_info.split("cm")
            screen_list = screen_list[0]
            
            
            system_list = product_detail_list[idx_sys:idx_conn]
            ram_list = []
            mem_list = []
            
            for j in system_list:
                if '램' in j:
                    ram_list += j
                    system_list.remove(j)
            for k in system_list:
                if '내장' in k:
                    mem_list += k
                    system_list.remove(k)
                    
            system = ''.join(system_list)
            ram = ''.join(ram_list)
            mem = ''.join(mem_list)
            system = system.replace(' 시스템 ','').replace('  ', '/ ')
            ram = ram.replace('램:', '')
            mem = mem.replace('내장:', '')
            
            connect_list = product_detail_list[idx_conn:idx_cam]
            connect = ''.join(connect_list)
            connect = connect.replace(' 통신 ','').replace('  ', '/ ')
        
            camera_list = product_detail_list[idx_cam:idx_sound]
            camera = ''.join(camera_list)
            camera = camera.replace(' 카메라 ','').replace('  ', '/ ')
        
            sound_list = product_detail_list[idx_sound:idx_func]
            sound = ''.join(sound_list)
            sound = sound.replace(' 사운드 ','').replace('  ', '/ ')
        
            function_list = product_detail_list[idx_func:idx_bat]
            function = ''.join(function_list)
            function = function.replace(' 보안 및 기능 ','').replace('  ', '/ ')
        
            battery_list = product_detail_list[idx_bat:idx_size]
            battery = ''.join(battery_list)
            battery = battery.replace(' 배터리 ','').replace('  ', '/ ')

            size_list = product_detail_list[idx_size:]
            del_num = size_list.index("벤치마크")
            del size_list[del_num:]
            size = ''.join(size_list)
            size = size.replace(' 규격 ','').replace('  ', '/ ')

        except:
            size_list = product_detail_list[idx_size:]
            size = ''.join(size_list)
            size = size.replace(' 규격 ','').replace('  ', '/ ')
            

        try:
            img_link = 'http:' + prod_item.select_one('div.thumb_image > a > img').get('data-original')
        except:
            img_link = 'http:' + prod_item.select_one('div.thumb_image > a > img').get('src')
        if product_name:
            mylist = [1, product_name, model_name, company_name, release_os, screen_size, screen_info, system, ram, mem, connect, camera, sound, function, battery, size, img_link]
            
        if mylist[0]:
            prod_data.append(mylist)

    return(prod_data)


#---------------- 태블릿 크롤링 ---------------------
def tablet_Crawling(driver):
    url = 'https://prod.danawa.com/list/?cate=12210596'  #태블릿
    driver.get(url)

    total_page = chech_total_page()  #총 페이지

    total_next_page = total_page // 10
    last_page = total_page - total_next_page * 10
    curPage = 1  #시작 페이지
    num = 0 #page의 10의자리

    url = 'https://prod.danawa.com/list/?cate=12210596'  #처음으로_방법찾으면 바꿀 예정
    driver.get(url)

    prod_detail_total = []
    
    print('----- Tablet Crawling Start ------')
    
    while curPage <= total_page:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        prod_items = soup.select('li.prod_item.prod_layer')
        print('----- Current Page : {}'.format(curPage), '------')

        prod_item_list = get_tablet_items(prod_items)
        prod_detail_total.append(prod_item_list)

        curPage += 1

        if curPage > total_page:
            print('Crawling succeed!')
            break
        
        if curPage % 10 == 1:
            if num == 0:
                cur_css = '#productListArea > div.prod_num_nav > div > a'
            else:
                cur_css = '#productListArea > div.prod_num_nav > div > a.edge_nav.nav_next'
            num += 10
        else:
            cur_css = 'div.number_wrap > a:nth-child({})'.format(curPage-num)
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,cur_css))).click()    #페이지 넘기기
        
        del soup
        time.sleep(3)

    driver.close()

    total = []
    for temp in prod_detail_total:
        total += temp
    prod_detail_total = total

    data = pd.DataFrame(prod_detail_total)
    data.columns = ['Category', 'Product_name', 'model_name', 'company_name', '출시OS', '화면정보', '프로세서', '램', '내장메모리', '통신', '카메라', '사운드', '악세서리', '배터리', '규격', '이미지']
    data = data.drop_duplicates(subset='Product_ID', keep='first')
    data.to_excel('./file/danawa_crawling_tablit_detail_result_class.xlsx', index =False)


#---------------- 태블릿 컨텐츠 크롤링 ---------------------
def get_tablet_items(prod_items):    
    prod_data = []
    
    for prod_item in prod_items:
    
        #상품명, 제조사 크롤링
        try:  
            product_name = prod_item.select('p.prod_name > a')[0].text.strip()            
            product_name_list = product_name.split()
            company_name = product_name_list[0]
            del product_name_list[0]
                
            product_name = ' '.join(product_name_list)
        except:
            product_name = ""
            company_name = ""
        
        try:
            product_list = prod_item.select('div.spec_list')[0].text.strip()
            product_type_detail_list = product_list.split('/')
            product_type_list = product_type_detail_list[0]
            product_type = ''.join(product_type_list)
            product_type = product_type.replace(' ', '')
        except:
            product_type = ''
        
        #상품 모델명 크롤링
        try:
            model_name = prod_item.select('span.cm_mark')[0].text.strip()
            model_name_list = model_name.split(':')
            del model_name_list[0]
            model_name = ''.join(model_name_list)
        except:
            model_name = ""
    
        #상품 크롤링
        try:  
            product_list = prod_item.select('div.spec_list')[0].text.strip()
            product_list = product_list.replace('스피커/단자', '스피커 및 단자')
            product_detail_list = product_list.split('/')
            idx = 10
    
            release_os = ''
            screen_info = ''
            system = ''
            ram = ''
            mem = ''
            connect = ''
            camera = ''
            sound = ''
            accessory = ''
            battery = ''
            size = ''
            bench_mark = ''
    
            release_os_list = []
            screen_info_list = []
            system_list = []
            ram_list = []
            mem_list = []
            connect_list = []
            camera_list = []
            sound_list = []
            accessory_list = []
            battery_list = []
            size_list = []            
    
            for i in product_detail_list:
                if '출시OS' in i:
                    idx = 0
                elif '화면정보' in i:
                    idx = 1
                elif '시스템' in i:
                    idx = 2
                elif '네트워크' in i:
                    idx = 3
                elif '카메라' in i:
                    idx = 4
                elif '사운드' in i:
                    idx = 5
                elif '액세서리' in i:
                    idx = 6
                elif '배터리' in i:
                    idx = 7
                elif '규격' in i:
                    idx = 8
                elif '모델명' in i:
                    idx = 10
                elif '중국 출시가' in i:
                    idx = 10
                    
                if idx == 0:
                    release_os_list.append(i)
                elif idx == 1:
                    screen_info_list.append(i)
                elif idx == 2:
                    system_list.append(i)
                elif idx == 3:
                    connect_list.append(i)
                elif idx == 4:
                    camera_list.append(i)
                elif idx == 5:
                    sound_list.append(i)
                elif idx == 6:
                    accessory_list.append(i)
                elif idx == 7:
                    battery_list.append(i)
                elif idx == 8:
                    size_list.append(i)
                
            if release_os_list:
                release_os = ''.join(release_os_list[0])
                release_os = release_os.replace('출시OS:','').replace(' ', '')
            
            if screen_info_list:
                screen_info = ''.join(screen_info_list)
                screen_info = screen_info.replace(' 화면정보 ','').replace('  ', '/ ')

            if system_list:
                system = ''.join(system_list)
                system = system.replace(' 시스템 ','').replace('  ', '/ ')
        
                for sys in system_list:
                    if '램' in sys:
                        ram = ''.join(sys)
                        if '시스템' in sys:
                            ram = ram.replace(' 시스템 ','')
                    elif '내장' in sys:
                        mem = ''.join(sys)
                ram = ram.replace(' 램:', '').replace(' ', '')
                mem = mem.replace(' 내장:', '').replace(' ', '')
        
            if connect_list:
                connect = ''.join(connect_list)
                connect_list = connect.split('네트워크 ')
                del connect_list[0]
                connect = ''.join(connect_list)
                connect = connect.replace('  ', '/ ')

            if camera_list:
                camera = ''.join(camera_list)
                camera = camera.replace(' 카메라 ','').replace('  ', '/ ')
        
            if sound_list:
                sound = ''.join(sound_list)
                sound = sound.replace(' 사운드 ','').replace('  ', '/ ')
            
            if accessory_list:
                accessory = ''.join(accessory_list)
                accessory = accessory.replace(' 액세서리','').replace('  ', '/ ')
            
            if battery_list:
                if '규격' in battery_list[0]:
                    size = ''.join(battery_list)
                    size = size.replace(' 배터리 ','').replace('  ', '/ ').replace(' 규격 ','')
                else: 
                    battery = ''.join(battery_list)
                    battery = battery.replace(' 배터리 ','').replace('  ', '/ ')
                    
                    if size_list:
                        size = ''.join(size_list)
                        size = size.replace(' 규격 ','').replace('  ', '/ ')
    
        except:
            release_os = ''
            screen_info = ''
            system = ''
            ram = ''
            mem = ''
            connect = ''
            camera = ''
            sound = ''
            accessory = ''
            battery = ''
            size = ''
            bench_mark = ''
    
        try:
            img_link = 'http:' + prod_item.select_one('div.thumb_image > a > img').get('data-original')
        except:
            img_link = 'http:' + prod_item.select_one('div.thumb_image > a > img').get('src')

        if model_name in product_name:
            product_name = product_name.replace(model_name, '')
        if '램' in product_name:
            product_name = product_name.replace(ram, '').replace(', 램', '')
            
        mylist = [2, product_name, model_name, company_name, release_os, screen_info, system, ram, mem, connect, camera, sound, accessory , battery, size, img_link]
            
        if mylist[1]:
            if '태블릿PC' in product_type:
                if '중고' not in product_name:
                    if  '키즈' not in product_name:
                        if  '패키지' not in product_name:
                            if '완납' not in product_name:
                                if '비즈니스' not in product_name:
                                    prod_data.append(mylist)

    return(prod_data)

#---------------- 노트북 크롤링 ---------------------
def laptop_Crawling(driver):
    url = 'https://prod.danawa.com/list/?cate=112758&15main_11_02'  #노트북 전체
    driver.get(url)
    curPage = 1  #시작 페이지
    #total_page = chech_total_page()  #총 페이지
    total_page = 10

    prod_detail_total = []

    print('----- Laptop Crawling Start ------')
    
    while curPage <= total_page:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        prod_items = soup.select('li.prod_item.prod_layer')
        print('----- Current Page : {}'.format(curPage), '------')

        prod_item_list = get_laptop_items(prod_items)
        prod_detail_total.append(prod_item_list)

        curPage += 1

        if curPage > total_page:
            print('Crawling succeed!\n')
            print()
            break

        cur_css = 'div.number_wrap > a:nth-child({})'.format(curPage)
        WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR,cur_css))).click()    #페이지 넘기기

        del soup
        time.sleep(3)
    
    driver.close()

    total = []
    for temp in prod_detail_total:
        total += temp
    prod_detail_total = total

    data = pd.DataFrame(prod_detail_total)
    data.columns = ['Category','Product_name', 'model_name','company_name', 'os', '화면정보', '화면크기', 'CPU', '램', '그래픽', '저장장치', '네트워크', '영상입출력', '단자', '부가기능', '입력장치', '파워', '주요재원', '이미지']
    data = data.drop_duplicates(subset='model_name', keep='first')
    
    data.to_excel('./file/danawa_crawling_laptop_detail_result_class.xlsx', index =False)

#---------------- 노트북 컨텐츠 크롤링 ---------------------
def get_laptop_items(prod_items):    
    prod_data = []
    
    for prod_item in prod_items:
        try:
            product_list = prod_item.select('div.spec_list')[0].text.strip()
            product_type_detail_list = product_list.split('/')
            product_type_list = product_type_detail_list[0]
            product_type = ''.join(product_type_list)
            product_type = product_type.replace(' ', '')
        except:
            product_type = ''

        try:  #상품명, 기업명 크롤링
            product_name = prod_item.select('p.prod_name > a')[0].text.strip()
            #product_name = product_name.replace(", 자급제", "").replace(", 공기계", "").replace("글로벌", "").replace("5G","").replace("LTE", "")
            product_name_list = product_name.split()
            company_name = product_name_list[0]
            model_name = ''
            del product_name_list[0]
            
            for word in reversed(product_name_list):
                if '램' in word:
                    product_name_list.remove(word)
                elif 'WIN' in word:
                    product_name_list.remove(word)
                elif word == '4070':
                    product_name_list.remove(word)
                elif word == '4060':
                    product_name_list.remove(word)
                elif word == '4080':
                    product_name_list.remove(word)
                elif word == '3060':
                    product_name_list.remove(word)
                elif word == 'OLED':
                    product_name_list.remove(word)
                elif word == 'QHD':
                    product_name_list.remove(word)  
                elif word == 'R5':
                    product_name_list.remove(word)
                elif word == '4050':
                    product_name_list.remove(word)
                elif word == '내장그래픽':
                    product_name_list.remove(word)
                elif word == '외장그래픽':
                    product_name_list.remove(word)
                elif word == 'W11':
                    product_name_list.remove(word)
                elif word == '5D':
                    product_name_list.remove(word)
                elif word == 'Plus':
                    product_name_list.remove(word)
                elif word == '4K':
                    product_name_list.remove(word)
                elif word == 'Mini':
                    product_name_list.remove(word)
                elif word == 'LED':
                    product_name_list.remove(word)
                elif word == 'PRO':
                    product_name_list.remove(word)
                elif word == 'I7' or word == 'i7':
                    product_name_list.remove(word)
                elif word == 'I9' or word == 'i9':
                    product_name_list.remove(word)
                elif word == 'I5' or word == 'i5':
                    product_name_list.remove(word)
                elif word == '블랙':
                    product_name_list.remove(word)
                elif word == '블루':
                    product_name_list.remove(word)
                elif word == '그레이':
                    product_name_list.remove(word)
                elif word == '화이트':
                    product_name_list.remove(word)
                elif word == '베이직':
                    product_name_list.remove(word)
                elif word == '스타':
                    product_name_list.remove(word)
                elif word == '카본':
                    product_name_list.remove(word)
                elif word == '3050Ti':
                    product_name_list.remove(word)
                else:
                    break
                
            model_name = ''.join(product_name_list[-1])
            del product_name_list[-1]
            product_name = ' '.join(product_name_list)

        except:
            product_name = ""
            model_name = ''
            company_name = ''
        
        product_list = prod_item.select('div.spec_list')[0].text.strip()
        product_detail_list = product_list.split('/')
        release_os = ''
        screen_info = ''
        screen_size = ''
        cpu_info = ''
        ram_info = ''
        graphic_info = ''
        memory_info = ''
        network_info = ''
        image_IO_info = ''
        terminal_info = ''
        add_function_info = ''
        input_info = ''
        power_info = ''
        spec_info = ''
        
        idx = 0

        release_os_list = []
        screen_info_list = []
        screen_size_list = []
        cpu_info_list = []
        ram_info_list = []
        graphic_info_list = []
        memory_info_list = []
        network_info_list = []
        image_IO_info_list = []
        terminal_info_list = []
        add_function_info_list = []
        input_info_list = []
        power_info_list = []
        spec_info_list = []

        for i in range(len(product_detail_list)):
            if '운영체제' in product_detail_list[i]:
                idx = 1
            elif '화면정보' in product_detail_list[i]:
                idx = 2
            elif 'CPU' in product_detail_list[i]:
                idx = 3
            elif '램' in product_detail_list[i]:
                idx = 4
            elif '그래픽' in product_detail_list[i]:
                idx = 5
            elif '저장장치' in product_detail_list[i]:
                idx = 6
            elif '네트워크' in product_detail_list[i]:
                idx = 7
            elif '영상입출력' in product_detail_list[i]:
                idx = 8
            elif '단자 ' in product_detail_list[i]:
                idx = 9
            elif '부가기능' in product_detail_list[i]:
                idx = 10
            elif '입력장치' in product_detail_list[i]:
                idx = 11
            elif '파워' in product_detail_list[i]:
                idx = 12
            elif '주요제원' in product_detail_list[i]:
                idx = 13
            
            if idx == 1:
                release_os_list.append(product_detail_list[i])
            elif idx == 2:
                screen_info_list.append(product_detail_list[i])
            elif idx == 3:
                cpu_info_list.append(product_detail_list[i])
            elif idx == 4:
                ram_info_list.append(product_detail_list[i])
            elif idx == 5:
                graphic_info_list.append(product_detail_list[i])
            elif idx == 6:
                memory_info_list.append(product_detail_list[i])
            elif idx == 7:
                network_info_list.append(product_detail_list[i])
            elif idx == 8:
                image_IO_info_list.append(product_detail_list[i])
            elif idx == 9:
                terminal_info_list.append(product_detail_list[i])
            elif idx == 10:
                add_function_info_list.append(product_detail_list[i])
            elif idx == 11:
                input_info_list.append(product_detail_list[i])
            elif idx == 12:
                power_info_list.append(product_detail_list[i])
            elif idx == 13:
                spec_info_list.append(product_detail_list[i])

        try:
            release_os = ''.join(release_os_list)
            release_os = release_os.replace(' 운영체제(OS): ','').replace(' ', '')
        except:
            release_os = ''
        
        try:
            screen_info = ''.join(screen_info_list)
            screen_info = screen_info.replace(' 화면정보 ','').replace('  ', '/ ')

            screen_size = ''.join(screen_info_list[0])
            screen_size_list = screen_size.split('(')
            screen_size = ''.join(screen_size_list[1])
            screen_size = screen_size.replace(') ','')
            
            screen_list = screen_info.split("cm")
            screen_list = screen_list[0]
        except:
            screen_info = ''
            screen_size = ''
        
        try:
            cpu_info = ''.join(cpu_info_list)
            cpu_info = cpu_info.replace(' CPU ','').replace('  ', '/ ')
        except:
            cpu_info = ''
        
        try:
            ram_info = ''.join(ram_info_list)
            ram_info = ram_info.replace(' 램 ','').replace('  ', '/ ')
        except:
            ram_info = ''
        
        try:
            graphic_info = ''.join(graphic_info_list)
            graphic_info = graphic_info.replace(' 그래픽 ','').replace('  ', '/ ')
        except:
            graphic_info = ''
        
        try:
            memory_info = ''.join(memory_info_list)
            memory_info = memory_info.replace(' 저장장치 ','').replace('  ', '/ ')
        except:
            memory_info = ''
        
        try:
            network_info = ''.join(network_info_list)
            network_info = network_info.replace(' 네트워크 ','').replace('  ', '/ ')
        except:
            network_info = ''
        
        try:
            image_IO_info = ''.join(image_IO_info_list)
            image_IO_info = image_IO_info.replace(' 영상입출력 ','').replace('  ', '/ ')
        except:
            image_IO_info = ''
        
        try:
            terminal_info = ''.join(terminal_info_list)
            terminal_info = terminal_info.replace(' 단자 ','').replace('  ', '/ ')
        except:
            terminal_info = ''
        
        try:
            add_function_info = ''.join(add_function_info_list)
            add_function_info = add_function_info.replace(' 부가기능 ','').replace('  ', '/ ')
        except:
            add_function_info = ''
        
        try:
            input_info = ''.join(input_info_list)
            input_info = input_info.replace(' 입력장치 ','').replace('  ', '/ ')
        except:
            input_info = ''
        
        try:
            power_info = ''.join(power_info_list)
            power_info = power_info.replace(' 파워 ','').replace('  ', '/ ')
        except:
            power_info = ''
        
        try:
            spec_info = ''.join(spec_info_list)
            spec_info = spec_info.replace(' 주요재원 ','').replace('  ', '/ ')
        except:
            spec_info = ''

        try: 
            img_link = 'http:' + prod_item.select_one('div.thumb_image > a > img').get('data-original')
        except:
            img_link = 'http:' + prod_item.select_one('div.thumb_image > a > img').get('src')
 
        if product_name:
            if '노트북' in product_type:
                mylist = [3, product_name, model_name, company_name, release_os, screen_info, screen_size, cpu_info, ram_info, graphic_info, memory_info, network_info, image_IO_info, terminal_info, add_function_info, input_info, power_info, spec_info, img_link]
                prod_data.append(mylist)

    return(prod_data)

#---------------- 검색 ---------------------
 
options = Options()
options.add_argument('headless'); # headless는 화면이나 페이지 이동을 표시하지 않고 동작하는 모드

chromedriver_autoinstaller.install()
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
driver.set_window_size(1920,1280)

#---------------- 핸드폰 크롤링 ---------------------
phone_Crawling(driver)


#---------------- 크롤링 재시작 ---------------------
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
driver.set_window_size(1920,1280)

#---------------- 태블릿 크롤링 ---------------------
tablet_Crawling(driver)

#---------------- 크롤링 재시작 ---------------------
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
driver.set_window_size(1920,1280)

#---------------- 노트북 크롤링 ---------------------
laptop_Crawling(driver)
