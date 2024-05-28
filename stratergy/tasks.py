from dhanhq import dhanhq
import datetime
import time
from celery import shared_task
from stratergy.symbols.details import get_price, get_market_data, get_instrument
from trade.models import dhanapi


client_id = "1100617939"
# access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzA2NjIzMDU3LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDYxNzkzOSJ9.Yo5ehm4a3fKwp-oqaKPkQK_hA37z6q-W5tlAyYU0FxD-MW39-qmQi11V2Ie2_Z_roFWGUOoNPZ2Y0xtyzqb-Lw"

access_token = dhanapi.objects.first().accesstoken

dhan = dhanhq(client_id,access_token)

#@shared_task
def manual_input_strat():
    from stratergy.models import Alert,Executed_Stratergy
    for x in Alert.objects.filter(function='Activated'):
        if datetime.datetime.now().time() < x.start_time:
            continue
        try:
            print('LTP Price')
            ltp = int(get_price(x.token))
            x.ltp = ltp
            x.save()
            f = open("ltp.txt", "a")
            f.write(f'{ltp}\n')
            f.close()
            print(ltp)
            if (((x.position_status == 'POSITION_CLOSED') and ltp <= (x.high-x.gap)) or ((x.position_status == 'SCALP_POSITION_CLOSED') and ltp >= (x.low+x.gap))):
                x.position_status = 'EMPTY'
                x.save()
            if (ltp >= (int(x.high)+(int(x.target)))):
                x.position_status = 'POSITION_CLOSED'
                x.ltp = ltp
                x.save()
            if (ltp <= (int(x.low)-(int(x.target)))):
                x.position_status = 'SCALP_POSITION_CLOSED'
                x.ltp = ltp
                x.save()
            a = dhan.intraday_daily_minute_charts(
                security_id=x.dhan_token,
                exchange_segment=x.segment,
                instrument_type=x.instrument_type
            )
            f = open("log.txt", "a")
            f.write(f'{a}\n')
            f.close()
            current_volume = int(a['data']['volume'][-1])
            if x.position_status == 'EMPTY':
                f = open("entry.txt", "a")
                f.write(f'Entry \n')
                f.close()
                try:
                    if (ltp > x.high and current_volume > x.last_volume):
                        x.position_status = 'POSITION_OPEN'
                        x.save()
                        f = open("order.txt", "a")
                        f.write(f'BUY POSITION \n')
                        f.close()
                        # PLACE BUY ORDER
                        Executed_Stratergy.objects.create(remark='Buy Position Created',url=x.url,syntax_used=x.buy_syntax,response="response")
                    if (ltp < x.low and current_volume > x.last_volume):
                        x.position_status = 'SCALP_POSITION_OPEN'
                        x.save()
                        # PLACE SELL ORDER
                        f = open("order.txt", "a")
                        f.write(f'SELL POSITION \n')
                        f.close()
                        Executed_Stratergy.objects.create(remark='Sell Position Created',url=x.url,syntax_used=x.sell_syntax,response="response")
                except Exception as e:
                     f = open("error.txt", "a")
                     f.write(f'ENTRY {e} \n')
                     f.close()
                x.last_volume = current_volume
                x.save()
        except Exception as e:
            print('-=-=-=-=-=-==-=-=-STRATERGY ERROR-=-=---=-=-=-=-=-=--=-=-=-')
            print(e)
            f = open("error.txt", "a")
            f.write(f'{e} \n')
            f.close()
    return {'status':'success'}

import datetime
import time
from stratergy.symbols.details import get_price, get_market_data, get_instrument
from threading import Thread



@shared_task
def update_data():
    f = open("once.txt", "a")
    f.write('one \n')
    f.close()
    remote = True
    start_time = time.time()
    end_time = start_time + 3600
    while time.time() < end_time:
        try:
            from stratergy.models import Alert,Stratergy_settings
            remote = Stratergy_settings.objects.all().first().status
            temp_list = []
            for x in Alert.objects.filter(function='Activated'):
                temp_list.append(get_instrument(x.token))
            symbols = ','.join(temp_list)
            f = open("symbols.txt", "a")
            f.write(f'{symbols} \n')
            f.close()
            f = open("logging.txt", "a")
            f.write(f'Bot Started at {datetime.datetime.now()} \n')
            f.close()
            market_data = get_market_data(symbols)
            for x in market_data['data']:
                symbol = market_data['data'][x]['symbol']
                ob = Alert.objects.filter(symbol=symbol).first()
                print('-==-=-=-=-=-=-=-=-=-')
                ob.ltp = int(market_data['data'][x]['last_price'])
                ob.current_volume = int(market_data['data'][x]['volume'])
                f = open("ltp.txt", "a")
                f.write(f'{ob.ltp} \n')
                f.close()
                ob.save()
            time.sleep(3)
        except Exception as e:
            f = open("error.txt", "a")
            f.write(f'Bot Started at {datetime.datetime.now()}, {e} \n')
            f.close()
            time.sleep(3)
