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
phone_production = '4402811773'
phone_development = '4402539053'
client_username = '411671'
client_password = 'Gerbil567!'
input_origin_city = 'Lima'
input_origin_state = 'Ohio'
input_destination_city = 'North Canton'
input_destination_state = 'Ohio'
input_rate_per_mile = 4.0
list_rows_already_read = []
int_page_refreshes = 0
bool_page_sorted_by_descending = False
list_window_dimensions_heroku = [1400,1400]
list_origin_destination_rate_sets = [
    ('Lima','North Canton - Ohio', 4.0),
    ('Hudson','USA',3.0),
    ('Akron','Ohio',3.2)]


pathname_output = 'output'
filename_output = pathname_output+'/collected.txt'
if not os.path.exists(pathname_output+'/'):
    try: os.makedirs(pathname_output)
    except: pass
    file_list_all_items = open(
        filename_output,'w',encoding='utf-8',
        errors='surrogateescape')
    file_list_all_items.close()



def scroll_with_js():
    web.execute_script(
        "arguments[0].scrollIntoView(true);", web.find_element_by_xpath(
            '/html/body/div[2]/form/div/div[3]/div/div[5]/div/div[1]/div[1]/div[6]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[2]/table[2]/tbody/tr['+str(rownumber)+']'))



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



def login_heroku():
    global web
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    web = webdriver.Chrome(options=chrome_options)
    windowsize()

    web.get('https://sb1.schneider.com/execution/ictl/ui/faces/jsps/tlShipmentSearch.jspx')
    print(web.title)
    web.find_element_by_xpath(
      '//*[@id="username"]').send_keys(client_username); time.sleep(3)
    web.find_element_by_xpath(
      '//*[@id="password"]').send_keys(client_password); time.sleep(3)
    web.find_element_by_xpath('//*[@id="submit-button"]/a').click(); time.sleep(3)


def input_search_criteria():
    global textbox_origin_city, textbox_origin_postal_code, button_search
    
    def input_textbox_origin_city():
        textbox_origin_city = web.find_element_by_xpath(
            '//*[@id="pt1:r1:0:r1:0:subform:it141::content"]')
        textbox_origin_city.send_keys(Keys.CONTROL + 'a'); time.sleep(1)
        [textbox_origin_city.send_keys(Keys.BACKSPACE) for i in range(20)]
        textbox_origin_city.send_keys(input_origin_city); time.sleep(1)
        time.sleep(1)

    def input_dropdown_origin_state():
        pass
        
    def input_textbox_destination_city():
        textbox_destination_city = web.find_element_by_xpath(
            '//*[@id="pt1:r1:0:r1:0:subform:it151::content"]')
        textbox_destination_city.send_keys(input_destination_city)
        time.sleep(1)
    
    def input_dropdown_destination_state():
        dropdown_destination_state_ohio = web.find_element_by_xpath(
            '//*[@id="pt1:r1:0:r1:0:subform:soc8::content"]/option[37]')
        dropdown_destination_state_ohio.click()
        time.sleep(1)
    
    input_textbox_origin_city()
    input_dropdown_origin_state()
    input_textbox_destination_city()
    input_dropdown_destination_state()
    
    button_search = [
        i for i in web.find_elements_by_tag_name(
            'td') if 'Search' in i.get_attribute(
            'innerHTML')][-1]
    button_search.click()



def sort_by_price_descending():
    global bool_page_sorted_by_descending
    # Sort table by rate, descending
    for i in range(2):
        try:
            button_sort = [
                i for i in web.find_elements_by_class_name(
                    'x1ko') if i.text=='Estimated Total Rate Per Mile'][0]
            button_sort.click(); time.sleep(10)
        except:
            button_sort = web.find_element_by_id('pt1:r1:0:r1:1:pc1:t1:c191')
            button_sort.click(); time.sleep(10)
    bool_page_sorted_by_descending = True
    print('[ √ ] Table Sorted by Rate')

    

def activate_main_table():                
    global first_row_in_table, int_row_total, int_page_refreshes
    windowsize()

    # Making sure the results page has loaded
    while True:
        print()
        print('Activating main datatable...')
        
        try:
            int_row_total = int(web.find_element_by_id('pt1:r1:0:r1:1:pc1:ot24').text)
            if int_row_total == 0: 
                print('No Results')
                refresh_table()
                time.sleep(sleeptimer_long)
                continue            
            first_row_in_table = web.find_element_by_xpath(
             '/html/body/div[2]/form/div/div[3]/div/div[5]/div/div[1]/div[1]/div[6]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[2]/table/tbody/tr[1]')
            first_row_in_table.click()
            break
        except:
            print('Results still loading...')
            time.sleep(10)

    print('[ √ ] Results Loaded')
