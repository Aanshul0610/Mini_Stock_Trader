def calculate_percent_change(data):
    first_price = data["Close"].iloc[0]
    last_price = data["Close"].iloc[-1]

    percent_change = ((last_price - first_price) / first_price) * 100

    return round(percent_change, 2)


def calculate_moving_averages(data):
    data = data.copy()

    data["MA7"] = data["Close"].rolling(window=7).mean()
    data["MA20"] = data["Close"].rolling(window=20).mean()

    latest_ma7 = data["MA7"].iloc[-1]
    latest_ma20 = data["MA20"].iloc[-1]

    return latest_ma7, latest_ma20


def get_stock_signal(data):
    percent_change = calculate_percent_change(data)
    latest_ma7, latest_ma20 = calculate_moving_averages(data)

    if latest_ma7 > latest_ma20 and percent_change > 0:
        signal = "Bullish"
        confidence = "Medium"
        reason = "The 7-day moving average is above the 20-day moving average and recent return is positive."

    elif latest_ma7 < latest_ma20 and percent_change < 0:
        signal = "Bearish"
        confidence = "Medium"
        reason = "The 7-day moving average is below the 20-day moving average and recent return is negative."

    else:
        signal = "Sideways / Unclear"
        confidence = "Low"
        reason = "The moving averages and recent return do not strongly agree."

    return {
        "signal": signal,
        "confidence": confidence,
        "reason": reason,
        "ma7": round(latest_ma7, 2),
        "ma20": round(latest_ma20, 2)
    }


def get_stock_summary(data):
    latest_price = data["Close"].iloc[-1]
    highest_price = data["Close"].max()
    lowest_price = data["Close"].min()
    average_price = data["Close"].mean()
    percent_change = calculate_percent_change(data)

    if percent_change > 2:
        trend = "Uptrend"
    elif percent_change < -2:
        trend = "Downtrend"
    else:
        trend = "Sideways"

    signal_info = get_stock_signal(data)

    return {
        "latest_price": round(latest_price, 2),
        "highest_price": round(highest_price, 2),
        "lowest_price": round(lowest_price, 2),
        "average_price": round(average_price, 2),
        "percent_change": percent_change,
        "trend": trend,
        "ma7": signal_info["ma7"],
        "ma20": signal_info["ma20"],
        "signal": signal_info["signal"],
        "confidence": signal_info["confidence"],
        "reason": signal_info["reason"]
    }


def compare_performance(stocks):
    performance = {}

    for symbol, data in stocks.items():
        percent_change = calculate_percent_change(data)
        performance[symbol] = percent_change

    best_stock = max(performance, key=performance.get)
    worst_stock = min(performance, key=performance.get)

    return {
        "performance": performance,
        "best_stock": best_stock,
        "worst_stock": worst_stock
    }