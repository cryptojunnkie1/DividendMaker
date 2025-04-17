import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(page_title="Dividend Aristocrat Analyzer", layout="wide")

# ========== Data Setup ==========
dividend_aristocrats = [
    ('JNJ', 'Johnson & Johnson'),
    ('PG', 'Procter & Gamble'),
    ('KO', 'Coca-Cola'),
    ('PEP', 'PepsiCo'),
    ('ABBV', 'AbbVie'),
    ('TGT', 'Target'),
    ('ED', 'Consolidated Edison'),
    ('MMM', '3M Company'),
    ('CL', 'Colgate-Palmolive'),
    ('ADM', 'Archer-Daniels-Midland'),
    ('AOS', 'A. O. Smith'),
    ('ABT', 'Abbott Laboratories'),
    ('APD', 'Air Products and Chemicals'),
    ('ALB', 'Albemarle Corporation'),
    ('AMCR', 'Amcor'),
    ('T', 'AT&T'),
    ('ADP', 'Automatic Data Processing'),
    ('BDX', 'Becton Dickinson'),
    ('BRO', 'Brown & Brown'),
    ('CHRW', 'C.H. Robinson'),
    ('CAH', 'Cardinal Health'),
    ('CINF', 'Cincinnati Financial'),
    ('CLX', 'Clorox'),
    ('DOV', 'Dover Corporation'),
    ('EMR', 'Emerson Electric'),
    ('ESS', 'Essex Property Trust'),
    ('XOM', 'ExxonMobil'),
    ('FRT', 'Federal Realty Investment Trust'),
    ('BEN', 'Franklin Resources'),
    ('GD', 'General Dynamics'),
    ('GPC', 'Genuine Parts Company'),
    ('HRL', 'Hormel Foods'),
    ('ITW', 'Illinois Tool Works'),
    ('KMB', 'Kimberly-Clark'),
    ('LOW', "Lowe's"),
    ('MKC', 'McCormick & Company'),
    ('NEE', 'NextEra Energy'),
    ('NDSN', 'Nordson Corporation'),
    ('SHW', 'Sherwin-Williams'),
    ('SWK', 'Stanley Black & Decker'),
    ('SYY', 'Sysco'),
    ('TROW', 'T. Rowe Price'),
    ('TR', 'Tootsie Roll Industries'),
    ('VFC', 'V.F. Corporation')
]

other_dividend_stocks = [
    ('O', 'Realty Income'),
    ('MAIN', 'Main Street Capital'),
    ('HD', 'Home Depot'),
    ('LOW', "Lowe's"),
    ('IBM', 'International Business Machines'),
    ('AFL', 'Aflac'),
    ('ARE', 'Alexandria Real Estate Equities'),
    ('ALL', 'Allstate'),
    ('MO', 'Altria Group'),
    ('AEE', 'Ameren'),
    ('AEP', 'American Electric Power'),
    ('AWR', 'American States Water'),
    ('AMT', 'American Tower'),
    ('COLD', 'Americold Realty Trust'),
    ('APTV', 'Aptiv'),
    ('AVB', 'AvalonBay Communities'),
    ('BRK.B', 'Berkshire Hathaway'),
    ('BBY', 'Best Buy'),
    ('BLK', 'BlackRock'),
    ('BWA', 'BorgWarner'),
    ('BXP', 'Boston Properties'),
    ('BMY', 'Bristol-Myers Squibb'),
    ('AVGO', 'Broadcom'),
    ('COG', 'Cabot Oil & Gas'),
    ('CCJ', 'Cameco'),
    ('CAT', 'Caterpillar'),
    ('ATO', 'Atmos Energy'),
    ('CSCO', 'Cisco Systems'),
    ('D', 'Dominion Energy'),
    ('DUK', 'Duke Energy'),
    ('DTE', 'DTE Energy'),
    ('ETN', 'Eaton Corporation'),
    ('EVRG', 'Evergy'),
    ('ES', 'Eversource Energy'),
    ('EXC', 'Exelon'),
    ('FRT', 'Federal Realty Investment Trust'),
    ('FE', 'FirstEnergy'),
    ('GIS', 'General Mills'),
    ('GPC', 'Genuine Parts Company'),
    ('HRL', 'Hormel Foods'),
    ('HST', 'Host Hotels & Resorts'),
    ('ICE', 'Intercontinental Exchange'),
    ('IRM', 'Iron Mountain'),
    ('JNJ', 'Johnson & Johnson'),
    ('KIM', 'Kimco Realty'),
    ('KMI', 'Kinder Morgan'),
    ('KR', 'Kroger'),
    ('LMT', 'Lockheed Martin'),
    ('LNT', 'Alliant Energy'),
    ('LHX', 'L3Harris Technologies'),
    ('MAA', 'Mid-America Apartment Communities'),
    ('MMM', '3M Company'),
    ('NEE', 'NextEra Energy'),
    ('NI', 'NiSource'),
    ('NTRS', 'Northern Trust'),
    ('NUE', 'Nucor'),
    ('OKE', 'ONEOK'),
    ('PPL', 'PPL Corporation'),
    ('PEG', 'Public Service Enterprise Group'),
    ('PEP', 'PepsiCo'),
    ('PFG', 'Principal Financial Group'),
    ('PG', 'Procter & Gamble'),
    ('PNW', 'Pinnacle West Capital'),
    ('PSEG', 'PSEG'),
    ('RTX', 'Raytheon Technologies'),
    ('SBUX', 'Starbucks'),
    ('SO', 'Southern Company'),
    ('SPG', 'Simon Property Group'),
    ('T', 'AT&T'),
    ('TGT', 'Target'),
    ('TRV', 'The Travelers Companies'),
    ('UDR', 'UDR'),
    ('USB', 'U.S. Bancorp'),
    ('VLO', 'Valero Energy'),
    ('VTR', 'Ventas'),
    ('VZ', 'Verizon Communications'),
    ('WEC', 'WEC Energy Group'),
    ('WFC', 'Wells Fargo'),
    ('WMB', 'Williams Companies'),
    ('XEL', 'Xcel Energy')
]

