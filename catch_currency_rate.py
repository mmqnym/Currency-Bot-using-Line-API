import pandas as pd
import localtime

def now_time():
    return localtime.get()
    
def now_all():
    cur_time = now_time()
    dfs = pd.read_html(r'https://rate.bot.com.tw/xrt?Lang=zh-TW')
    currency = dfs[0].iloc[:,0:3]
    currency.columns = [u'幣別', u'買入', u'賣出']
    currency[u'幣別'] = currency[u'幣別'].str.extract('\((\w+)\)')
    name_list = currency.iloc[:,0:1]
    name_list = name_list.to_dict('list')['幣別']
    
    return name_list, currency.set_index(u'幣別').T.to_dict('list')

print(now_time())