from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

bp = Blueprint('quote', __name__)


def lookup(symbol):
    """Look up quote for symbol."""
        # Contact API
    api_key = "pk_ffcacf40c52845028338ee78513497b1"
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token=pk_ffcacf40c52845028338ee78513497b1"
    response = requests.get(url)

    quote = response.json()
    
    return {
        "name": quote["companyName"],
        "price": float(quote["latestPrice"]),
        "symbol": quote["symbol"],
        "currency": quote["currency"]
    }

    

@bp.route("/")
@login_required
def index():
    db = get_db()
    user_id = int(session.get('user_id'))
    print(user_id)
    history = db.execute("SELECT * FROM stocks WHERE stk_id = ?",(user_id,))

    return render_template('quote/index.html', history=history)


@bp.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        error = None
        qt = lookup(symbol)  

        # Ensure symbol was submited
        if not symbol:
            error = 'Must provide ticker'
        if qt is None:
            error = 'Incorrect ticker'
        # insert into database
        insert = """INSERT INTO stocks (stk_id, sym, nm, prc) VALUES (?, ?, ?, ?)"""
        data_tuple = (g.user['id'], qt["symbol"], qt["name"], qt["price"])
        
        db = get_db()
        db.execute(insert, data_tuple)
        db.commit()   
        return render_template("quote/quoted.html", qt=qt)

    else:
        return render_template("quote/quote.html")
    


@bp.route("/del/", methods=["GET", "POST"])
@login_required
def del_all():
    db = get_db()
    db.execute('DELETE FROM stocks')
    db.commit()
    return redirect(url_for('quote.index'))
