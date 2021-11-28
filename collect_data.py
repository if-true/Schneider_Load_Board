from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pickle
import time
import traceback
import os
from twilio.rest import Client
import datetime
from selenium.webdriver.common.action_chains import ActionChains


sleeptimer_long = 60*2
sleeptimer_scrolltable = 1
client_username = '411671'
client_password = 'Gerbil567!'
int_page_refreshes = 0


pathname_output = 'output'
filename_output = pathname_output+'/collected.txt'
if not os.path.exists(pathname_output+'/'):
    try: os.makedirs(pathname_output)
    except: pass
    file_list_all_items = open(
        filename_output,'w',encoding='utf-8',
        errors='surrogateescape')
    file_list_all_items.close()



def login():
   global web
   web = webdriver.Chrome('../support/chromedriver.exe')
   windowsize()
   web.get('https://sb1.schneider.com/execution/ictl/ui/faces/jsps/tlShipmentSearch.jspx')

   web.find_element_by_xpath(
      '//*[@id="username"]').send_keys(client_username); time.sleep(3)
   web.find_element_by_xpath(
      '//*[@id="password"]').send_keys(client_password); time.sleep(3)
   web.find_element_by_xpath('//*[@id="submit-button"]/a').click(); time.sleep(3)



def input_search_criteria():
    input('manually enter search criteria. press enter to continue.')

    

def activate_main_table():                
    global first_row_in_table, int_row_total, int_page_refreshes
    windowsize()

    # Making sure the results page has loaded
    while True:
        try:
            first_row_in_table = web.find_element_by_xpath(
             '/html/body/div[2]/form/div/div[3]/div/div[5]/div/div[1]/div[1]/div[6]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[2]/table/tbody/tr[1]')
            first_row_in_table.click()
            break
        except:
            print('Results still loading...')
            time.sleep(10)

    print('[ √ ] Results Loaded')
    int_row_total = int(web.find_element_by_id(
        'pt1:r1:0:r1:1:pc1:ot24').text)

    # Activating the table for scrolling
    first_row_in_table = web.find_element_by_xpath(
     '/html/body/div[2]/form/div/div[3]/div/div[5]/div/div[1]/div[1]/div[6]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[2]/table/tbody/tr[1]')
    first_row_in_table.click()
    print('[ √ ] Table Activated')

    for i in range(4):
        print('keydown')
        ActionChains(web).key_down(Keys.ARROW_DOWN).perform()
        time.sleep(sleeptimer_scrolltable)
            
    print() 
    print('_____________________')
    print(datetime.datetime.now())
    print()




def match_criteria_and_send_alerts():
    global list_visible_rows, rowitem, rowtext, str_text_message, rowitem_html
    global rate_per_mile, load_id, scrollcount, rownumber, rowitem, rowitem_text
    global list_all_rows

    int_iterations_before_refresh = int(round(int_row_total/5,0))+2
    rownumber = 0

    for scrollcount in range(int_iterations_before_refresh):
        windowsize()
        time.sleep(3)
        print()
        print('Scrollcount: '+str(scrollcount)+'/'+str(int_iterations_before_refresh))
        
        list_visible_rows = [i for i in web.find_elements_by_class_name('x17d')]
        
        for rowitem in list_visible_rows:
            try: rowitem_text = rowitem.text
            except:
                time.sleep(5);
                print('missed')
                continue
            if 'ASSIGN' in rowitem_text: continue
            if rowitem_text == '': continue
            
            print()
            print(rowitem_text)
            save_line(rowitem_text)
        
        print()
        for i in range(5):
            print('keydown')
            ActionChains(web).key_down(Keys.ARROW_DOWN).perform()
            time.sleep(sleeptimer_scrolltable)



def save_line(line):
    global list_all_items, file_list_all_items
    line = line.lower().replace('\n','\t')
    list_all_items = [
        i.strip() for i in open(filename_output).readlines()]
    if line in list_all_items: return

    file_list_all_items = open(
        filename_output,'a',encoding='utf-8',
        errors='surrogateescape')
    file_list_all_items.write(line+'\n')
    file_list_all_items.close()




def refresh_table():
   global int_page_refreshes, button_refresh

   print('Refreshing page')
   button_refresh = [
       i for i in web.find_elements_by_tag_name(
           'span') if 'refresh all' in i.text.lower()][0]
   button_refresh.click()
   int_page_refreshes += 1
   send_alert('Refreshing Page', phone_development)



def windowsize():
    if os.getcwd() == '/Users/darec_adirondack/Pie/Projects/Schneider Load Board':
        web.maximize_window()
    else:
        web.set_window_size(1200,1200)


    
def main():
    while True:
        activate_main_table()                
        match_criteria_and_send_alerts()
        refresh_table()
        time.sleep(sleeptimer_long)


login(); time.sleep(10)
input_search_criteria()
main()





