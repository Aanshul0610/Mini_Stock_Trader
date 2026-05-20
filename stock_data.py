import yfinance as yf


def get_stock_data(symbol, period="1mo", interval="1d"):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period, interval=interval)

    if data.empty:
        raise ValueError(f"No data found for {symbol}. Please check the ticker symbol.")

    return data


def get_multiple_stocks(symbols, period="1mo", interval="1d"):
    stock_library = {}

    for symbol in symbols:
        try:
            data = get_stock_data(symbol, period, interval)
            stock_library[symbol] = data

        except ValueError as error:
            print(error)

    return stock_library