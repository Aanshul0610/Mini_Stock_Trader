import streamlit as st

from stock_data import get_stock_data, get_multiple_stocks
from analysis import get_stock_summary, compare_performance
from watchlist import load_watchlist, add_to_watchlist, remove_from_watchlist
from news import get_stock_news
from sentiment import analyze_sentiment


st.set_page_config(
    page_title="Mini Stock Tracker",
    layout="wide"
)


def show_stock_summary(symbol, summary):
    st.subheader(f"{symbol} Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Latest Price", f"${summary['latest_price']}")
    col2.metric("Percent Change", f"{summary['percent_change']}%")
    col3.metric("Trend", summary["trend"])

    col4, col5, col6 = st.columns(3)

    col4.metric("Highest Close", f"${summary['highest_price']}")
    col5.metric("Lowest Close", f"${summary['lowest_price']}")
    col6.metric("Average Close", f"${summary['average_price']}")

    col7, col8, col9 = st.columns(3)

    col7.metric("7-Day MA", f"${summary['ma7']}")
    col8.metric("20-Day MA", f"${summary['ma20']}")
    col9.metric("Signal", summary["signal"])

    st.write(f"**Confidence:** {summary['confidence']}")
    st.write(f"**Reason:** {summary['reason']}")


def show_stock_chart(data):
    chart_data = data[["Close"]].copy()
    chart_data["MA7"] = data["Close"].rolling(window=7).mean()
    chart_data["MA20"] = data["Close"].rolling(window=20).mean()

    st.line_chart(chart_data)


def show_news_and_sentiment(symbol):
    st.subheader(f"{symbol} News & Sentiment")

    try:
        news_items = get_stock_news(symbol, limit=5)

        if len(news_items) == 0:
            st.info("No news found for this ticker.")
            return

        total_score = 0

        for item in news_items:
            title = item["title"]
            publisher = item["publisher"]
            link = item["link"]

            sentiment = analyze_sentiment(title)
            total_score += sentiment["score"]

            st.write("---")
            st.write(f"**{title}**")
            st.write(f"Publisher: {publisher}")
            st.write(f"Sentiment: **{sentiment['label']}**")
            st.write(f"Sentiment Score: {sentiment['score']}")

            if link != "":
                st.link_button("Read Article", link)

        average_score = total_score / len(news_items)

        if average_score > 0.05:
            overall_sentiment = "Positive"
        elif average_score < -0.05:
            overall_sentiment = "Negative"
        else:
            overall_sentiment = "Neutral"

        st.write("---")
        st.metric("Overall News Sentiment", overall_sentiment)
        st.write(f"Average Sentiment Score: {round(average_score, 3)}")

    except Exception as error:
        st.error(f"Could not load news: {error}")


st.title("Mini Stock Tracker")
st.write("Analyze stocks, compare performance, save a watchlist, and check news sentiment.")


# ---------------- SIDEBAR WATCHLIST ----------------

st.sidebar.header("Watchlist")

watchlist = load_watchlist()

if len(watchlist) == 0:
    st.sidebar.write("No stocks saved yet.")
else:
    st.sidebar.write("Saved stocks:")

    for saved_symbol in watchlist:
        st.sidebar.write(f"- {saved_symbol}")

st.sidebar.divider()

watchlist_symbol = st.sidebar.text_input("Ticker for watchlist")

col_add, col_remove = st.sidebar.columns(2)

with col_add:
    if st.button("Add"):
        add_to_watchlist(watchlist_symbol)
        st.rerun()

with col_remove:
    if st.button("Remove"):
        remove_from_watchlist(watchlist_symbol)
        st.rerun()


# ---------------- TABS ----------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Single Stock",
    "Multiple Stocks",
    "Compare Stocks",
    "News Sentiment"
])


# ---------------- SINGLE STOCK TAB ----------------

with tab1:
    symbol = st.text_input("Enter stock ticker", value="AAPL").upper().strip()

    if st.button("Analyze Stock"):
        if symbol == "":
            st.error("Please enter a ticker.")
        else:
            try:
                data = get_stock_data(symbol)
                summary = get_stock_summary(data)

                show_stock_summary(symbol, summary)

                st.subheader("Price Chart")
                show_stock_chart(data)

                st.subheader("Recent Data")
                st.dataframe(data.tail())

                show_news_and_sentiment(symbol)

            except Exception as error:
                st.error(f"Error: {error}")


# ---------------- MULTIPLE STOCKS TAB ----------------

with tab2:
    tickers_input = st.text_input(
        "Enter stock tickers separated by commas",
        value="AAPL, MSFT, TSLA"
    )

    if st.button("Analyze Multiple Stocks"):
        symbols = []

        for symbol in tickers_input.upper().replace(" ", "").split(","):
            if symbol != "":
                symbols.append(symbol)

        if len(symbols) == 0:
            st.error("Please enter at least one ticker.")
        else:
            stocks = get_multiple_stocks(symbols)

            for symbol, data in stocks.items():
                summary = get_stock_summary(data)
                show_stock_summary(symbol, summary)

                with st.expander(f"Show chart for {symbol}"):
                    show_stock_chart(data)

                with st.expander(f"Show news sentiment for {symbol}"):
                    show_news_and_sentiment(symbol)


# ---------------- COMPARE STOCKS TAB ----------------

with tab3:
    compare_input = st.text_input(
        "Enter stocks to compare",
        value="AAPL, MSFT, TSLA"
    )

    if st.button("Compare"):
        symbols = []

        for symbol in compare_input.upper().replace(" ", "").split(","):
            if symbol != "":
                symbols.append(symbol)

        if len(symbols) < 2:
            st.error("Please enter at least two tickers.")
        else:
            stocks = get_multiple_stocks(symbols)

            if len(stocks) < 2:
                st.error("Not enough valid stocks to compare.")
            else:
                comparison = compare_performance(stocks)

                st.subheader("Performance Comparison")

                for symbol, percent_change in comparison["performance"].items():
                    st.write(f"**{symbol}:** {percent_change}%")

                st.success(f"Best Performer: {comparison['best_stock']}")
                st.warning(f"Worst Performer: {comparison['worst_stock']}")


# ---------------- NEWS SENTIMENT TAB ----------------

with tab4:
    news_symbol = st.text_input("Enter ticker for news sentiment", value="AAPL").upper().strip()

    if st.button("Get News Sentiment"):
        if news_symbol == "":
            st.error("Please enter a ticker.")
        else:
            show_news_and_sentiment(news_symbol)