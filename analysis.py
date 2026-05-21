"""
in this program we analyze the raw data we acquire from the yfinance library
and analyze the percent change and so on
"""
#create the calculate percentage problem
def calculate_percent_change(df):
    first_price=df['Close'].iloc[0]
    last_price=df['Close'].iloc[-1]
    change=last_price-first_price
    percent_change=(change/last_price)*100
    return round(percent_change,2)
def get_stock_summary(data):
    latest_price=data['Close'].iloc[-1]
    highest_price=data["Close"].max()
    lowest_price=data["Close"].min()
    average_price=data["Close"].mean()
    percent_change=calculate_percent_change(data)
    if percent_change>2:
        trend="Uptrend"
    elif percent_change<-2:
        trend="Downtrend"
    else:
        trend="Normal"
    return{
        "latest_price":latest_price,
        "highest_price":highest_price,
        "lowest_price":lowest_price,
        "average_price":average_price,
        "percent_change":percent_change,
        "trend":trend,
        "data":data
    }

