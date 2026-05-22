from stock_data import get_stock_data, get_multiple_stocks
from analysis import get_stock_summary, compare_performance


def clean_symbols(user_input):
    symbols = user_input.upper().replace(" ", "").split(",")

    clean_list = []

    for symbol in symbols:
        if symbol != "":
            clean_list.append(symbol)

    return clean_list


def print_stock_summary(symbol, summary):
    print(f"\n===== {symbol} SUMMARY =====")
    print(f"Latest Price: ${summary['latest_price']}")
    print(f"Highest Close: ${summary['highest_price']}")
    print(f"Lowest Close: ${summary['lowest_price']}")
    print(f"Average Close: ${summary['average_price']}")
    print(f"Percent Change: {summary['percent_change']}%")
    print(f"Trend: {summary['trend']}")
    print(f"7-Day Moving Average: ${summary['ma7']}")
    print(f"20-Day Moving Average: ${summary['ma20']}")
    print(f"Signal: {summary['signal']}")
    print(f"Confidence: {summary['confidence']}")
    print(f"Reason: {summary['reason']}")


def view_one_stock():
    symbol = input("Enter a stock ticker: ").upper().strip()

    if symbol == "":
        print("You did not enter a ticker.")
        return

    try:
        data = get_stock_data(symbol)
        summary = get_stock_summary(data)
        print_stock_summary(symbol, summary)

    except Exception as error:
        print(f"Error: {error}")


def view_multiple_stocks():
    user_input = input("Enter stock tickers separated by commas: ")

    symbols = clean_symbols(user_input)

    if len(symbols) == 0:
        print("You did not enter any valid tickers.")
        return

    stocks = get_multiple_stocks(symbols)

    for symbol, data in stocks.items():
        summary = get_stock_summary(data)
        print_stock_summary(symbol, summary)


def compare_stocks():
    user_input = input("Enter stock tickers separated by commas: ")

    symbols = clean_symbols(user_input)

    if len(symbols) < 2:
        print("Please enter at least two stock tickers.")
        return

    stocks = get_multiple_stocks(symbols)

    if len(stocks) < 2:
        print("Not enough valid stocks to compare.")
        return

    comparison = compare_performance(stocks)

    print("\n===== PERFORMANCE COMPARISON =====")

    for symbol, percent_change in comparison["performance"].items():
        print(f"{symbol}: {percent_change}%")

    print(f"\nBest Performer: {comparison['best_stock']}")
    print(f"Worst Performer: {comparison['worst_stock']}")


def main():
    while True:
        print("\n===== MINI STOCK TRACKER =====")
        print("1. View One Stock")
        print("2. View Multiple Stocks")
        print("3. Compare Stocks")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            view_one_stock()

        elif choice == "2":
            view_multiple_stocks()

        elif choice == "3":
            compare_stocks()

        elif choice == "4":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()