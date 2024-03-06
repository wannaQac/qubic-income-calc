import requests
from datetime import datetime

hashrate   = 100 # 自己主机目前的算力
login_url  = 'https://api.qubic.li/Auth/Login' # qubic登录url 
data_url   = 'https://api.qubic.li/Score/Get'  # qubic数据url
login_data = {"userName": "guest@qubic.li", "password": "guest13@Qubic.li"} # qubic官网用户名密码
price_url  = "https://tradeogre.com/api/v1/ticker/QUBIC-USDT" # qubic价格url

print('-----------------------------------')
# 获取当前时间
formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("当前时间:", formatted_time)
print('-----------------------------------') 

login_response = requests.post(login_url, json=login_data)
if login_response.ok and "token" in login_response.json():

    token   = login_response.json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    data_response = requests.get(data_url, headers=headers)
        
    if data_response.ok:
        data = data_response.json()

        epoch      = data['scoreStatistics'][0]['epoch']
        allnethash = data['estimatedIts']
        solperhour = data['solutionsPerHour']
        coinperSol = int(((10 ** 12 / 1.06) / (solperhour * 24 * 7)) * 0.85)
        solperDay  = round((hashrate / allnethash) * solperhour * 24, 2)
        avgscore   = round(data['averageScore'],2)
        print('全网算力:', allnethash, 'it/s')
        print('当前纪元:', epoch)
        print('一个Sol预估币量:', coinperSol)
        print('-----------------------------------') 
        
        # 获取qubic价格
        price_response = requests.get(price_url)
        if price_response.ok and "price" in price_response.json():
          price  = price_response.json()['price']
          income = round(coinperSol * float(price) * float(solperDay), 2)
          print('当前qubic价格: $', price)
          print(hashrate, 'it/s 算力预估每日sol数量:', solperDay)
          print(hashrate, 'it/s 算力预估每日收益(USDT):', income)
          print('-----------------------------------') 
          
    else:
        print('登录qubic网站成功，但登录算力页面失败.')
else:
    print('登录qubic网站失败，无法获取算力信息.')
