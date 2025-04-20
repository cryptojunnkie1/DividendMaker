# INSTALLATION: Run these commands first
# pip install streamlit yfinance pandas numpy plotly streamlit-extras
# streamlit run app.py

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from streamlit_extras import responsive

# ========== DATA SETUP ==========
dividend_aristocrats = [
    ('JNJ', 'Johnson & Johnson'), ('PG', 'Procter & Gamble'), 
    ('KO', 'Coca-Cola'), ('PEP', 'PepsiCo'), ('ABBV', 'AbbVie'),
    ('TGT', 'Target'), ('ED', 'Consolidated Edison'), ('MMM', '3M Company'),
    ('CL', 'Colgate-Palmolive'), ('ADM', 'Archer-Daniels-Midland'),
    ('AOS', 'A. O. Smith'), ('ABT', 'Abbott Laboratories'),
    ('APD', 'Air Products and Chemicals'), ('ALB', 'Albemarle Corporation'),
    ('AMCR', 'Amcor'), ('T', 'AT&T'), ('ADP', 'Automatic Data Processing'),
    ('BDX', 'Becton Dickinson'), ('BRO', 'Brown & Brown'),
    ('CHRW', 'C.H. Robinson'), ('CAH', 'Cardinal Health'),
    ('CVX', 'Chevron'), ('CINF', 'Cincinnati Financial'),
    ('CLX', 'Clorox'), ('DOV', 'Dover Corporation'),
    ('EMR', 'Emerson Electric'), ('ESS', 'Essex Property Trust'),
    ('XOM', 'ExxonMobil'), ('FRT', 'Federal Realty Investment Trust'),
    ('BEN', 'Franklin Resources'), ('GD', 'General Dynamics'),
    ('GPC', 'Genuine Parts Company'), ('HRL', 'Hormel Foods'),
    ('ITW', 'Illinois Tool Works'), ('KMB', 'Kimberly-Clark'),
    ('LOW', "Lowe's"), ('MKC', 'McCormick & Company'),
    ('NEE', 'NextEra Energy'), ('NDSN', 'Nordson Corporation'),
    ('SHW', 'Sherwin-Williams'), ('SWK', 'Stanley Black & Decker'),
    ('SYY', 'Sysco'), ('TROW', 'T. Rowe Price'),
    ('TR', 'Tootsie Roll Industries'), ('VFC', 'V.F. Corporation')
]

