from flask import Flask, jsonify, render_template
import database

app = Flask(__name__)

database.init_db()


@app.route('/api/cards')
def cards():
    """Return all cards with their latest price."""
    data = database.get_latest_prices()
    return jsonify(data)


@app.route('/api/cards/<int:card_id>/history')
def card_history(card_id):
    """Return price history for a specific card."""
    data = database.get_price_history(card_id)
    return jsonify(data)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
