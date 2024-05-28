from stratergy.symbols.instruments import *
import upstox_client

def get_market_data(upstox_symbol_list):
    from stratergy.models import Stratergy_settings
    access_token = Stratergy_settings.objects.all().first().access_token
#    access_token = "eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIyOEFaNDUiLCJqdGkiOiI2NTk0MDc2ZmI4ZWUxOTVjYzhmMzMyNjQiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNBY3RpdmUiOnRydWUsInNjb3BlIjpbImludGVyYWN0aXZlIiwiaGlzdG9yaWNhbCJdLCJpYXQiOjE3MDQyMDAwNDcsImlzcyI6InVkYXBpLWdhdGV3YXktc2VydmljZSIsImV4cCI6MTcwNDIzMjgwMH0.DL0t9cY9dUU8XxY84XoNIZO-QbCC6EiVEbUGUtM2X0I"
    f = open('tkn.txt','w')
    f.write(f'\n{upstox_symbol_list} \n')
    try:
        configuration = upstox_client.Configuration()
        configuration.access_token = access_token
        api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))
        api_version = 'v-2'
        api_response = api_instance.get_full_market_quote(upstox_symbol_list, api_version)
        f.close()
        return api_response.to_dict()
    except Exception as e:
        return None


def get_price(token,c=1):
    instrument = get_instrument(token)
    segment = get_exchange(token)
    try:
        market_data = get_market_data(instrument)
        symbol_data = market_data['data'][f"{segment}:{get_symbol(token)}"]
        return symbol_data.get('last_price', 0)
    except Exception as e:
        co = c+1
        if co == 2:
            return 0.0
        return get_price(token,c=co)
