import os
import requests
import json

from dotenv import load_dotenv

from app.alpha import ODDS_API_KEY


load_dotenv()

ODDS_API_KEY = os.getenv("ODDS_API_KEY")


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71
def arbitrage_calculator(home_odds, away_odds, desired_winnings):

    total_probability = ((1/float(home_odds)) + (1/float(away_odds)))

    if ((total_probability) < 1):
        stake_home = desired_winnings*1/float(home_odds)/total_probability
        stake_away = desired_winnings*1/float(away_odds)/total_probability

        profit_home = (stake_home*home_odds) - desired_winnings
        profit_away = (stake_away*away_odds) - desired_winnings

        #print (f"Bet placed on home team: {stake_home}")
        #print (f"Bet placed on away team: {stake_away}")
        #print (f"Total Profit: {profit}")
        return (f"Bet placed on home team: {to_usd(stake_home)}, Bet placed on away team: {to_usd(stake_away)}, Total Profit if Home Team Wins: {to_usd(profit_home)}, Total Profit if Away Team Wins: {to_usd(profit_away)}")

    else:
        print(1/float(away_odds))
        return ("No arbitrage oppurtunity")



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
if __name__ == "__main__":

    desired_sport = input ("Sports League: (Options: 'NFL')")

    if (desired_sport == 'NFL'):
        desired_sport = "americanfootball_nfl"
        desired_winnings = input ("Max bet:")
        arbitrage_seeker(desired_sport, desired_winnings)
    else:
        print ("Sorry, we do not currently offer data on that league.")

