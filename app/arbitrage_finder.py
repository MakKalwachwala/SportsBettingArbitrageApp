import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()

ODDS_API_KEY = os.getenv("ODDS_API_KEY")



def arbitrage_calculator(home_odds, away_odds, desired_winnings):

    total_probability = ((1/float(home_odds)) + (1/float(away_odds)))

    if ((total_probability) < 1):
        stake_home = desired_winnings / home_odds
        stake_away = desired_winnings / away_odds

        profit = desired_winnings - stake_home - stake_away

        print (f"Bet placed on home team: {stake_home}")
        print (f"Bet placed on away team: {stake_away}")
        print (f"Total Profit: {profit}")
    else:
        print ("No arbitrage oppurtunity")



def arbitrage_seeker(desired_sport, desired_winnings):

    request_url = f"https://api.the-odds-api.com/v4/sports/{desired_sport}/odds/?regions=us&oddsFormat=decimal&apiKey={ODDS_API_KEY}"

    r = requests.get(request_url)

    data = json.loads(r.text)

    nfl_games = []

    for entry in data:
        if entry['sport_key'] == 'americanfootball_nfl':
            nfl_games.append(entry)


    for game in nfl_games:
        print (game['home_team']+"(H)", "vs" , game['away_team'] + "(A)" )


    first_game = []

    books = []

    for game in nfl_games:
        books.append(game["bookmakers"])

    odds = []
    odds_home = {}
    odds_away = {}

    for book in books:

        for key in book:
            odds.append(key["markets"])
            for odd in odds:
                odds_home[key['title']] = odd[0]["outcomes"][0]['price']
                odds_away[key['title']] = odd[0]["outcomes"][1]["price"]
            #print (key['markets'])

        home_team = (key['markets'][0]['outcomes'][0]["name"])
        away_team = (key['markets'][0]['outcomes'][1]["name"])


        print (f"----BEST {home_team} (H) ODDS----")


        best_home_odds = 0.00
        best_home_odds_sportsbook = " "


        for line in odds_home.items():


            if (line[1] > best_home_odds):
                best_home_odds = line[1]
                best_home_odds_sportsbook = line[0]

        print (best_home_odds_sportsbook)
        print (best_home_odds)



        print (f"---- BEST {away_team} (A) ODDS----")

        best_away_odds = 0.00
        best_away_odds_sportsbook = " "

        for line in odds_away.items():



            if (line[1]) > best_away_odds:
                best_away_odds = line[1]
                best_away_odds_sportsbook = line[0]


        print (best_away_odds_sportsbook)

        print (best_away_odds)

        desired_winnings = 200.00

        arbitrage_calculator(best_home_odds, best_away_odds, desired_winnings)



#Main 

desired_sport = input ("Sports League: (Options: 'NFL')")

if (desired_sport == 'NFL'):
    desired_sport = "americanfootball_nfl"
    desired_winnings = input ("Max bet:")
    arbitrage_seeker(desired_sport, desired_winnings)
else:
    print ("Sorry, we do not currently offer data on that league.")

