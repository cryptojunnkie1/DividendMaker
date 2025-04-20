# COMPLETE DIVIDEND ANALYZER APP
# INSTALL: pip install streamlit yfinance pandas numpy plotly
# RUN: streamlit run app.py

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ========== DATA SETUP ==========
DIVIDEND_ARISTOCRATS = [
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

HIGH_YIELD_STOCKS = [
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

PAPERCHASN_STOCKS = [
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


# ====== CORE FUNCTIONS ======
@st.cache_data(ttl=3600)
def get_stock_data(ticker_list):
    """Fetch complete stock data with error handling"""
    data = []
    for ticker, name in ticker_list:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1y")
            
            entry = {
                'Ticker': ticker,
                'Name': name,
                'Price ($)': info.get('currentPrice', np.nan),
                'Div Yield (%)': info.get('dividendYield', 0) * 100,
                '5Y Div Growth (%)': info.get('fiveYearAvgDividendGrowthRate', 0) * 100,
                'Payout Ratio (%)': info.get('payoutRatio', 0) * 100,
                'Market Cap ($B)': info.get('marketCap', 0) / 1e9,
                'Revenue Growth (%)': info.get('revenueGrowth', 0) * 100,
                'Last Updated': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            data.append(entry)
        except Exception as e:
            st.error(f"Error fetching {ticker}: {str(e)}")
    return pd.DataFrame(data)

def create_dividend_chart(ticker):
    """Generate interactive dividend history chart"""
    try:
        div_history = yf.Ticker(ticker).dividends.reset_index()
        fig = px.line(div_history, x='Date', y='Dividends', 
                     title=f"{ticker} Dividend History",
                     labels={'Dividends': 'Dividend per Share ($)'})
        fig.update_traces(line=dict(width=4))
        return fig
    except Exception as e:
        st.error(f"Chart error: {str(e)}")
        return px.scatter(title="Data Not Available")

# ====== RESPONSIVE LAYOUT SYSTEM ======
def is_mobile():
    """Detect mobile devices using simple screen width simulation"""
    return st.session_state.get('screen_width', 1200) < 768

def responsive_columns():
    """Dynamic column configuration"""
    return 1 if is_mobile() else [2, 1]

def adaptive_dataframe(df):
    """Optimize dataframe display for different devices"""
    fmt_dict = {
        'Price ($)': '{:.2f}',
        'Div Yield (%)': '{:.2f}%',
        '5Y Div Growth (%)': '{:.2f}%',
        'Payout Ratio (%)': '{:.1f}%',
        'Market Cap ($B)': '${:.2f}B',
        'Revenue Growth (%)': '{:.2f}%'
    }
    
    styled_df = df.style.format(fmt_dict)
    
    if is_mobile():
        return st.dataframe(
            styled_df.set_properties(**{'font-size': '10px'}),
            height=400,
            use_container_width=True
        )
    else:
        return st.dataframe(
            styled_df.background_gradient(),
            height=600,
            use_container_width=True
        )

# ====== MAIN APP ======
def main():
    # Initial configuration
    st.set_page_config(
        page_title="Dividend Pro", 
        layout="wide", 
        page_icon="💸",
        menu_items={
            'Get Help': 'https://dividendanalyzer.com/help',
            'Report a bug': 'mailto:support@dividendanalyzer.com',
            'About': "### Dividend Analysis Tool v2.0"
        }
    )
    
    # Session state initialization
    if 'screen_width' not in st.session_state:
        st.session_state.screen_width = 1200  # Default desktop
    
    # Device-aware title
    st.title("📱 Mobile Dividend Viewer" if is_mobile() else "💻 Professional Dividend Analyzer")
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Controls")
        shares = st.number_input("Number of Shares", 1, 10000, 100, 
                               help="Enter your total shares owned")
        investment = st.number_input("Investment Amount ($)", 100, 1000000, 10000)
        
        st.divider()
        alert_options = ["Yield >5%", "Payout <75%", "52W Low", "High Debt", "Negative Growth"]
        alerts = st.multiselect("Set Alerts", alert_options)
        
        st.divider()
        if is_mobile():
            with st.expander("📚 Dividend Guide"):
                st.markdown("""
                **Key Formulas**  
                \[ Dividend\ Yield = \frac{Annual\ Dividend}{Stock\ Price} \times 100\% \]  
                \[ Payout\ Ratio = \frac{Dividends\ Paid}{Net\ Income} \times 100\% \]
                """)
        else:
            st.markdown("""
            **Essential Formulas**  
            \[ Yield = \frac{D}{P} \times 100\% \]  
            \[ Payout\ Ratio = \frac{Div}{EPS} \times 100\% \]
            """)

    # Main interface tabs
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "💰 Portfolio", "💬 Community"])

    with tab1:
        # Stock category selection
        category = st.radio("Select Stock Category", 
                           ("Aristocrats", "High Yield", "PaperChasn"),
                           horizontal=is_mobile(),
                           help="Choose between stable dividend payers and growth stocks")
        
        # Load appropriate stock list
        stock_map = {
            "Aristocrats": DIVIDEND_ARISTOCRATS,
            "High Yield": HIGH_YIELD_STOCKS,
            "PaperChasn": PAPERCHASN_STOCKS
        }
        df = get_stock_data(stock_map[category])
        
        # Responsive columns layout
        cols = st.columns(responsive_columns())
        
        # Left column - Data display
        with cols[0]:
            st.subheader(f"{category} Stocks")
            adaptive_dataframe(df)
        
        # Right column - Detailed analysis (desktop only)
        if len(cols) > 1:
            with cols[1]:
                st.subheader("Deep Analysis")
                selected_ticker = st.selectbox("Choose Stock", df['Ticker'])
                
                # Dividend chart
                st.plotly_chart(
                    create_dividend_chart(selected_ticker),
                    use_container_width=True
                )
                
                # Key metrics
                metric_cols = st.columns(2)
                with metric_cols[0]:
                    st.metric("Current Yield", 
                             f"{df[df['Ticker'] == selected_ticker]['Div Yield (%)'].values[0]:.2f}%")
                    st.metric("Payout Ratio", 
                             f"{df[df['Ticker'] == selected_ticker]['Payout Ratio (%)'].values[0]:.1f}%")
                with metric_cols[1]:
                    st.metric("5Y Growth", 
                             f"{df[df['Ticker'] == selected_ticker]['5Y Div Growth (%)'].values[0]:.2f}%")
                    st.metric("Market Cap", 
                             f"${df[df['Ticker'] == selected_ticker]['Market Cap ($B)'].values[0]:.2f}B")

    with tab2:
        st.header("Portfolio Simulation")
        cols = st.columns(1 if is_mobile() else 3)
        
        # Portfolio inputs
        with cols[0]:
            st.subheader("Holdings")
            selected_stocks = st.multiselect("Select Stocks", [t[0] for t in DIVIDEND_ARISTOCRATS])
            
        if len(cols) > 1:
            with cols[1]:
                st.subheader("Dividend Impact")
                if selected_stocks:
                    div_total = sum(df[df['Ticker'].isin(selected_stocks)]['Div Yield (%)']/100 * investment)
                    st.metric("Annual Income", f"${div_total:.2f}")
                else:
                    st.warning("Select stocks to see projections")
        
        if len(cols) > 2:
            with cols[2]:
                st.subheader("Growth Projection")
                years = st.slider("Years", 1, 30, 10)
                if selected_stocks:
                    growth = sum(df[df['Ticker'].isin(selected_stocks)]['5Y Div Growth (%)']/100)
                    future_value = investment * (1 + growth)**years
                    st.metric("Projected Value", f"${future_value:,.2f}")

    with tab3:
        st.header("Community Strategies")
        strategy = st.text_area("Share Your Strategy", 
                               height=100 if is_mobile() else 150,
                               placeholder="Describe your dividend investment approach...")
        if st.button("Submit"):
            st.success("Strategy submitted! Community votes coming soon.")

if __name__ == "__main__":
    main()