other_dividend_stocks = [
    ('O', 'Realty Income'), ('MAIN', 'Main Street Capital'),
    ('HD', 'Home Depot'), ('LOW', "Lowe's"),
    ('IBM', 'International Business Machines'), ('AFL', 'Aflac'),
    ('ARE', 'Alexandria Real Estate Equities'), ('ALL', 'Allstate'),
    ('MO', 'Altria Group'), ('AEE', 'Ameren'),
    ('AEP', 'American Electric Power'), ('AWR', 'American States Water'),
    ('AMT', 'American Tower'), ('COLD', 'Americold Realty Trust'),
    ('APTV', 'Aptiv'), ('AVB', 'AvalonBay Communities'),
    ('BRK-B', 'Berkshire Hathaway'), ('BBY', 'Best Buy'),
    ('BLK', 'BlackRock'), ('BWA', 'BorgWarner'),
    ('BXP', 'Boston Properties'), ('BMY', 'Bristol-Myers Squibb'),
    ('AVGO', 'Broadcom'), ('CCJ', 'Cameco'),
    ('CAT', 'Caterpillar'), ('ATO', 'Atmos Energy'),
    ('CSCO', 'Cisco Systems'), ('D', 'Dominion Energy'),
    ('DUK', 'Duke Energy'), ('DTE', 'DTE Energy'),
    ('ETN', 'Eaton Corporation'), ('EVRG', 'Evergy'),
    ('ES', 'Eversource Energy'), ('EXC', 'Exelon'),
    ('FRT', 'Federal Realty Investment Trust'), ('FE', 'FirstEnergy'),
    ('GIS', 'General Mills'), ('GPC', 'Genuine Parts Company'),
    ('HRL', 'Hormel Foods'), ('HST', 'Host Hotels & Resorts'),
    ('ICE', 'Intercontinental Exchange'), ('IRM', 'Iron Mountain'),
    ('JNJ', 'Johnson & Johnson'), ('KIM', 'Kimco Realty'),
    ('KMI', 'Kinder Morgan'), ('KR', 'Kroger'),
    ('LMT', 'Lockheed Martin'), ('LNT', 'Alliant Energy'),
    ('LHX', 'L3Harris Technologies'), ('MAA', 'Mid-America Apartment Communities'),
    ('MMM', '3M Company'), ('NEE', 'NextEra Energy'),
    ('NI', 'NiSource'), ('NTRS', 'Northern Trust'),
    ('NUE', 'Nucor'), ('OKE', 'ONEOK'),
    ('PPL', 'PPL Corporation'), ('PEG', 'Public Service Enterprise Group'),
    ('PEP', 'PepsiCo'), ('PFG', 'Principal Financial Group'),
    ('PG', 'Procter & Gamble'), ('PNW', 'Pinnacle West Capital'),
    ('RTX', 'Raytheon Technologies'), ('SBUX', 'Starbucks'),
    ('SO', 'Southern Company'), ('SPG', 'Simon Property Group'),
    ('T', 'AT&T'), ('TGT', 'Target'),
    ('TRV', 'The Travelers Companies'), ('UDR', 'UDR'),
    ('USB', 'U.S. Bancorp'), ('VLO', 'Valero Energy'),
    ('VTR', 'Ventas'), ('VZ', 'Verizon Communications'),
    ('WEC', 'WEC Energy Group'), ('WFC', 'Wells Fargo'),
    ('WMB', 'Williams Companies'), ('XEL', 'Xcel Energy')
]

paper_chasn_stocks = [
    ('ABBV', 'AbbVie'), ('CVX', 'Chevron'),
    ('TROW', 'T. Rowe Price'), ('C', 'Citigroup'),
    ('BBY', 'Best Buy'), ('O', 'Realty Income'),
    ('CMA', 'Comerica'), ('HSBC', 'HSBC Holdings'),
    ('BMY', 'Bristol-Myers Squibb'), ('EPR', 'EPR Properties'),
    ('PFE', 'Pfizer'), ('BCE', 'BCE Inc.'),
    ('STWD', 'Starwood Property Trust'), ('NLY', 'Annaly Capital'),
    ('APA', 'APA Corporation'), ('ARR', 'ARMOUR Residential REIT'),
    ('HST', 'Host Hotels & Resorts'), ('IVZ', 'Invesco'),
    ('IEP', 'Icahn Enterprises'), ('AGNC', 'AGNC Investment'),
    ('BTG', 'B2Gold')
]

# ========== HELPER FUNCTIONS ==========
@st.cache_data(ttl=3600)
def get_stock_data(tickers):
    data = []
    for ticker, name in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            history = stock.history(period="5y")
            
            div_yield = info.get('dividendYield', 0) or 0
            pe_ratio = info.get('trailingPE')
            payout_ratio = info.get('payoutRatio')
            market_cap = info.get('marketCap')
            div_growth = history['Dividends'].pct_change(periods=252*5).mean()*100
            
            data.append({
                'Ticker': ticker,
                'Company': name,
                'Price ($)': info.get('currentPrice'),
                'Div Yield (%)': div_yield,
                '5Y Div Growth (%)': div_growth,
                'Payout Ratio (%)': (payout_ratio * 100) if payout_ratio else None,
                'P/E Ratio': pe_ratio,
                'Market Cap ($B)': round(market_cap/1e9, 2) if market_cap else None,
                'Revenue Growth (%)': (info.get('revenueGrowth', 0) or 0)*100
            })
        except Exception as e:
            st.error(f"Error fetching {ticker}: {str(e)}")
    return pd.DataFrame(data)

