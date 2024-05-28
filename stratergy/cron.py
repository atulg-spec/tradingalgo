from stratergy.models import Executed_Stratergy
from dhanhq import dhanhq
import datetime
import upstox_client
import time
from stratergy.symbols.details import get_price, symbollist, get_market_data, get_instrument
from stratergy.symbols.instruments import get_instrument_type


client_id = "1100617939"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzAzOTA5NDk0LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDYxNzkzOSJ9.qJkrDil7DJeAizbFWs3LGXdNqHIWKQMVisrrCOeJAlbcUvahmArsFEimIgrXkQu50nKPOgDkn5d0ToPBd2x5qg"

dhan = dhanhq(client_id,access_token)
def manual_input_strat():
    from stratergy.models import Alert,Executed_Stratergy
    for x in Alert.objects.filter(function='Activated'):
        if datetime.datetime.now().time() < x.start_time:
            continue
        start_time = time.time()
        end_time = start_time + (60)
        while time.time() < end_time:
            try:
                data = symbollist.get(x.symbol)
                token = data['token']
                print('LTP Price')
                ltp = int(get_price(x.symbol))
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
                    security_id=token,
                    exchange_segment=x.segment,
                    instrument_type=get_instrument_type(token)
                )
                current_volume = int(a['data']['volume'][-1])
                if x.position_status == 'EMPTY':
                    if (ltp > x.high and current_volume > x.last_volume):
                        # PLACE BUY ORDER
                        data = symbollist.get(x.symbol)
                        instrument = get_instrument(data['token'])
                        response = get_market_data(instrument)
                        x.position_status = 'POSITION_OPEN'
                        Executed_Stratergy.objects.create(remark='Buy Position Created',syntax_used=x.buy_syntax,response=response)
                    if (ltp < x.low and current_volume > x.last_volume):
                        # PLACE SELL ORDER
                        data = symbollist.get(x.symbol)
                        instrument = get_instrument(data['token'])
                        response = get_market_data(instrument)
                        x.position_status = 'SCALP_POSITION_OPEN'
                        Executed_Stratergy.objects.create(remark='Sell Position Created',syntax_used=x.sell_syntax,response=response)
                    x.last_volume = current_volume
                    x.ltp = ltp
                    x.save()
            except Exception as e:
                print('-=-=-=-=-=-==-=-=-STRATERGY ERROR-=-=---=-=-=-=-=-=--=-=-=-')
                print(e)
            time.sleep(1)
    
