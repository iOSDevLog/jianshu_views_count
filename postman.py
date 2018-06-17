import requests

url = "https://www.jianshu.com/notes/173451a13914/mark_viewed.json"

payload = "uuid=8b832e19-9e2b-4776-9761-93f099f23f9e"
headers = {
    'Origin': "https://www.jianshu.com",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15",
    'Referer': "https://www.jianshu.com/p/173451a13914",
    'Content-Type': "text/plain",
    'Cache-Control': "no-cache",
    'Postman-Token': "abe87427-a2a3-4f11-a66f-1bdcc0320913"
    }

while True:
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

