from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

import currencies #for currencies exchange function
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # if got a massage
            
                print('### message get log ###:' + event.message.text + '\n')
                
                # message filter: exchange currencies 
                reply_text = msg_filter_exchange_currencies(event.message.text)
                
                if reply_text != '':
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))
        return HttpResponse()
    elif request.method == 'GET':
        print('### log: illegal request, or auto uptimerobot message ###')
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
    

def msg_filter_exchange_currencies(got_text):
    
    
    if got_text[-1] == '=' or (got_text[-2] == '=' and got_text[-1] == '$'):
        msg_token_list = currencies.replace_synonym(got_text)
        msg_token_list = currencies.judge_to_add(msg_token_list)
        
        msg = ''

        # check user want execute the instruction
        if msg_token_list[-2:] == ['=', '$'] and ('幣' in msg_token_list[-3] \
                                               or '元' in msg_token_list[-3] \
                                               or '圓' in msg_token_list[-3]):
            msg += msg_token_list[-4]
            msg += msg_token_list[-3]
            msg = '您選擇的貨幣『 ' + msg + ' 』不在我的支援範圍內唷 (ಥ_ಥ)' 
            print(msg)
            
            return msg
    
        if msg_token_list[-1] == '=' and ('幣' in msg_token_list[-2] \
                                          or '元' in msg_token_list[-2] \
                                          or '圓' in msg_token_list[-2]):
            msg += msg_token_list[-3]
            msg += msg_token_list[-2]
            msg = '您選擇的貨幣『 ' + msg + ' 』不在我的支援範圍內唷 (ಥ_ಥ)' 
            print(msg)
            
            return msg

        if len(msg_token_list) == 3 or \
            (len(msg_token_list) == 4 and msg_token_list[0] == '-'):
    
            if currencies.is_number(msg_token_list[0]) and msg_token_list[2] == '=':
                if (float(msg_token_list[0]) >= 0.0):
                    msg = currencies.calculate_rate(float(msg_token_list[0]) \
                                         , msg_token_list[1], None)
                    print(msg)
            
                else:
                    msg = '請不要餵我吃負額! 會發育不良的!(#`Д´)ﾉ'
                    print(msg)
                    
                return msg
            
            elif msg_token_list[0] == '-':
                msg = '請不要餵我吃負額! 會發育不良的!(#`Д´)ﾉ'
                print(msg)
                return msg
        
            elif ~currencies.is_number(msg_token_list[0]) and msg_token_list[2] == '=':
                msg = '對不起 我聽不懂你的意思><\n請確認您輸入的是否為數字'
                print(msg)
                return msg

        elif len(msg_token_list) == 4 or \
            (len(msg_token_list) == 5 and msg_token_list[0] == '-'):
            if currencies.is_number(msg_token_list[0]) and msg_token_list[2] == '=' \
                and msg_token_list[3] == '$':
            
                if (float(msg_token_list[0]) >= 0.0):
                    msg = currencies.calculate_rate(float(msg_token_list[0]),\
                                                msg_token_list[1], 'USD')
                    print(msg)
            
                else:
                    msg = '請不要餵我吃負額! 會發育不良的!(#`Д´)ﾉ'
                    print(msg)
                    
                return msg
    
            elif msg_token_list[0] == '-':
                msg = '請不要餵我吃負額! 會發育不良的!(#`Д´)ﾉ'
                print(msg)
                return msg
        
            elif ~currencies.is_number(msg_token_list[0]) and msg_token_list[2] == '=' \
                and msg_token_list[3] == '$':
                
                msg = '對不起 我聽不懂你的意思><\n請確認您輸入的是否為數字'
                print(msg)
                return msg
    
    if got_text != '幫幫我':
        out_text = '對不起 我聽不懂你說的意思><\n請確認您輸入的是我聽得懂的指令:\n'\
                   + got_text
    else:
        out_text = ''
    
    return out_text
    