def create_dividend_chart(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.dividends.reset_index()
        fig = px.area(hist, x='Date', y='Dividends', 
                     title=f"{ticker} Dividend History",
                     labels={'Dividends': 'Amount ($)'})
        fig.update_layout(hovermode="x", template='plotly_white')
        return fig
    except:
        return px.scatter(title="Data Unavailable")

# ========== APP INTERFACE ==========
st.set_page_config(page_title="Dividend Pro", layout="wide", page_icon="💸")
responsive.config(default_layout="desktop")

# Sidebar Controls
with st.sidebar:
    st.title("Controls")
    shares = st.number_input("Shares to Hold", 1, 10000, 100)
    alerts = st.multiselect("Alerts", ["Yield >5%", "Payout <75%", "52W Low"])
    st.divider()
    
    # Education Section
    with st.expander("Learn Dividends 101"):
        st.markdown("""
        **Dividend Basics**  
        - Yield = Annual Dividend / Stock Price  
        - Payout Ratio = Dividends / Earnings  
        - DRIP = Dividend Reinvestment Plan  
        \[ Yield = \frac{D}{P} \times 100\% \]
        """)

# Main Tabs
tab1, tab2, tab3 = st.tabs(["Analysis", "Portfolio", "Community"])

with tab1:
    # Stock Selection
    category = st.radio("Stock Group", ["Aristocrats", "High Yield", "PaperChasn"])
    tickers = {
        "Aristocrats": dividend_aristocrats,
        "High Yield": other_dividend_stocks,
        "PaperChasn": paper_chasn_stocks
    }.get(category, dividend_aristocrats)
    
    # Data Display
    df = get_stock_data(tickers)
    if not df.empty:
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.dataframe(
                df.style.format({
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
            selected = st.selectbox("Analyze Stock", df['Ticker'])
            st.plotly_chart(create_dividend_chart(selected), use_container_width=True)
            
            stock = df[df['Ticker'] == selected].iloc[0]
            st.metric("Current Yield", f"{stock['Div Yield (%)']:.2f}%")
            st.progress(min(stock['Payout Ratio (%)']/100, 1), 
                       text=f"Payout Ratio: {stock['Payout Ratio (%)']:.1f}%")

with tab2:
    st.header("Portfolio Builder")
    cols = st.columns(3)
    
    # Holdings Input
    holdings = {}
    for idx, (ticker, name) in enumerate(dividend_aristocrats + other_dividend_stocks):
        with cols[idx%3]:
            holdings[ticker] = st.slider(
                f"{ticker} Shares", 0, 1000, 0,
                help=f"Allocate {name}"
            )
    
    # Portfolio Math
    total_value = 0
    income = 0
    for ticker, shares in holdings.items():
        price = get_stock_data([(ticker, '')])['Price ($)'].values[0]
        total_value += price * shares
        yield_pct = get_stock_data([(ticker, '')])['Div Yield (%)'].values[0]
        income += (price * shares) * (yield_pct / 100)
    
    # Display Metrics  
    st.success(f"**Portfolio Value**: ${total_value:,.2f}")
    st.info(f"**Annual Income**: ${income:,.2f}")
    
    # Projection
    if st.button("Project 5 Years"):
        growth = np.random.normal(0.07, 0.15, 1000)
        projected = total_value * (1 + growth)**5
        fig = px.histogram(projected, nbins=50, 
                         title="Wealth Distribution Forecast")
        st.plotly_chart(fig)

with tab3:
    st.header("Community Strategies")
    strategy = st.text_area("Share Your Approach (Max 280 chars)", height=150)
    if st.button("Publish"):
        st.session_state.strategies = st.session_state.get('strategies', []) + [strategy]
    
    st.subheader("Top Strategies")
    for strat in st.session_state.get('strategies', [
        "Reinvest dividends in highest conviction picks",
        "Balance high yield with growth stocks",
        "Use sector rotation for stability"
    ]):
        st.markdown(f"- {strat}")

# ========== FOOTER & NOTES ==========
st.markdown("---")
st.caption("""
Data Source: Yahoo Finance | 
Updated: 2025-04-20 | 
For Educational Purposes Only
""")
