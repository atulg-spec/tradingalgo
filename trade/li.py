from fyers_api.Websocket import ws


def run_process_symbol_data(access_token):
    data_type = "symbolData"
    symbol = ["NSE:SBIN-EQ"]
    fs = ws.FyersSocket(access_token=access_token,log_path="/home/user/logs")
    fs.websocket_data = custom_message
    fs.subscribe(symbol=symbol,data_type=data_type)
    fs.keep_running()


def custom_message(msg):
    print (f"Custom:{msg}") 


def main():
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTE1MDk1NzcsImV4cCI6MTY5MTU0MTAxNywibmJmIjoxNjkxNTA5NTc3LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCazBtTkpfWW5kMkxmNjltSGJMUXRQMlJhVEJoUzJhRWxtMDFDWDBaMlpncnFTeXFRbGtTOHludF94VnA2V0lSOUZDalQ0UjB1T3RlV2M0MzlGdVZ4QnhHNHE5VXh1dUUyY21ldEJXX1ExVXhWblZVST0iLCJkaXNwbGF5X25hbWUiOiJBU0lGIEFMSSIsIm9tcyI6IksxIiwiaHNtX2tleSI6Ijc3NmE3YmVmMDdjOGQxN2VmZTM0NzYxNTU0NzAwYmI2YzViZDg3YTUzODQxMWEyYzJiOWZmNmU3IiwiZnlfaWQiOiJYQTYxMDg1IiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.IC4GW2k_rlq2e71XKJYXFkCyDl8gO5uU3Xn9ljyBo5k"
    run_process_symbol_data(access_token)


if __name__ == '__main__':
  main()