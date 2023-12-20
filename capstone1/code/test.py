import requests

url = 'http://localhost:9696/predict'

data = {'url': 'https://vegcropshotline.org/wp-content/uploads/2018/08/3-CercosporaLeaf1.jpg'}

result = requests.post(url, json=data).json()
print(result)