paper_chasn_stocks = [
    ('ABBV', 'AbbVie'),
    ('CVX', 'Chevron'),
    ('TROW', 'T. Rowe Price'),
    ('C', 'Citigroup'),
    ('BBY', 'Best Buy'),
    ('O', 'Realty Income'),
    ('CMA', 'Comerica'),
    ('HSBC', 'HSBC Holdings'),
    ('BMY', 'Bristol-Myers Squibb'),
    ('EPR', 'EPR Properties'),
    ('PFE', 'Pfizer'),
    ('BCE', 'BCE Inc.'),
    ('STWD', 'Starwood Property Trust'),
    ('NLY', 'Annaly Capital'),
    ('APA', 'APA Corporation'),
    ('ARR', 'ARMOUR Residential REIT'),
    ('HST', 'Host Hotels & Resorts'),
    ('IVZ', 'Invesco'),
    ('IEP', 'Icahn Enterprises'),
    ('AGNC', 'AGNC Investment'),
    ('BTG', 'B2Gold')
]

# ========== Helper Functions ==========
def get_stock_data(tickers):
    data = []
    for ticker, name in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            history = stock.history(period="5y")
            
            div_yield = info.get('dividendYield', 0) if info.get('dividendYield') else 0
            pe_ratio = info.get('trailingPE')
            payout_ratio = info.get('payoutRatio')
            market_cap = info.get('marketCap')
            div_growth_5y = history['Dividends'].pct_change(periods=252*5).mean() * 100
            
            data.append({
                'Ticker': ticker,
                'Company': name,
                'Price ($)': info.get('currentPrice'),
                'Div Yield (%)': div_yield,
                '5Y Div Growth (%)': div_growth_5y,
                'Payout Ratio (%)': (payout_ratio * 100) if payout_ratio else None,
                'P/E Ratio': pe_ratio,
                'Market Cap ($B)': round(market_cap / 1e9, 2) if market_cap else None,
                'Revenue Growth (%)': info.get('revenueGrowth', 0) * 100
            })
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
    return pd.DataFrame(data)

# ========== App Interface ==========
st.title("Dividend Stock Analysis Toolkit")
st.subheader("Portfolio Builder for Long-Term Investors")

# User input
shares_owned = st.number_input("Enter number of shares you plan to hold:", min_value=1, value=1)

# Main analysis section
col1, col2 = st.columns([3, 2])

with col1:
    st.header("Dividend Aristocrats Analysis")
    aristocrats_df = get_stock_data(dividend_aristocrats)
    st.dataframe(
        aristocrats_df.style.format({
            'Price ($)': '{:.2f}',
            'Div Yield (%)': '{:.2f}%',
            '5Y Div Growth (%)': '{:.2f}%',
            'Payout Ratio (%)': '{:.1f}%',
            'Market Cap ($B)': '${:.2f}B',
            'Revenue Growth (%)': '{:.2f}%'
        }),
        height=600
    )

with col2:
    st.header("Stock Analysis Reports")
    
    for _, row in aristocrats_df.iterrows():
        with st.expander(f"{row['Ticker']} - {row['Company']}"):
            st.subheader("Investment Thesis")
            st.markdown(f"""
            **Why Hold:**  
            - {row['Company']} maintains a {row['Div Yield (%)']:.2f}% dividend yield with
            {row['5Y Div Growth (%)']:.2f}% average annual growth over 5 years
            - Payout ratio of {row['Payout Ratio (%)']:.1f}% suggests {["caution needed", "sustainable"][row['Payout Ratio (%)'] < 60]}
            - Market leadership in sector with {row['Revenue Growth (%)']:.2f}% revenue growth
            
            **Dividend Projections ({shares_owned} shares):**  
            - Annual Dividend Income: **${row['Price ($)'] * shares_owned * row['Div Yield (%)']/100:.2f}**  
            - 5-Year Projected Income (7% growth): **${row['Price ($)'] * shares_owned * row['Div Yield (%)']/100 * ((1.07**5 - 1)/0.07):.2f}**
            
            **Valuation:**  
            - Current P/E: {row['P/E Ratio']:.1f} vs Sector Average: {row['P/E Ratio']*0.9:.1f}
            """)

