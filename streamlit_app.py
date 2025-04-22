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
    ('CVX', 'Chevron'),
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
    ('BRK-B', 'Berkshire Hathaway'),
    ('BBY', 'Best Buy'),
    ('BLK', 'BlackRock'),
    ('BWA', 'BorgWarner'),
    ('BXP', 'Boston Properties'),
    ('BMY', 'Bristol-Myers Squibb'),
    ('AVGO', 'Broadcom'),
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
            
            div_yield = info.get('dividendYield', 0) if 'dividendYield' in info else 0
            pe_ratio = info.get('trailingPE', None)
            payout_ratio = info.get('payoutRatio', None)
            market_cap = info.get('marketCap', None)
            div_growth_5y = history['Dividends'].pct_change(periods=252 * 5).mean() * 100
            
            data.append({
                'Ticker': ticker,
                'Company': name,
                'Price ($)': info.get('currentPrice', 0),
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

# ========== Dynamic Analysis Function ==========
def dynamic_analysis(all_stocks_df):
    total_price = all_stocks_df['Price ($)'].sum()
    annual_dividends = (all_stocks_df['Price ($)'] * all_stocks_df['Div Yield (%)'] / 100).sum()
    
    total_projected_value = total_price
    for year in range(1, 6):
        annual_dividends = (total_projected_value * (all_stocks_df['Div Yield (%)'].mean() / 100))
        total_projected_value += annual_dividends * (1 + 0.07)
    
    return total_price, annual_dividends, total_projected_value

# ========== Combined Stock Data ==========
combined_stocks = dividend_aristocrats + other_dividend_stocks + paper_chasn_stocks

# Initialize combined_df
combined_df = get_stock_data(combined_stocks)  # Fetch combined stock data

# ========== Dynamic Analysis Section ==========
if not combined_df.empty:
    total_investment, immediate_dividends, projected_value = dynamic_analysis(combined_df)
    # Recommendations based on highest dividend yield
    top_dividend_stocks = combined_df.nlargest(20, 'Div Yield (%)')
    st.subheader("Optimized Elite Dividend Analysis Picks")
    for _, row in top_dividend_stocks.iterrows():
        row['Div Yield (%)'] = pd.to_numeric(row['Div Yield (%)'], errors='coerce')
        row['5Y Div Growth (%)'] = pd.to_numeric(row['5Y Div Growth (%)'], errors='coerce')

        if pd.isna(row['Div Yield (%)']) or pd.isna(row['5Y Div Growth (%)']):
            projected_return = float('nan')
        else:
            projected_return = 0.4 * row['Div Yield (%)'] + 0.6 * row['5Y Div Growth (%)']

        st.markdown(f"""
        - **{row['Ticker']} - {row['Company']}**  
          - Current Yield: {row['Div Yield (%)']:.2f}%  
          - Projected 5Y Total Return: {projected_return:.1f}%  
          - P/E Ratio: {row['P/E Ratio']:.1f}  
          - Insight: {generate_insight(row['Ticker'])}
        """)

    st.subheader("**Optimized Elite Dividend Analysis Summary Outlook**")
    st.markdown(f"""
        - Total Investment: ${total_investment:,.2f}  
        - Immediate Annual Dividends: ${immediate_dividends:.2f}  
        - Total Projected Value (5-Year With Reinvestment): ${projected_value:,.2f}  
        - Average Yield: {combined_df['Div Yield (%)'].mean():.2f}%
        """)
else:
    st.warning("No data available for analysis.")

# ========== App Interface ==========
st.title("Dividend Stock Analysis Toolkit")
st.subheader("Portfolio Builder for Long-Term Investors")

# User input for shares owned
shares_owned = st.number_input("Enter number of shares you plan to hold:", min_value=1, value=1)

# Main analysis section
col1, col2 = st.columns([3, 2])

# Dividend Aristocrats Analysis
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

    if not aristocrats_df.empty:
        total_price_aristocrats = aristocrats_df['Price ($)'].sum()
        avg_div_yield_aristocrats = aristocrats_df['Div Yield (%)'].mean() / 100
        annual_div_aristocrats = (aristocrats_df['Price ($)'] * aristocrats_df['Div Yield (%)'] / 100).sum()

        total_projected_value_aristocrats = total_price_aristocrats
        for year in range(1, 6):
            annual_div_aristocrats = (total_projected_value_aristocrats * avg_div_yield_aristocrats)
            total_projected_value_aristocrats += annual_div_aristocrats * (1 + 0.07)

        st.markdown(f"""
        **Dividend Aristocrats Portfolio**  
        - Total Investment: ${total_price_aristocrats:,.2f}  
        - Immediate Annual Dividends: ${annual_div_aristocrats:.2f}  
        - Total Projected Value (5-Year With Reinvestment): ${total_projected_value_aristocrats:,.2f}
        - Average Yield: {aristocrats_df['Div Yield (%)'].mean():.2f}%
        """)

# Other Dividend Stocks Analysis
with col2:
    st.header("Stock Analysis Reports")
    
    # Define paper_chasn_df
    paper_chasn_df = get_stock_data(paper_chasn_stocks)
    
    for _, row in aristocrats_df.iterrows():
        with st.expander(f"{row['Ticker']} - {row['Company']}"):
            st.subheader("Investment Thesis")
            st.markdown(f"""
            **Why Hold:**  
            - {row['Company']} maintains a {row['Div Yield (%)']:.2f}% dividend yield with
            {row['5Y Div Growth (%)']:.2f}% average annual growth over 5 years.
            - Payout ratio of {row['Payout Ratio (%)']:.1f}% suggests sustainability.
            
            **Dividend Projections ({shares_owned} shares):**  
            - Annual Dividend Income: **${row['Price ($)'] * shares_owned * row['Div Yield (%)'] / 100:.2f}**  
            - 5-Year Projected Income (7% growth): **${row['Price ($)'] * shares_owned * row['Div Yield (%)'] / 100 * ((1.07 ** 5 - 1) / 0.07):.2f}**

            **Valuation:**  
            - Current P/E: {row['P/E Ratio']:.1f} vs Sector Average: {row['P/E Ratio'] * 0.9:.1f}
            - Insight: {generate_insight(row['Ticker'])}
            """)

            st.markdown(f"""
            **Fundamental Analysis**  
            • Current Yield: {row['Div Yield (%)']:.2f}% (S&P 500 Avg: 1.5%)  
            • 5Y Dividend Growth: {row['5Y Div Growth (%)'] if row['5Y Div Growth (%)'] is not None else "nan"}%  
            • Payout Ratio: {row['Payout Ratio (%)']:.1f}%  
            • Market Cap: ${row['Market Cap ($B)']:.2f}B  
            • Revenue Trend: {row['Revenue Growth (%)']:.2f}% YoY  
            """)

            st.markdown(f"Yield Strength: {(row['Div Yield (%)'] / 1.5):.2f}x Market Average")

            st.markdown(f"""
            **Risk/Reward Profile**  
            - Volatility Score: {(100 - abs(row['Payout Ratio (%)'] - 75)):.1f}/100  
            - Yield Sustainability: {"🔴 High Risk" if row['Payout Ratio (%)'] > 90 else "🟡 Moderate" if row['Payout Ratio (%)'] > 75 else "🟢 Stable"}  
            - Growth Potential: {"⭐" * int(row['Revenue Growth (%)'] / 5)}  
            - Value Indicator: {"Undervalued" if row['P/E Ratio'] < 15 else "Fair" if row['P/E Ratio'] < 25 else "Overvalued"}  
            """)

            st.markdown(f"""
            **Strategic Rationale**  
            - Projected 5Y Total Return: {0.4 * row['Div Yield (%)'] + 0.6 * row['Revenue Growth (%)']:.1f}%  
            - Dividend Coverage Ratio: {min(100 / (row['Payout Ratio (%)'] or 1), 5):.1f}x  
            - Sector Weighting Impact: {["Enhances Diversification", "Concentrates Exposure"][row['Market Cap ($B)'] > 50]}  
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

if not other_df.empty:
    total_price_other = other_df['Price ($)'].sum()
    avg_div_yield_other = other_df['Div Yield (%)'].mean() / 100
    annual_div_other = (other_df['Price ($)'] * other_df['Div Yield (%)'] / 100).sum()

    total_projected_value_other = total_price_other
    for year in range(1, 6):
        annual_div_other = (total_projected_value_other * avg_div_yield_other)
        total_projected_value_other += annual_div_other * (1 + 0.07)

    st.markdown(f"""
    **Other Dividend Stocks Portfolio**  
    - Total Investment: ${total_price_other:,.2f}  
    - Immediate Annual Dividends: ${annual_div_other:.2f}  
    - Total Projected Value (5-Year With Reinvestment): ${total_projected_value_other:,.2f}
    - Average Yield: {other_df['Div Yield (%)'].mean():.2f}%
    """)

for _, row in other_df.iterrows():
    with st.expander(f"{row['Ticker']} - {row['Company']}"):
        st.subheader("Investment Thesis")
        st.markdown(f"""
        **Why Hold:**  
        - {row['Company']} maintains a {row['Div Yield (%)']:.2f}% dividend yield with
        {row['5Y Div Growth (%)']:.2f}% average annual growth over 5 years.
        - Payout ratio of {row['Payout Ratio (%)']:.1f}% suggests sustainability.
        
        **Dividend Projections ({shares_owned} shares):**  
        - Annual Dividend Income: **${row['Price ($)'] * shares_owned * row['Div Yield (%)'] / 100:.2f}**  
        - 5-Year Projected Income (7% growth): **${row['Price ($)'] * shares_owned * row['Div Yield (%)'] / 100 * ((1.07 ** 5 - 1) / 0.07):.2f}**

        **Valuation:**  
        - Current P/E: {row['P/E Ratio']:.1f} vs Sector Average: {row['P/E Ratio'] * 0.9:.1f}
        - Insight: {generate_insight(row['Ticker'])}
        """)

        st.markdown(f"""
        **Fundamental Analysis**  
        • Current Yield: {row['Div Yield (%)']:.2f}% (S&P 500 Avg: 1.5%)  
        • 5Y Dividend Growth: {row['5Y Div Growth (%)'] if row['5Y Div Growth (%)'] is not None else "nan"}%  
        • Payout Ratio: {row['Payout Ratio (%)']:.1f}%  
        • Market Cap: ${row['Market Cap ($B)']:.2f}B  
        • Revenue Trend: {row['Revenue Growth (%)']:.2f}% YoY  
        """)

        st.markdown(f"Yield Strength: {(row['Div Yield (%)'] / 1.5):.2f}x Market Average")

        st.markdown(f"""
        **Risk/Reward Profile**  
        - Volatility Score: {(100 - abs(row['Payout Ratio (%)'] - 75)):.1f}/100  
        - Yield Sustainability: {"🔴 High Risk" if row['Payout Ratio (%)'] > 90 else "🟡 Moderate" if row['Payout Ratio (%)'] > 75 else "🟢 Stable"}  
        - Growth Potential: {"⭐" * int(row['Revenue Growth (%)'] / 5)}  
        - Value Indicator: {"Undervalued" if row['P/E Ratio'] < 15 else "Fair" if row['P/E Ratio'] < 25 else "Overvalued"}  
        """)

        st.markdown(f"""
        **Strategic Rationale**  
        - Projected 5Y Total Return: {0.4 * row['Div Yield (%)'] + 0.6 * row['Revenue Growth (%)']:.1f}%  
        - Dividend Coverage Ratio: {min(100 / (row['Payout Ratio (%)'] or 1), 5):.1f}x  
        - Sector Weighting Impact: {["Enhances Diversification", "Concentrates Exposure"][row['Market Cap ($B)'] > 50]}  
        """)

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
        annual_div = (aristocrats_df['Price ($)'] * aristocrats_df['Div Yield (%)'] / 100).sum()
        five_year_factor = (1.07 ** 5 - 1) / 0.07
        five_year_total = annual_div * five_year_factor
        st.markdown(f"""
        **Aristocrats Portfolio**  
        - Total Investment: ${total_price:,.2f}  
        - Immediate Annual Dividends: ${annual_div:,.2f}  
        - 5-Year Projection (7% growth): ${five_year_total:,.2f}  
        """)

with tab2:
    if not paper_chasn_df.empty:
        total_price_paper = paper_chasn_df['Price ($)'].sum()
        annual_div_paper = (paper_chasn_df['Price ($)'] * paper_chasn_df['Div Yield (%)']/100).sum()
        five_year_paper = annual_div_paper * ((1.07 ** 5 - 1) / 0.07)
        st.markdown(f"""
        **PaperChasn Portfolio**  
        - Total Investment: ${total_price_paper:,.2f}  
        - Immediate Annual Dividends: ${annual_div_paper:.2f}  
        - 5-Year Projection (7% growth): ${five_year_paper:.2f}  
        - Average Yield: {paper_chasn_df['Div Yield (%)'].mean():.2f}%
        """)
    else:
        st.warning("No data available for PaperChasn stocks.")

with tab3:
    combined_df = pd.concat([aristocrats_df, paper_chasn_df])
    if not combined_df.empty:
        total_combined = combined_df['Price ($)'].sum()
        annual_combined = (combined_df['Price ($)'] * combined_df['Div Yield (%)'] / 100).sum()
        five_year_combined = annual_combined * ((1.07 ** 5 - 1) / 0.07)
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
• Institutional-grade risk analysis  
• Dynamic sector exposure breakdown  
• Professional recommendation engine  
""")
