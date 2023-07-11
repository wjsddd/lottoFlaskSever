import json
import os
import random
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/lotto', methods=['GET'])
def lottoNum():
    num = request.args.get('num')
    numList = compare_lists(int(num))

    print(len(numList))
    jsonData = json.dumps(numList)

    return jsonData

def compare_lists(num):
    winningNumber = get_lotto_numbers(3)

    random_numbers = []

    choiceRanNum = generate_random_numbers(num)

    choiceRanNumLength = len(choiceRanNum)

    for i in range(choiceRanNumLength):
        
        random_numbers.append(winningNumber[choiceRanNum[i]])


    while len(random_numbers) < 6:
        new_number = random.randint(1, 45)
        if new_number not in random_numbers:
            random_numbers.append(new_number)
    
    random_numbers.sort()
    return random_numbers

def get_lotto_numbers(num):
    api_url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={num}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            lotto_numbers = [data[f"drwtNo{i}"] for i in range(1, 7)]

            return lotto_numbers
        else:
            print("API 요청에 실패했습니다. 상태 코드:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("API 요청 중 오류가 발생했습니다:", str(e))

    return None

def generate_random_numbers(num):
    numbers = []
    while len(numbers) < num:
        new_number = random.randint(0, 5)
        if new_number not in numbers:
            numbers.append(new_number)
    numbers.sort()
    return numbers




if __name__ == "__main__":
    app.run(host='172.30.1.68', port=5000)




