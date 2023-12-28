from flask import Flask, render_template, request
import requests

api_key = "RGAPI-468541bf-a0f9-41bd-a7d3-5a44b0624362"
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        tag = request.form['tag']
        print(name)
        region = "americas" 
        api_url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
        api_url += f'?api_key={api_key}'
        print(api_url)
        resp = requests.get(api_url)
        player_info = resp.json()
        print(player_info)
        player_puuid = player_info['puuid']
        
       


        start = 0
        all_matches = []
        matches = []


        region = "americas"


        while True:
            api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{player_puuid}/ids?queue=450&start={start}"
            api_url += f"&api_key={api_key}"
            print(api_url)
            resp = requests.get(api_url)
            matches = resp.json()
            if not matches:
                break
            start += 20
            all_matches += matches
            print("hello")


        print(len(all_matches))


        win_data = {}
        kd_data = {}
        dmg_data = {}


        for match_id in all_matches:
            match_data = get_match_data(region, match_id)
            key = getChamp(player_puuid, match_data)
            game_win = win(player_puuid, match_data)
            game_kd = kd(player_puuid, match_data)
            game_dmg = dmg(player_puuid, match_data)
            if key in win_data:
                win_data[key].append(game_win)
                kd_data[key].append(game_kd)
                dmg_data[key].append(game_dmg)
            else:
                win_data[key] = [game_win]
                kd_data[key] = [game_kd]
                dmg_data[key] = [game_dmg]


        averages = {}


        for key in win_data:
            win_values = win_data[key]
            kd_values = kd_data[key]
            dmg_values = dmg_data[key]


            average_win = round(sum(win_values) / float(len(win_values)), 2)
            average_kd = round(sum(kd_values) / len(kd_values), 2)
            average_dmg = round(sum(dmg_values) / len(dmg_values), 2)
            num_games = len(win_values)




            averages[key] = {
                "average_win": average_win,
                "average_kd": average_kd,
                "average_dmg": average_dmg,
                "num_games": num_games
            }


        return render_template('stats.html', username=name, stats=averages)


    return render_template('index.html')


def get_match_data(region, match_id):
    import time
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    while True:
        resp = requests.get(api_url)
        if resp.status_code == 429:
            print("Rate Limit hit, sleeping for 120 seconds")
            time.sleep(120)
            continue
        data = resp.json()
        return data


def getChamp(puuid, match_data):
    player_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][player_index]['championName']


def win(puuid, match_data):
    player_index = match_data['metadata']['participants'].index(puuid)
    return int(match_data['info']['participants'][player_index]['win'])


def kd(puuid, match_data):
    player_index = match_data['metadata']['participants'].index(puuid)
    kills = match_data['info']['participants'][player_index]['kills']
    deaths = match_data['info']['participants'][player_index]['deaths']
    return kills / deaths if deaths != 0 else kills


def dmg(puuid, match_data):
    player_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][player_index]['totalDamageDealtToChampions']


if __name__ == '__main__':
    app.run()


