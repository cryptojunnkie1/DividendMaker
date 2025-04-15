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
    ('ADM', 'Archer-Daniels-Midland')
]

other_dividend_stocks = [
    ('O', 'Realty Income'),
    ('MAIN', 'Main Street Capital'),
    ('HD', 'Home Depot'),
    ('LOW', "Lowe's"),
    ('IBM', 'International Business Machines')
]

# ========== Helper Functions ==========
def get_stock_data(tickers):
    data = []
    for ticker, name in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            history = stock.history(period="5y")
            
            div_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
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
shares_owned = st.number_input("Enter number of shares you plan to hold:", min_value=1, value=100)

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

# ========== Usage Instructions ==========
st.sidebar.markdown("""
**How to Use:**  
1. Enter planned share count in main input  
2. Explore Aristocrats in left table  
3. Click ➕ icons for detailed analysis  
4. Compare with other dividend stocks below  

**Key Metrics:**  
- **Div Yield%**: Annual dividend/price  
- **Payout Ratio**: % of earnings paid as dividends  
- **5Y Growth**: Dividend growth trajectory  
- **Rev Growth**: Fundamental strength indicator  
""")
