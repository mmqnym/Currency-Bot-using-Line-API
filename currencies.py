# -*- coding: utf-8 -*-

import re
import catch_currency_rate
import jieba
import threading
import time


currencies_name_list = []
currencies_info = {}
currencies_catched_time = ''
jieba.load_userdict('self_word_lib.txt')


def get_now_rate():
    global currencies_name_list, currencies_info, currencies_catched_time
    
    print('### bg: Start to get now rate')
    
    currencies_catched_time = catch_currency_rate.now_time()
    currencies_name_list, currencies_info = catch_currency_rate.now_all() # get current rate
    
    print('### bg: Succeeded in getting now rate')
    timer = threading.Timer(7200, get_now_rate)
    timer.start()
    
threading.Timer(0, get_now_rate).start() # start auto run
time.sleep(2)

def is_number(num):
  pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
  result = pattern.match(num)
  
  if result:
      return True
  else:
      return False

def replace_synonym(in_str):
    
    combine_dict = {}
    
    for line in open('self_exchangeword_lib.txt', \
                     'r', encoding = 'utf-8'):
        seperate_word = line.strip().split(' ')
        num = len(seperate_word)
        
        for i in range(1, num):
             combine_dict[seperate_word[i]] = seperate_word[0]
             
    
    seg_list = jieba.cut(in_str, cut_all = False)
    
    cut_str = ",".join(seg_list).encode('utf-8')
    cut_str = cut_str.decode('utf-8')
    print(cut_str)
    
    token_msg = ""
    
    for word in cut_str.split(','):
       if word in combine_dict:
           word = combine_dict[word]
           token_msg += word
       else:
           token_msg += word
       
       token_msg += ' '
           
    
    return token_msg.rstrip().split(' ')
 
 
def calculate_rate(value, currency_name, other_currency_name):
    
    global currencies_name_list, currencies_info, currencies_catched_time
    
    print('### start: Change rate log ###')
    print(value)
    print(currency_name)
    print(other_currency_name)
    print('### end: Change rate log ###')
    
    found = False
    msg = ''

    # convert foreign currency to TWD
    for i in range(len(currencies_name_list)):
        if currency_name == currencies_name_list[i] \
            and currency_name != 'ZAR': # not support
            found = True
            value *= float(currencies_info[currency_name][0])
            msg = '匯率擷取時間: ' + currencies_catched_time + '\n'
            break
        
        elif currency_name == 'TWD':
            found = True
            msg = '匯率擷取時間: ' + currencies_catched_time + '\n'
            break
        
        else:
            found = False
            
    
    if found:
        msg += ('醬子是" %.2f "台幣唷!'%value)
        if other_currency_name == None:
            return msg
        
    else:
        msg = '您選擇的貨幣『 ' + currency_name + ' 』不在我的支援範圍內唷 (ಥ_ಥ)' 
        return msg

    # if get 3rd argument, convert TWD result to a foreign currency
    msg = '' # reset msg
    found = False
    
    for i in range(len(currencies_name_list)):
        if other_currency_name == currencies_name_list[i] \
            and other_currency_name != 'ZAR': # not support
            found = True
            value /= float(currencies_info[other_currency_name][1])
            msg = '匯率擷取時間: ' + currencies_catched_time + '\n'
            
            break
        
        elif other_currency_name == 'TWD':
            found = True
            msg = '匯率擷取時間: ' + currencies_catched_time
            break
        
        else:
            found = False
    
    if found:
        msg += ('醬子是" %.2f "美金唷!'%value)
       
        if currency_name == other_currency_name and \
           currency_name != '':
            msg += '\n\n!!邪惡的匯差誕生囉~\n明明提醒過你的٩(ŏ﹏ŏ、)۶'
        
    else:
        msg = '您選擇的貨幣『 ' + other_currency_name + ' 』不在我的支援範圍內唷 (ಥ_ಥ)' 


    return msg

def judge_to_add(cut_token_list):
    
    if '+' not in cut_token_list[1]:
        return cut_token_list 
        
    if cut_token_list[-1] == '=' and cut_token_list[-3] == '+':
        del cut_token_list[-3]
    
    if cut_token_list[-1] == '$' and cut_token_list[-4] == '+':
        del cut_token_list[-4]
    
    total = 0.0
    
    i = 0
    
    for i in range(len(cut_token_list)):
        if is_number(cut_token_list[i]):
            total += float(cut_token_list[i])
            
            if cut_token_list[i+1] != '+':
                break
        
                    
    renew_list = []
    renew_list.append(str(total))
    
    if cut_token_list[-1] == '=':
        
        while cut_token_list[i] != '=':
            renew_list.append(str(cut_token_list[i+1]))
            i += 1
    
    if cut_token_list[-1] == '$':
        while cut_token_list[i] != '$':
            renew_list.append(str(cut_token_list[i+1]))
            i += 1
    
    print('### log:new list:', end = '')
    print(renew_list)
    
    return renew_list


''' using way
msg_token_list = replace_synonym('500澳幣=')
msg_token_list = judge_to_add(msg_token_list)
'''



