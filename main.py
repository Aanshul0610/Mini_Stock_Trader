from stock_data import get_stock_data, get_multiple_stocks


def clean_symbols(user_input):
    symbols = user_input.upper().replace(" ", "").split(",")

    clean_list = []

    for symbol in symbols:
        if symbol != "":
            clean_list.append(symbol)

    return clean_list


def test_single_stock():
    data = get_stock_data("AAPL")

    print("===== AAPL TEST DATA =====")
    print(data.head())
    print(data.tail())


def view_multiple_stocks():
    user_input = input("Enter stock tickers separated by commas: ")

    symbols = clean_symbols(user_input)

    if len(symbols) == 0:
        print("You did not enter any valid tickers.")
    else:
        stocks = get_multiple_stocks(symbols)

        for symbol, data in stocks.items():
            print(f"\n===== {symbol} =====")
            print(data.head())


def main():
    test_single_stock()
    view_multiple_stocks()


if __name__ == "__main__":
    main()