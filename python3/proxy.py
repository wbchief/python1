import requests
#
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Cookie': 'BAIDUID=662909CEBF72065225B74349CAB6B571:FG=1; BIDUPSID=662909CEBF72065225B74349CAB6B571; PSTM=1535525646; BD_UPN=123353; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BD_HOME=0; BD_CK_SAM=1; PSINO=5; H_PS_645EC=726dtlIkBvsHiBflVNk2Z4wQgaCcwbLQ4XD74lp2iK8Lpq%2FeuG%2BnMnW%2FX%2Fc; pgv_pvi=8067049472; pgv_si=s3879649280; H_PS_PSSID=26523_1464_25810_26909_21102_26350_20929',
#     'Host': 'www.baidu.com',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
# }
# response = requests.get('http://www.baidu.com', headers=headers, proxies={'http': 'http://103.76.175.87:8080', 'https': 'https:https://103.76.175.87:8080'})
# print(response.status_code)
# html = response.text
# print(html)

response = requests.get('http://www.baidu.com')

//*[@id="content"]/div/div[2]/ul/li[1]/div