import yfinance as yf

def check_inside_breakouts(stocks):
    breakout_msgs = []

    for symbol in stocks:
        try:
            data = yf.download(f"{symbol}.NS", period="5d", interval="1d", progress=False)
            if len(data) < 3:
                continue

            prev_candle = data.iloc[-2]
            curr_candle = data.iloc[-1]

            # Inside candle condition
            if (curr_candle["High"] < prev_candle["High"]) and (curr_candle["Low"] > prev_candle["Low"]):
                breakout_msgs.append(f"📍 Inside candle: {symbol}")

        except Exception as e:
            breakout_msgs.append(f"⚠️ {symbol} error: {e}")

    return breakout_msgs