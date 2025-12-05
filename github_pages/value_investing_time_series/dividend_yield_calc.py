import yfinance as yf
import pandas as pd
from datetime import datetime
import time
import random

# Full S&P 500 tickers (503 as of Dec 2025) — no duplicates
tickers = sorted(list({
    'A','AAL','AAPL','ABBV','ABNB','ABT','ACGL','ACN','ADBE','ADI','ADM','ADP','ADSK','AEE','AEP','AES','AFL','AIG','AIZ',
    'AJG','AKAM','ALB','ALGN','ALL','ALLE','AMAT','AMD','AME','AMGN','AMP','AMT','AMZN','ANET','ANSS','AON','AOS','APA',
    'APD','APH','APTV','ARE','ATO','AVB','AVGO','AWK','AXON','AXP','AZO','BA','BAC','BAX','BBWI','BBY','BDX','BEN','BG',
    'BIIB','BIO','BK','BKNG','BKR','BLK','BMY','BR','BRO','BSX','BWA','BX','BXP','C','CAG','CAH','CARR','CAT','CB','CBRE',
    'CCI','CCL','CDNS','CDW','CE','CEG','CF','CFG','CHD','CHRW','CHTR','CI','CINF','CL','CLX','CMA','CME','CMG','CMI','CMS',
    'CNC','CNP','COF','COO','COP','COR','COST','CPAY','CPB','CPRT','CPT','CRL','CRM','CSCO','CSGP','CSX','CTAS','CTLT','CTRA',
    'CTSH','CVS','CVX','CZR','D','DAL','DAY','DE','DECK','DFS','DG','DGX','DHI','DHR','DIS','DLR','DLTR','DOC','DOV','DPZ',
    'DRI','DTE','DUK','DVA','DVN','DXCM','EA','EBAY','ECL','ED','EFX','EG','EIX','EL','ELV','EMR','ENPH','EOG','EPAM','EQIX',
    'EQR','EQT','ES','ESS','ETN','ETR','ETSY','EVRG','EW','EXC','EXPD','EXPE','EXR','F','FANG','FAST','FDS','FDX','FE','FFIV',
    'FI','FIS','FITB','FMC','FOX','FOXA','FRT','FSLR','FTNT','FTV','GD','GE','GEHC','GEN','GEV','GILD','GIS','GL','GLW','GM',
    'GNRC','GOOG','GOOGL','GPC','GPN','GRMN','GS','GWW','HAL','HAS','HBAN','HCA','HD','HES','HIG','HII','HLT','HOLX','HON',
    'HPE','HPQ','HRL','HSIC','HST','HSY','HUBB','HUM','HWM','IBM','ICE','IDXX','IEX','ILMN','INCY','INTC','INTU','INVH','IP',
    'IPG','IQV','IR','IRM','ISRG','IT','ITW','IVZ','J','JBHT','JBL','JCI','JKHY','JNJ','JNPR','JPM','K','KDP','KEY','KEYS',
    'KHC','KIM','KLAC','KMB','KMI','KMX','KO','KR','KVUE','L','LDOS','LEN','LH','LHX','LKQ','LLY','LMT','LNT','LOW','LRCX',
    'LULU','LUV','LVS','LW','LYV','MA','MAA','MAR','MAS','MCD','MCHP','MCK','MCO','MDLZ','MDT','MET','META','MGM','MHK','MKC',
    'MKTX','MMC','MMM','MNST','MO','MOH','MOS','MPC','MPWR','MRK','MRNA','MRO','MS','MSCI','MSFT','MSI','MTB','MTCH','MTD',
    'MU','NCLH','NDAQ','NDSN','NEE','NEM','NET','NFLX','NI','NKE','NOC','NOW','NRG','NSC','NTAP','NTRS','NVDA','NVR','NWS',
    'NWSA','NXPI','O','ODFL','OKE','OMC','ON','ORCL','ORLY','OTIS','OXY','PANW','PARA','PAYC','PAYX','PCAR','PCG','PEG','PEP',
    'PFE','PFG','PG','PGR','PH','PHM','PKG','PLD','PM','PNC','PNR','PNW','PODD','POOL','PPL','PRU','PSA','PSX','PTC','PWR',
    'PYPL','QCOM','QRVO','RCL','REG','REGN','RF','RHI','RJF','RL','RMD','ROK','ROL','ROP','ROST','RSG','RTX','RVTY','SBAC',
    'SBUX','SCHW','SJM','SLB','SMCI','SNA','SNPS','SO','SOLV','SPG','SPGI','SRE','STE','STLD','STT','STX','STZ','SWK','SWKS',
    'SYF','SYK','SYY','T','TAP','TDG','TDY','TECH','TEL','TER','TFC','TFX','TGT','TJX','TMO','TMUS','TPR','TRGP','TRMB','TROW',
    'TRV','TSCO','TSLA','TSN','TT','TTWO','TXN','TXT','TYL','UAL','UBER','UDR','UHS','ULTA','UNH','UNP','UPS','URI','USB','V',
    'VFC','VICI','VLO','VLTO','VRSK','VRSN','VRTX','VTR','VTRS','VZ','WAB','WAT','WBA','WBD','WDC','WEC','WELL','WFC','WHR',
    'WM','WMB','WMT','WRB','WST','WTW','WY','WYNN','XEL','XOM','XYL','YUM','ZBH','ZBRA','ZTS',
    'APP','HOOD','EME','DASH','TKO','WSM','EXE','IBKR'
}))

