# get latest company financials using api calls
import yfinance as yf
import time

def get_pe_ratio(ticker):
    time.sleep(0.3)
    try:
        pe_ratio = yf.Ticker(ticker).info['previousClose'] / yf.Ticker(ticker).info['trailingEps']
    except:
        pe_ratio = None
        return pe_ratio
    return round(pe_ratio,2)

def get_pb_ratio(ticker):
    time.sleep(0.3)
    try:
        pb_ratio = yf.Ticker(ticker).info['priceToBook']
    except:
        pb_ratio = None
        return pb_ratio
    return round(pb_ratio,2)

def get_gross_margin(ticker):
    time.sleep(0.3)
    try:
        gross_margin = yf.Ticker(ticker).info['grossMargins']
    except:
        gross_margin = None
        return gross_margin
    return round(gross_margin,3)

def get_net_margin(ticker):
    try:
        profit_margin = yf.Ticker(ticker).info['profitMargins']
    except:
        profit_margin = None
        return profit_margin
    return round(profit_margin,3)

def get_return_on_assets(ticker):
    time.sleep(0.3)
    try:
        roa = yf.Ticker(ticker).info['returnOnAssets']
    except:
        roa = None
        return roa
    return round(roa,3)

def get_return_on_equity(ticker):
    time.sleep(0.3)
    try:
        roe = yf.Ticker(ticker).info['returnOnEquity']
    except:
        roe = None
        return roe
    return round(roe,3)

def get_revenue_growth(ticker):
    time.sleep(0.3)
    try:
        revenue_growth = yf.Ticker(ticker).info['revenueGrowth']
    except:
        revenue_growth = None
        return revenue_growth
    return round(revenue_growth,3)

def get_earnings_growth(ticker):
    time.sleep(0.3)
    try:
        earnings_growth = yf.Ticker(ticker).info['earningsGrowth']
    except:
        earnings_growth = None
        return earnings_growth
    return round(earnings_growth,3)

def get_quarterly_income(ticker):
    time.sleep(0.3)
    try:
        quarterly_income = yf.Ticker(ticker).quarterly_incomestmt.loc['Net Income',:].values[:4]
    except:
        quarterly_income = None
        return quarterly_income
    return quarterly_income

def get_annual_income(ticker):
    time.sleep(0.3)
    try:
        annual_income = yf.Ticker(ticker).incomestmt.loc['Net Income',:].values[:4]
    except:
        annual_income = None
        return annual_income
    return annual_income

def get_quarterly_revenue(ticker):
    time.sleep(0.3)
    try:
        quarterly_revenue = yf.Ticker(ticker).quarterly_incomestmt.loc['Total Revenue',:].values[:4]
    except:
        quarterly_revenue = None
        return quarterly_revenue
    return quarterly_revenue

def get_annual_revenue(ticker):
    time.sleep(0.3)
    try:
        annual_revenue = yf.Ticker(ticker).incomestmt.loc['Total Revenue',:].values[:4]
    except:
        annual_revenue = None
        return annual_revenue
    return annual_revenue

def get_quarterly_randd(ticker):
    time.sleep(0.3)
    try:
        quarterly_randd = yf.Ticker(ticker).quarterly_incomestmt.loc['Research And Development',:].values[:4]
    except:
        quarterly_randd = None
        return quarterly_randd
    return quarterly_randd

def get_annual_randd(ticker):
    time.sleep(0.3)
    try:
        annual_randd = yf.Ticker(ticker).incomestmt.loc['Research And Development',:].values[:4]
    except:
        annual_randd = None
        return annual_randd
    return annual_randd

def get_quarterly_debt(ticker):
    time.sleep(0.3)
    try:
        quarterly_debt = yf.Ticker(ticker).quarterly_balancesheet.loc['Total Debt',:].values[:4]
    except:
        quarterly_debt = None
        return quarterly_debt
    return quarterly_debt

def get_annual_debt(ticker):
    time.sleep(0.3)
    try:
        annual_debt = yf.Ticker(ticker).balancesheet.loc['Total Debt',:].values[:4]
    except:
        annual_debt = None
        return annual_debt
    return annual_debt

def get_quarterly_retained_earnings(ticker):
    time.sleep(0.3)
    try:
        quarterly_retained_earnings = yf.Ticker(ticker).quarterly_balancesheet.loc['Retained Earnings',:].values[:4]
    except:
        quarterly_retained_earnings = None
        return quarterly_retained_earnings
    return quarterly_retained_earnings

def get_annual_retained_earnings(ticker):
    time.sleep(0.3)
    try:
        annual_retained_earnings = yf.Ticker(ticker).balancesheet.loc['Retained Earnings',:].values[:4]
    except:
        annual_retained_earnings = None
        return annual_retained_earnings
    return annual_retained_earnings

def get_quarterly_cap_ex(ticker):
    time.sleep(0.3)
    try:
        quarterly_cap_ex = yf.Ticker(ticker).quarterly_cashflow.loc['Capital Expenditure',:].values[:4]
    except:
        quarterly_cap_ex = None
        return quarterly_cap_ex
    return quarterly_cap_ex

def get_annual_cap_ex(ticker):
    time.sleep(0.3)
    try:
        annual_cap_ex = yf.Ticker(ticker).cashflow.loc['Capital Expenditure',:].values[:4]
    except:
        annual_cap_ex = None
        return annual_cap_ex
    return annual_cap_ex

def get_quarterly_equity(ticker):
    time.sleep(0.3)
    try:
        quarterly_equity = yf.Ticker(ticker).quarterly_balancesheet.loc['Stockholders Equity',:].values[:4]
    except:
        quarterly_equity = None
        return quarterly_equity
    return quarterly_equity

def get_annual_equity(ticker):
    time.sleep(0.3)
    try:
        annual_equity = yf.Ticker(ticker).balancesheet.loc['Stockholders Equity',:].values[:4]
    except:
        annual_equity = None
        return annual_equity
    return annual_equity

# print(f"AAPL PE Ratio: {get_pe_ratio('AAPL')}")
# print(f"AAPL PB Ratio: {get_pb_ratio('AAPL')}")