##    sort_by_price_descending()    

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
    print('Client-ID: '+client_username)
    print('Pickup: '+input_origin_city)
    print('Dropoff: '+input_destination_state)
    print('Minimum Rate: '+str(input_rate_per_mile))
    print('Page Refreshes: '+str(int_page_refreshes))
    print('Total Search Results: '+str(int_row_total))
    print(datetime.datetime.now())
    print()




def match_criteria_and_send_alerts():
    global list_visible_rows, rowitem, rowitem_text
    global scrollcount, rownumber, rowitem_text
    
    int_iterations_before_refresh = int(round(int_row_total/5,0))
    if int_iterations_before_refresh == 0: int_iterations_before_refresh = 1
    rownumber = 0

    for scrollcount in range(1,int_iterations_before_refresh+1):
        windowsize()
        print()
        print('Scrollcount: '+str(scrollcount)+'/'+str(int_iterations_before_refresh))

        time.sleep(2)
        list_visible_rows = web.find_elements_by_class_name('x17d')        
        for rowitem in list_visible_rows:
            rowitem_text = rowitem.text
##            save_line(rowitem_text)
            evaluate(rowitem_text)
        
        print()
        for i in range(5):
            print('keydown')
            ActionChains(web).key_down(Keys.ARROW_DOWN).perform()
            time.sleep(sleeptimer_scrolltable)




def evaluate(rowtext):
    global rate_per_mile, load_id, list_rows_already_read
    if 'ASSIGN' in rowtext: return
    if rowtext == '': return

    print()
    print(rowitem_text)
    load_id = rowtext.split('\n')[0]
    rate_per_mile = rowitem_text.split('\n')[-1].split(' ')[2]
    if load_id in list_rows_already_read: return
    list_rows_already_read.append(load_id)

    if bool_page_sorted_by_descending == True:
        if float(rate_per_mile) < input_rate_per_mile: return

    elif bool_page_sorted_by_descending == False:
        if float(rate_per_mile) > input_rate_per_mile:
            str_text_message = '-\n\nPickup: '+input_origin_city.title()+'\n'
            str_text_message += 'Dropoff: '+input_destination_city+', '+input_destination_state+'\n'
            str_text_message += 'Rate Minimum: $'+str(input_rate_per_mile)+'\n'
            str_text_message += '\nID: '+load_id + '\nRate: $' + rate_per_mile+'\n'
            str_text_message += '\nDetails:\n'+rowitem_text

            send_alert(str_text_message, phone_development)
            if int_page_refreshes > 0: send_alert(str_text_message, phone_production)



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



def send_email():
    import smtplib, ssl

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "therealjonnycraig@gmail.com"
    receiver_email = "therealjonnycraig@gmail.com"
    password = '187023aA!'
    message = """\
    Subject: Hi there
    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)



def send_alert(str_text_message, verified_twilio_phone_number):
   if str_text_message=='': return
   # Find your Account SID and Auth Token at twilio.com/console
   account_sid = 'ACd4461f4406dd2801f4b3ca39fc4ece3b'
   auth_token = '62531e8d9d3464b40e0abb13f68a6c34'
   secret = '85ECXMsQuFxkxdGw7NOEiDyDg1d0hvig'
   client = Client(account_sid, auth_token)
   message = client.messages \
       .create(
            body=str_text_message,
            from_='3862843937',
            to=verified_twilio_phone_number)
   print('[+] Alert Sent to: '+verified_twilio_phone_number)



def refresh_table():
   global int_page_refreshes, button_refresh

   button_refresh = [
       i for i in web.find_elements_by_tag_name( 'span') if 'refresh all' in i.text.lower()][0]
   button_refresh.click()
   
   int_page_refreshes += 1
   if int_page_refreshes % 100 == 0: send_alert('Refreshing Page', phone_development)
   print('Refreshing Page: '+str(int_page_refreshes))


def windowsize():
    if os.getcwd() == '/Users/darec_adirondack/Pie/Projects/Schneider Load Board':
        web.maximize_window()
    else:
        web.set_window_size(
            list_window_dimensions_heroku[0],list_window_dimensions_heroku[1])

    
def main():
    while True:
        activate_main_table()                
        match_criteria_and_send_alerts()
        refresh_table()
        time.sleep(sleeptimer_long)


if os.getcwd() == '/Users/darec_adirondack/Pie/Projects/Schneider Load Board':
    login(); time.sleep(10)
else: login_heroku(); time.sleep(10)
input_search_criteria()
main()





