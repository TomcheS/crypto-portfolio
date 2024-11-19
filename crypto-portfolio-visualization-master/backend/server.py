
import requests

from collections import defaultdict
from datetime import datetime
from psycopg2 import pool
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from logic import BOUGHT, SOLD
from logic import format_db_row_to_transaction


LIVE_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"

postgreSQL_pool = pool.SimpleConnectionPool(
    1,
    20,
    database="exampledb",
    user="docker",
    password="docker",
    host="0.0.0.0"
)

app = Flask(__name__)
cors = CORS(app)

app.config['postgreSQL_pool'] = postgreSQL_pool


@app.route("/")
def health_check():
    return "I am cool!"


@app.route("/transactions")
@cross_origin()
def get_transactions():
    cur = postgreSQL_pool.getconn().cursor()
    cur.execute("SELECT * FROM transaction")
    rows = cur.fetchall()
    return jsonify(
        [
            format_db_row_to_transaction(row)
            for row in rows
        ]
    )


@app.route("/transactions", methods=["POST"])
def new_transaction():
    name = request.json["name"]
    symbol = request.json["symbol"]
    type = request.json["type"]
    amount = request.json["amount"]
    time_transacted = datetime.fromtimestamp(request.json["time_transacted"])
    time_created = datetime.fromtimestamp(request.json["time_created"])
    price_purchased_at = float(request.json["price_purchased_at"])
    no_of_coins = float(request.json.get("no_of_coins"))

    conn = postgreSQL_pool.getconn()
    cur = conn.cursor()
    insert_statement = f"INSERT INTO transaction (name, symbol, type, amount, time_transacted, time_created, price_purchased_at, no_of_coins) VALUES ('{name}', '{symbol}', {type}, {amount}, '{time_transacted}', '{time_created}', {price_purchased_at}, {no_of_coins}) RETURNING *"
    cur.execute(insert_statement)
    inserted_record = cur.fetchone()
    conn.commit()

    request.json["id"] = inserted_record[0]
    return jsonify(request.json)


@app.route("/get_rollups_by_coin")
def get_rollups_by_coin():
    portfolio = defaultdict(
        lambda: {
            "coins": 0,
            "total_cost": 0,
            "total_equity": 0,
            "live_price": 0
        }
    )

    conn = postgreSQL_pool.getconn()
    cur = conn.cursor()
    cur.execute(
        "SELECT symbol, type, SUM(amount)/100 AS total_amount, SUM(no_of_coins) AS total_coins FROM transaction GROUP BY symbol, type"
    )
    rows = cur.fetchall()
    for row in rows:
        coin = row[0]
        transaction_type = row[1]
        transaction_amount = row[2]
        transaction_coins = row[3]

        # This is a purchase
        if transaction_type == 1:
            portfolio[coin]['total_cost'] += transaction_amount
            portfolio[coin]['coins'] += transaction_coins
        else:
            # This is a sell
            portfolio[coin]['total_cost'] -= transaction_amount
            portfolio[coin]['coins'] -= transaction_coins

    symbol_to_coin_id_map = {
        "BTC": "bitcoin",
        "SOL": "solana",
        "LINK": "chainlink",
        "ETH": "ethereum",
        "ADA": "cardano",
        "MANA": "decentraland",
    }
    rollups_response = []
    for symbol in portfolio:
        response = requests.get(
            f"{LIVE_PRICE_URL}?ids={symbol_to_coin_id_map[symbol]}&vs_currencies=usd").json()
        live_price = response[symbol_to_coin_id_map[symbol]]['usd']

        portfolio[symbol]['live_price'] = live_price
        portfolio[symbol]['total_equity'] = float(
            portfolio[symbol]['coins']) * live_price

        rollups_response.append(
            {
                "symbol": symbol,
                "live_price": portfolio[symbol]['live_price'],
                "total_equity": portfolio[symbol]['total_equity'],
                "coins": portfolio[symbol]['coins'],
                "total_cost": portfolio[symbol]["total_cost"]
            }
        )
    return jsonify(rollups_response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
