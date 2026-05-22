import matplotlib.pyplot as plt



def plot_stock_chart(data, symbol):
    data = data.copy()

    data["MA7"] = data["Close"].rolling(window=7).mean()
    data["MA20"] = data["Close"].rolling(window=20).mean()

    plt.figure(figsize=(10, 5))

    plt.plot(data.index, data["Close"], label="Close Price")
    plt.plot(data.index, data["MA7"], label="7-Day Moving Average")
    plt.plot(data.index, data["MA20"], label="20-Day Moving Average")

    plt.title(f"{symbol} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.show()