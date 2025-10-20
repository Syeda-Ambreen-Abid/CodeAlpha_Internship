# app.py
from flask import Flask, render_template_string, request, redirect, url_for, send_file, Response
from types import SimpleNamespace

app = Flask(__name__)

# Hardcoded stock prices
stock_prices = {
    "AAPL": 180, "TSLA": 250, "MSFT": 320, "GOOGL": 135, "AMZN": 140,
    "NFLX": 410, "META": 305, "NVDA": 450, "BABA": 90, "JPM": 150,
    "V": 230, "MA": 380, "DIS": 90, "PYPL": 65, "ORCL": 120,
    "INTC": 35, "AMD": 110, "UBER": 48, "LYFT": 12, "SHOP": 60
}

# In-memory portfolio
portfolio = {}

# Template
template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Stock Portfolio Tracker</title>
    <style>
        body { font-family: Arial, sans-serif; background: #fff; color: #000; margin: 40px;}
        header { text-align: center; margin-bottom: 20px; }
        h1 {
            display: inline-block;
            background: linear-gradient(90deg, #e63946, #1d3557);
            -webkit-background-clip: text;
            color: transparent;
            font-size: 60px;
            margin: 40px 10px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        form { text-align: center; margin: 20px 0; }
        label {
            color: #1d3557; font-weight: 700; display: inline-block;
            width: 110px; font-size: 22px;
        }
        select, input[type="number"] {
            height: 45px; font-size: 18px; padding: 5px 10px;
            border: 1px solid #000; border-radius: 6px;
        }
        select { width: 180px; margin-right: 20px; }
        input[type="number"] { width: 140px; margin-right: 20px; }

        .controls {
    text-align: center;
    margin-top: 20px;
}

.controls .button {
    display: inline-block;
    margin: 0 10px;
    padding: 10px 18px;
    border-radius: 8px;
    border: none;
    background: green;
    color: #fff;
    cursor: pointer;
    font-size: 20px;
    font-weight: 700;
    text-decoration: none;
}

.controls .button:hover {
    background: lightgreen;
}

        .button{
            padding: 9px 14px;
            width: 140px;
            height: 30px;
            margin: 0;
            padding:0
            border-radius: 8px;
            border: none;
            background: blue;
            color: #fff;
            cursor: pointer;
            font-size: 20px;
            font-weight: 700;}

         button {
            padding: 9px 14px;
            width: 160px;
            height: 40px;
            margin-left: 6px;
            border-radius: 8px;
            border: none;
            background: #e63946; /* red */
            color: #fff;
            cursor: pointer;
            font-size: 20px;
            font-weight: 700;
        }
        button:hover { background: #1d3557; }
        .result { margin-top: 20px; padding: 20px; border-radius: 12px;
                  border: 2px solid #1d3557; background: #fafafa; }
        .result h3 { color: #e63946; text-align: center; }
        ul { list-style: none; padding: 0; }
        li { padding: 6px 8px; border-bottom: 1px dashed #ddd; }
        .error { color: #e63946; text-align: center; font-weight: 700; }
        .small{
        margin-top:20px}
    </style>
</head>
<body>
    <header><h1> 📊 Stock Portfolio Tracker</h1></header>
    <div class="container">
        <form method="post" action="{{ url_for('index') }}">
            <label for="stock">Stock</label>
            <select name="stock" id="stock" required>
                {% for s in stock_prices %}
                    <option value="{{ s }}">{{ s }} (${{ stock_prices[s] }})</option>
                {% endfor %}
            </select>

            <label for="quantity">Quantity</label>
            <input type="number" name="quantity" id="quantity" min="1" value="1" required>
            <button type="submit">Check</button>
        </form>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        {% if portfolio %}
            <div class="result">
                <h3 style="font-size:25px;">Your Portfolio</h3>
                <ul>
                    {% for stock, data in portfolio.items() %}
                        <li><strong>{{ stock }}</strong>: {{ data.qty }} × ${{ data.price }} = ${{ data.value }}</li>
                    {% endfor %}
                </ul>
                <div style="font-size:25px; text-align:center; margin-top:10px;">
                    <strong>Total Investment: ${{ total }}</strong>
                </div>

               <div class="controls">
                    <!-- Reset uses anchor that clears the server-side portfolio -->
                    <a class="button" href="{{ url_for('reset') }}">🔄 Reset</a>

                    <!-- Download link: triggers the /download route which returns a file -->
                    <a class="button" href="{{ url_for('download') }}">💾 Save</a>
                </div>
                <div class="small">Tip: Reset clears your portfolio. Save downloads it as <code>portfolio.txt</code>.</div>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        stock = request.form.get("stock", "").upper()
        qty_raw = request.form.get("quantity", "0")
        try:
            qty = int(qty_raw)
            if qty < 1:
                raise ValueError("Quantity must be >= 1")
        except ValueError:
            total = sum(item["value"] for item in portfolio.values())
            portfolio_ns = {k: SimpleNamespace(**v) for k, v in portfolio.items()}
            return render_template_string(template, stock_prices=stock_prices, portfolio=portfolio_ns,
                                          total=total, error="Quantity must be a positive integer.")
        if stock not in stock_prices:
            total = sum(item["value"] for item in portfolio.values())
            portfolio_ns = {k: SimpleNamespace(**v) for k, v in portfolio.items()}
            return render_template_string(template, stock_prices=stock_prices, portfolio=portfolio_ns,
                                          total=total, error="Unknown stock symbol.")
        price = stock_prices[stock]
        value = price * qty
        if stock in portfolio:
            portfolio[stock]["qty"] += qty
            portfolio[stock]["value"] += value
        else:
            portfolio[stock] = {"qty": qty, "price": price, "value": value}
        return redirect(url_for("index"))

    total = sum(item["value"] for item in portfolio.values())
    portfolio_ns = {k: SimpleNamespace(**v) for k, v in portfolio.items()}
    return render_template_string(template, stock_prices=stock_prices, portfolio=portfolio_ns, total=total, error=None)

@app.route("/reset")
def reset():
    portfolio.clear()
    return redirect(url_for("index"))

from flask import Response


@app.route("/save", methods=["POST"])
def save():
    """Save portfolio to file and allow download"""
    total = sum(item["value"] for item in portfolio.values())
    with open("portfolio.txt", "w") as f:
        f.write("📊 Portfolio Summary:\n")
        for stock, data in portfolio.items():
            f.write(f"{stock}: {data['qty']} × ${data['price']} = ${data['value']}\n")
        f.write(f"\n💰 Total Investment Value: ${total}\n")
    return send_file("portfolio.txt", as_attachment=True)

from flask import Response

@app.route("/download")
def download():
    content = "📊 Portfolio Summary:\n"
    total = sum(item["value"] for item in portfolio.values())
    for stock, data in portfolio.items():
        content += f"{stock}: {data['qty']} × ${data['price']} = ${data['value']}\n"
    content += f"\n💰 Total Investment Value: ${total}\n"

    return Response(
        content,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=portfolio.txt"}
    )

if __name__ == "__main__":
    app.run(debug=True)
