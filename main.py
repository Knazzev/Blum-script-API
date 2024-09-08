import requests as network
import json
import time
import random

def choose_language():
    print("1: Русский\n2: English")
    choice = input("Введите номер для выбора языка: ").strip()
    if choice == '1':
        return 'RU'
    elif choice == '2':
        return 'EN'
    else:
        print("Некорректный выбор, используется русский язык по умолчанию.")
        return 'RU'

language = choose_language()

def play_session(auth_token):
    request_headers = {
        'Authorization': 'Bearer ' + auth_token,
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }

    balance_response = network.get('https://game-domain.blum.codes/api/v1/user/balance', headers=request_headers)
    ticket_count = json.loads(balance_response.text)['playPasses']
    accumulated_points = 0

    if ticket_count > 0:
        tickets_spent = int(input("Сколько билетов вы хотите использовать?: " if language == 'RU' else "How many tickets would you like to use?: "))

        if tickets_spent > ticket_count:
            print("Недостаточно билетов!" if language == 'RU' else "Not enough tickets!")
        else:
            print("Игра начинается..." if language == 'RU' else "The game begins...")

            for round_num in range(tickets_spent):
                game_start_response = network.post('https://game-domain.blum.codes/api/v1/game/play', headers=request_headers)
                game_session_id = json.loads(game_start_response.text)['gameId']
                time.sleep(random.randint(30, 60))

                score = random.randint(150, 250)
                network.post('https://game-domain.blum.codes/api/v1/game/claim', headers=request_headers, json={
                    "gameId": game_session_id,
                    "points": score
                })

                print(f"Раунд {round_num + 1} из {tickets_spent} завершен" if language == 'RU' else f"Round {round_num + 1} of {tickets_spent} completed")
                time.sleep(random.randint(1, 5))
                print(f"Полученные очки: {score}" if language == 'RU' else f"Points earned: {score}")
                accumulated_points += score

            print(f"Общее количество очков: {accumulated_points}" if language == 'RU' else f"Total points: {accumulated_points}")
    else:
        print("Недостаточно ресурсов для игры." if language == 'RU' else "Not enough resources to play.")
        exit()

def claim_balance_from_friends(auth_token):
    request_headers = {
        'Authorization': 'Bearer ' + auth_token,
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    print("Начинаем сбор наград с друзей..." if language == 'RU' else "Starting to collect rewards from friends...")

    try:
        response = network.post('https://user-domain.blum.codes/api/v1/friends/claim', headers=request_headers)
        if response.status_code == 200:
            data = response.json()
            print(f"Текущий баланс: {data}" if language == 'RU' else f"Current balance: {data}")
        else:
            print(f"Ошибка при сборе наград, статус: {response.status_code}" if language == 'RU' else f"Error collecting rewards, status: {response.status_code}")
    except network.exceptions.ConnectionError as e:
        print(f"Ошибка соединения при сборе наград с друзей: {e}" if language == 'RU' else f"Connection error while collecting rewards from friends: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}" if language == 'RU' else f"An error occurred: {e}")

if __name__ == '__main__':
    auth_token = input("Введите ваш токен: " if language == 'RU' else "Enter your token: ")
    collect_friends_rewards = input("Хотите ли вы собрать награду с друзей? (y/n): " if language == 'RU' else "Do you want to collect rewards from friends? (y/n): ").strip().lower()

    if collect_friends_rewards == 'y':
        claim_balance_from_friends(auth_token)

    play_session(auth_token)