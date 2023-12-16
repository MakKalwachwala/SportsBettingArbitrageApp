from flask import Blueprint, request, render_template, redirect, flash

from app.arbitrage_finder import arbitrage_output

arbitrage_routes = Blueprint("arbitrage_routes", __name__)

@arbitrage_routes.route("/arbitrage/form")
def arbitrage_form():
    print ("ARBITRAGE FORM...")
    return render_template("arbitrage_form.html")

@arbitrage_routes.route("/arbitrage/dashboard", methods = ["GET", "POST"])
def arbitrage_dashboard():
    print("ARBITRAGE DASHBOARD...")

    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)
    else:
        # for data sent via GET request, url params are in request.args
        request_data = dict(request.args)
        print("URL PARAMS:", request_data)

    desired_sport = request_data.get("sports_league")  
    max_bet = request_data.get("max_bet") 
    week = request_data.get("week")
    try:
        data = arbitrage_output(desired_sport, float(max_bet), week)
        return render_template("arbitrage_dashboard.html",
        data = data,
        desired_sport = desired_sport,
        max_bet = max_bet
        )
    except Exception as err:


        print('OOPS', err)

        flash("Market Data Error. Market Data is not available for selected week", "danger")
        return redirect("/arbitrage/form")