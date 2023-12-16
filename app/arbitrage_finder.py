import os
import requests
import json
import dateutil.parser as dp
from dotenv import load_dotenv



load_dotenv()

ODDS_API_KEY = os.getenv("ODDS_API_KEY")

weeks = ["Week 15", "Week 16", "Week 17", "Week 18", "Wild Card", "Divisional", "Conference Championships", "Super Bowl" ]
date = ["2023-12-13T01:00:00Z", "2023-12-20T01:00:00Z", "2023-12-27T01:00:00Z", "2023-01-03T01:00:00Z", "2023-01-13T01:00:00Z", 
        "2023-01-17T01:00:00Z", "2023-01-24T01:00:00Z", "2023-02-07T01:00:00Z", "2023-02-20T01:00:00Z"]
unix_date = [1702429200, 1703034000, 1703638800, 1672707600, 1673571600, 1673917200, 1674522000, 1675731600, 1676854800]


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

def arbitrage_calculator(home_odds, away_odds, desired_winnings):

    total_probability = ((1/float(home_odds[1])) + (1/float(away_odds[1])))

    if ((total_probability) < 1):
        stake_home = desired_winnings*1/float(home_odds[1])/total_probability
        stake_away = desired_winnings*1/float(away_odds[1])/total_probability

        profit_home = (stake_home*home_odds[1]) - desired_winnings
        profit_away = (stake_away*away_odds[1]) - desired_winnings

        #print (f"Bet placed on home team: {stake_home}")
        #print (f"Bet placed on away team: {stake_away}")
        #print (f"Total Profit: {profit}")
        return (f"Bet placed on home team: {to_usd(stake_home)}, Bet placed on away team: {to_usd(stake_away)}, Total Profit if Home Team Wins: {to_usd(profit_home)}, Total Profit if Away Team Wins: {to_usd(profit_away)}")

    else:
        print(1/float(away_odds[1]))
        return ("No arbitrage oppurtunity")

def best_odds(x):
    return max(x, key=lambda x:x[1])

def date_conversion(time):
    parsed_t = dp.parse(time)
    game_time = parsed_t.timestamp()
    return game_time

def data_retrieval(desired_sport, week):
    if (desired_sport == "NFL"):
        desired_sport = "americanfootball_nfl"

        date_num = weeks.index(week)
        date_from = date[date_num]
        date_to = date[date_num+1]
        unix_from = unix_date[date_num]
        unix_to = unix_date[date_num+1]
        

        request_url = f"https://api.the-odds-api.com/v4/sports/{desired_sport}/odds/?regions=us&oddsFormat=decimal&apiKey={ODDS_API_KEY}&commenceTimeFrom={date_from}&commenceTimeTo{date_to}"
        r = requests.get(request_url)
        
        data = json.loads(r.text)

        game_time = date_conversion(data[1]["commence_time"])

        if unix_to < game_time or game_time < unix_from:
            
            return data
        else:
            return data
    
    

def arbitrage_seeker(desired_sport, desired_winnings, week):

    data = data_retrieval(desired_sport, week)

    nfl_games = []

    final_data = []

    for entry in data:
        if entry['sport_key'] == 'americanfootball_nfl':
            nfl_games.append(entry)

    first_game = []

    books = []

    for game in nfl_games:
        books.append(game["bookmakers"])

    

    for book in books:
        odds = []
        odds_home = {}
        odds_away = {}

        for key in book:

            odds.append(key["markets"])
            for odd in odds:
                odds_home[key['title']] = odd[0]["outcomes"][0]['price']
                odds_away[key['title']] = odd[0]["outcomes"][1]["price"]
            #print (key['markets'])

        home_team = (key['markets'][0]['outcomes'][0]["name"])
        away_team = (key['markets'][0]['outcomes'][1]["name"])


        #print (f"----BEST {home_team} (H) ODDS----")


        best_home_odds = best_odds(odds_home.items())
        best_away_odds = best_odds(odds_away.items())

        arbitrage_calculator(best_home_odds, best_away_odds, desired_winnings)

        output = arbitrage_calculator(best_home_odds, best_away_odds, desired_winnings)

        
        data = {"Home Team": home_team, "Home Sportsbook": f"{best_home_odds[0]} ({best_home_odds[1]})" , "Away Team": away_team, "Away Sportsbook": f"{best_away_odds[0]} ({best_away_odds[1]})", "Arbitrage": output}


        final_data.append(data)

    #pprint (final_data)
    
    return (final_data)




#Main 
if __name__ == "__main__":

    desired_sport = input ("Sports League: (Options: 'NFL')")

    if (desired_sport == 'NFL'):
        desired_sport = "americanfootball_nfl"
        desired_winnings = input ("Max bet:")
        week = input("What week? i.e Week 15:")
        arbitrage_seeker(desired_sport, desired_winnings, week)
    else:
        print ("Sorry, we do not currently offer data on that league.")