def get_sp500_dividends_safe():
    start_date = '2015-01-01'
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    all_dividends = []
    summary = []
    
    print(f'\\nStarting safe download of {len(tickers)} S&P 500 stocks (≈17 minutes total)...\\n')
    
    for i, ticker in enumerate(tickers):
        # Polite delay: 1.8–2.3 seconds between requests
        if i > 0:
            time.sleep(1.8 + random.uniform(0, 0.5))
        
        print(f'[{i+1:3d}/{len(tickers)}] Fetching {ticker} ... ', end='')
        
        try:
            stock = yf.Ticker(ticker)
            
            # 10-year dividend history
            hist = stock.dividends.loc[start_date:end_date]
            if len(hist) > 0:
                df = hist.to_frame().reset_index()
                df['Ticker'] = ticker
                df = df.rename(columns={'Dividends': 'Amount', 'Date': 'Ex_Dividend_Date'})
                df = df[['Ticker', 'Ex_Dividend_Date', 'Amount']]
                all_dividends.append(df)
            
            # Current TTM dividend & yield
            ttm_div = stock.dividends[-365:].sum()
            price = stock.info.get('currentPrice') or stock.info.get('regularMarketPrice')
            name  = stock.info.get('longName', ticker)
            
            yield_pct = round((ttm_div / price * 100), 3) if price and price > 0 and ttm_div > 0 else 0.0
            
            company_name = ' '.join(name.split()[:3]) if name else ticker
            
            summary.append({
                'Ticker': ticker,
                'Company': company_name,
                'Current_Price': round(price, 2) if price else None,
                'TTM_Dividend_per_Share': round(ttm_div, 4),
                'Dividend_Yield_%': yield_pct
            })
            print('done')
            
        except Exception as e:
            print(f'failed ({e})')
            continue
    
    # Final data frames
    dividends_df = pd.concat(all_dividends, ignore_index=True) if all_dividends else pd.DataFrame()
    summary_df = pd.DataFrame(summary)
    summary_df = summary_df.sort_values('Dividend_Yield_%', ascending=False).reset_index(drop=True)
    
    print('\\nCompleted! Ready for R.')
    return dividends_df, summary_df

# Run it (this will take ~17 minutes)
dividends_10y, yield_summary = get_sp500_dividends_safe()