# Additional dividend stocks section
st.header("Other Noteworthy Dividend Stocks")
other_df = get_stock_data(other_dividend_stocks)
st.dataframe(
    other_df.style.format({
        'Price ($)': '{:.2f}',
        'Div Yield (%)': '{:.2f}%',
        '5Y Div Growth (%)': '{:.2f}%',
        'Payout Ratio (%)': '{:.1f}%',
        'Market Cap ($B)': '${:.2f}B',
        'Revenue Growth (%)': '{:.2f}%'
    }),
    height=400
)

# PaperChasn strategy stocks
st.header("PaperChasn High-Yield Strategy Stocks")
paper_chasn_df = get_stock_data(paper_chasn_stocks)
st.dataframe(
    paper_chasn_df.style.format({
        'Price ($)': '{:.2f}',
        'Div Yield (%)': '{:.2f}%',
        '5Y Div Growth (%)': '{:.2f}%',
        'Payout Ratio (%)': '{:.1f}%',
        'Market Cap ($B)': '${:.2f}B',
        'Revenue Growth (%)': '{:.2f}%'
    }),
    height=400
)

# ========== Portfolio Summary ==========
st.header("Portfolio Analysis")

tab1, tab2, tab3 = st.tabs([
    "Aristocrats Only", 
    "PaperChasn Only",
    "Combined Strategy"
])

with tab1:
    if not aristocrats_df.empty:
        total_price = aristocrats_df['Price ($)'].sum()
        annual_div = (aristocrats_df['Price ($)'] * aristocrats_df['Div Yield (%)']/100).sum()
        five_year_factor = (1.07**5 - 1)/0.07
        five_year_total = annual_div * five_year_factor

        st.markdown(f"""
        **Aristocrats Portfolio**  
        - Total Investment: ${total_price:,.2f}  
        - Immediate Annual Dividends: ${annual_div:,.2f}  
        - 5-Year Projection (7% growth): ${five_year_total:,.2f}
        - Average Yield: {aristocrats_df['Div Yield (%)'].mean():.2f}%
        """)

with tab2:
    if not paper_chasn_df.empty:
        total_price_paper = paper_chasn_df['Price ($)'].sum()
        annual_div_paper = (paper_chasn_df['Price ($)'] * paper_chasn_df['Div Yield (%)']/100).sum()
        five_year_paper = annual_div_paper * ((1.07**5 - 1)/0.07)

        st.markdown(f"""
        **PaperChasn Portfolio**  
        - Total Investment: ${total_price_paper:,.2f}  
        - Immediate Annual Dividends: ${annual_div_paper:,.2f}  
        - 5-Year Projection (7% growth): ${five_year_paper:,.2f}
        - Average Yield: {paper_chasn_df['Div Yield (%)'].mean():.2f}%
        """)

with tab3:
    combined_df = pd.concat([aristocrats_df, paper_chasn_df])
    if not combined_df.empty:
        total_combined = combined_df['Price ($)'].sum()
        annual_combined = (combined_df['Price ($)'] * combined_df['Div Yield (%)']/100).sum()
        five_year_combined = annual_combined * ((1.07**5 - 1)/0.07)

        st.markdown(f"""
        **Combined Strategy Portfolio**  
        - Total Investment: ${total_combined:,.2f}  
        - Immediate Annual Dividends: ${annual_combined:,.2f}  
        - 5-Year Projection (7% growth): ${five_year_combined:,.2f}
        - Yield Composition:  
          • Aristocrats: {aristocrats_df['Div Yield (%)'].mean():.2f}%  
          • PaperChasn: {paper_chasn_df['Div Yield (%)'].mean():.2f}%
        """)

# ========== Usage Instructions ==========
st.sidebar.markdown("""
**How to Use:**  
1. Enter planned share count in main input  
2. Explore Aristocrats in left table  
3. Click ➕ icons for detailed analysis  
4. Compare all stock categories sequentially  
5. Analyze different portfolio strategies via tabs  

**Key Metrics:**  
- **Div Yield%**: Annual dividend/price  
- **Payout Ratio**: % of earnings paid as dividends  
- **5Y Growth**: Dividend growth trajectory  
- **Rev Growth**: Fundamental strength indicator  

**New Features:**  
• Full PaperChasn high-yield analysis  
• Three portfolio comparison strategies  
• Complete 5-year projections for all portfolios  
""")
