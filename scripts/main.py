import os
import json
import get_financials
import pandas as pd
import time
from upload import upload_s3
from util import get_file
import io
from io import StringIO
import boto3
from datetime import datetime

def main():
    # get environment variables
    bucket = 'fin-fj'
    input_file_prefix = 'input'
    output_file_prefix = 'output'

    # read stock information
    df_stocks = get_file(bucket, input_file_prefix, 'sp500_tickers.csv')

    # print number of total stocks and start timer
    st = time.time()
    print(f'Total stocks before filtering: {df_stocks.shape[0]}')

    # drop stocks with no industry or sectory and blank check companies and print total stocks after filtering
    df_stocks = df_stocks.dropna(subset = ['Sector','Industry'])
    df_stocks = df_stocks[df_stocks['Industry'] != 'Blank Checks']
    print(f'Total stocks after Industry and Sector filtering: {df_stocks.shape[0]}')
    # df_stocks = df_stocks.head(10)

    # get PE ratio
    df_stocks['PERatio'] = df_stocks['Symbol'].apply(lambda x: get_financials.get_pe_ratio(x))

    # limit to stocks with positive PE ratio
    df_stocks['PERatioFilter'] = df_stocks['PERatio'].apply(lambda x: True if x > 0 and x < 50 else False)
    print(f'PE Filter Created')

    # get PB ratio
    df_stocks['PBRatio'] = df_stocks['Symbol'].apply(lambda x: get_financials.get_pb_ratio(x))

    # get sector average PB ratio filtering
    sector_avg_pb = df_stocks.groupby('Sector').agg({'PBRatio':'mean'}).reset_index().rename(columns = {'PBRatio':'SectorAvgPBRatio'})
    df_stocks = df_stocks.merge(sector_avg_pb, on = 'Sector', how = 'left')
    df_stocks['SectorAvgPBRatio'] = round(df_stocks['SectorAvgPBRatio'],2)
    df_stocks['PBRatioFilter'] = df_stocks.apply(lambda x: True if (x['PBRatio'] < 10) or (x['PBRatio'] < x['SectorAvgPBRatio']) else False, axis = 1)
    print(f'PB Filter Created')

    # get gross and net margins
    df_stocks['grossMargins'] = df_stocks['Symbol'].apply(lambda x: get_financials.get_gross_margin(x))
    df_stocks['netMargins'] = df_stocks['Symbol'].apply(lambda x: get_financials.get_net_margin(x))

    # filter on margins
    df_stocks['MarginFilter'] = df_stocks.apply(lambda x: True if x['grossMargins'] > 0.2 and x['netMargins'] > 0.1 else False, axis = 1)
    print(f'Margin Filter Created')

    # get return on assets and equity
    df_stocks['returnOnAssets'] = df_stocks['Symbol'].apply(lambda x: get_financials.get_return_on_assets(x))
    df_stocks['returnOnEquity'] = df_stocks['Symbol'].apply(lambda x: get_financials.get_return_on_equity(x))

    # filter on return on equity
    df_stocks['RoEFilter'] = df_stocks.apply(lambda x: True if x['returnOnEquity'] > 0.05 and x['returnOnAssets'] > 0.05 else False, axis = 1)
    print(f'RoE Filter Created')

    # get revenue and earnings growth
    # df_stocks['revenueGrowth'] = df_stocks['Symbol'].apply(lambda x: get_financials.get_revenue_growth(x))
    # df_stocks['earningsGrowth'] = df_stocks['Symbol'].apply(lambda x: get_financials.get_earnings_growth(x))
    # print('Growth Calculated')

    # get annual and quarterly earnings from last four quarters
    df_stocks[['quarterly_earnings-1', 'quarterly_earnings-2', 'quarterly_earnings-3', 'quarterly_earnings-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_quarterly_income(x)))
    df_stocks[['annual_earnings-1', 'annual_earnings-2', 'annual_earnings-3', 'annual_earnings-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_annual_income(x)))
    print('Earnings Calculated')

    # get annual and quarterly revenue from last four quarters
    df_stocks[['quarterly_revenue-1', 'quarterly_revenue-2', 'quarterly_revenue-3', 'quarterly_revenue-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_quarterly_revenue(x)))
    df_stocks[['annual_revenue-1', 'annual_revenue-2', 'annual_revenue-3', 'annual_revenue-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_annual_revenue(x)))
    print('Revenue Calculated')

    # # get annual and quarterly r&d from last four quarters
    df_stocks[['quarterly_randd-1', 'quarterly_randd-2', 'quarterly_randd-3', 'quarterly_randd-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_quarterly_randd(x)))
    df_stocks[['annual_randd-1', 'annual_randd-2', 'annual_randd-3', 'annual_randd-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_annual_randd(x)))
    print('R&D Calculated')

    # get annual and quarterly debt from last four periods
    df_stocks[['quarterly_debt-1', 'quarterly_debt-2', 'quarterly_debt-3', 'quarterly_debt-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_quarterly_debt(x)))
    df_stocks[['annual_debt-1', 'annual_debt-2', 'annual_debt-3', 'annual_debt-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_annual_debt(x)))
    print('Debt Calculated')

    # get annual and quarterly retained earnings from last four periods
    df_stocks[['quarterly_retained_earnings-1', 'quarterly_retained_earnings-2', 'quarterly_retained_earnings-3', 'quarterly_retained_earnings-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_quarterly_retained_earnings(x)))
    df_stocks[['annual_retained_earnings-1', 'annual_retained_earnings-2', 'annual_retained_earnings-3', 'annual_retained_earnings-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_annual_retained_earnings(x)))
    print('Retained Earnings Calculated')

    # get annual and quarterly capital expenditure from last four periods
    df_stocks[['quarterly_cap_ex-1', 'quarterly_cap_ex-2', 'quarterly_cap_ex-3', 'quarterly_cap_ex-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_quarterly_cap_ex(x)))
    df_stocks[['annual_cap_ex-1', 'annual_cap_ex-2', 'annual_cap_ex-3', 'annual_cap_ex-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_annual_cap_ex(x)))
    print('Capex Calculated')

    # get shareholder's equity
    df_stocks[['quarterly_equity-1', 'quarterly_equity-2', 'quarterly_equity-3', 'quarterly_equity-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_quarterly_equity(x)))
    df_stocks[['annual_equity-1', 'annual_equity-2', 'annual_equity-3', 'annual_equity-4']] = df_stocks['Symbol']\
    .apply(lambda x: pd.Series(get_financials.get_annual_equity(x)))
    print('Equity Calculated')

    # calculate debt to equity
    df_stocks['debtToEquity'] = round(df_stocks['quarterly_equity-1']/df_stocks['quarterly_debt-1'],2)

    # calculate capex to net income
    df_stocks['capExToIncome'] = round(df_stocks['quarterly_cap_ex-1']/df_stocks['quarterly_earnings-1'],2)

    # calculate fundamentals ranking
    df_stocks['returnOnAssets_rank'] = df_stocks['returnOnAssets'].apply(lambda x: 1 if x > 0.2 else 2 if x > 0.1 else 3)
    df_stocks['returnOnEquity_rank'] = df_stocks['returnOnEquity'].apply(lambda x: 1 if x > 0.2 else 2 if x > 0.1 else 3)
    df_stocks['debtToEquity_rank'] = df_stocks.apply(lambda x: 1 if x['debtToEquity'] < 1 else 2 if x['debtToEquity'] < 2 else 3, axis = 1)
    df_stocks['capExToIncome_rank'] = df_stocks['capExToIncome'].apply(lambda x: 1 if x < 0.25 else 2 if x < 0.5 else 3)
    print('Ranks Calculated')

    # sort on final rank
    df_stocks['final_rank'] = df_stocks['returnOnAssets_rank'] + df_stocks['returnOnEquity_rank'] + \
                        df_stocks['debtToEquity_rank'] + df_stocks['capExToIncome_rank']
    df_stocks.sort_values('final_rank', ascending = True, inplace = True)

    # add run date
    df_stocks['run_date'] = datetime.today().strftime('%Y-%m-%d')

    # print elapsed time
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', round(elapsed_time,2), 'seconds')

    # upload output to output directory
    upload_s3(bucket, output_file_prefix, f"sp500/{datetime.today().strftime('%Y-%m-%d')}/sp500_tickers.csv", df_stocks)
    print(f'{df_stocks.shape[0]} Stocks Saved to S3 Bucket')

if __name__ == '__main__':
    main()
