import requests


def get_pass(num):
    api = "https://random-word-api.herokuapp.com/word"
    parameters = {"number": num}
    response = requests.get(f"{api}", params=parameters)
    if response.status_code != 200:
        return Exception("Error in fetching data")
    else:
        result = response.json()
        s = ""
        for i in range(num - 1):
            s += result[i] + "-"
        s += result[num - 1]
        return s


ans = get_pass(7)
print(ans)
