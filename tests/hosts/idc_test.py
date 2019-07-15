import requests

if __name__ == "__main__":
    #session = requests.Session()
    #response = session.get("http://127.0.0.1:8080")
    #print(response.cookies)
    #print(response.content)
    response = requests.post('http://127.0.0.1:8080/hosts/idcs/add',data={
        'name': 'name2',
        'city': 'city2'
    })
    print(response.content)
