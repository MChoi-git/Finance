# This is a test file to practice polygon.io REST API

from polygon import RESTClient

def main():
    key = 'PjeqU9zauMH9o49WYWurfZslqfY8HpF7'
    with RESTClient(key) as client:
        #resp = client.stocks_equities_daily_open_close("AAPL","2018-03-02")
        #print(f"on: {resp.from_} Apple opened at {resp.open} and closed at {resp.close}")
        resp = client.reference_stock_financials("MSFT",limit=1,type='Q')
        # Note that Q results are off by 1 fiscal year, bug currently being worked on
        print(f"MSFT market cap is {resp.results[0].get('marketCapitalization')} as reported on {resp.results[0].get('reportPeriod')}.")
        custom_limit=100
        resp = client.reference_stock_financials("MSFT",limit=100,type='Q')
        for i in range(custom_limit):
            print('*'*50)
            print(f"MSFT market cap is {resp.results[i].get('marketCapitalization')} as reported on {resp.results[i].get('reportPeriod')}.")
            print(f"MSFT debt to equity ratio is {resp.results[i].get('debtToEquityRatio')} as reported on {resp.results[i].get('reportPeriod')}.")
            print(f"MSFT divident yield is {resp.results[i].get('dividendYield')} as reported on {resp.results[i].get('reportPeriod')}.")
            print(f"MSFT gross profit is {resp.results[i].get('grossProfit')} as reported on {resp.results[i].get('reportPeriod')}.")
            print(f"MSFT net income is {resp.results[i].get('netIncome')} as reported on {resp.results[i].get('reportPeriod')}.")
            print(f"MSFT revenues in USD is {resp.results[i].get('revenuesUSD')} as reported on {resp.results[i].get('reportPeriod')}.")
            print(f"MSFT operating income is {resp.results[i].get('operatingIncome')} as reported on {resp.results[i].get('reportPeriod')}.")
            print('*'*50)
if __name__ == '--main__':
    main()
