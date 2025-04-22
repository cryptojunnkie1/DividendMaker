import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

# Configure the Streamlit page
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

# Reiva'j Retirement Fund
reiva_j_retirement_fund = [
    ('BPRIX', 'BlackRock Inflation Protected Bond Instl'),
    ('FIHBX', 'Federated Inst High Yield Bond Inst'),
    ('FBNRX', 'Templeton Global Bond R6'),
    ('FGBMX', 'Fidelity Advisor New Markets Income Z'),
    ('RIDGX', 'American Funds Inc Fund of Amer R6'),
    ('CSRSX', 'Cohen & Steers Realty Shares'),
    ('MEIJX', 'MFS Value R4'),
    ('SAPYX', 'ClearBridge Appreciation I'),
    ('VIIIX', 'Vanguard Institutional Index Instl PL'),
    ('RGAGX', 'American Funds Growth Fund of Amer R6'),
    ('NRSRX', 'Neuberger Berman Sustainable Equity R6'),
    ('TILIX', 'TIAA-CREF Large-Cap Growth Index Fund—Institutional'),
    ('TILGX', 'TIAA-CREF Large-Cap Growth Fund—Institutional'),
    ('TILVX', 'TIAA-CREF Large-Cap Value Index Fund—Institutional'),
    ('TIEIX', 'TIAA-CREF Equity Index Fund—Institutional'),
    ('TISPX', 'TIAA-CREF S&P 500 Index Fund—Institutional'),
    ('VASVX', 'Vanguard Selected Value'),
    ('TIMVX', 'TIAA-CREF Mid-Cap Value Fund—Institutional'),
    ('VMCIX', 'Vanguard Mid-Cap Index Ins'),
    ('JAENX', 'Janus Henderson Enterprise T'),
    ('VMGMX', 'Vanguard Mid-Cap Growth Index Admiral'),
    ('GSSIX', 'Goldman Sachs Small Cap Value Inst'),
    ('VSCIX', 'Vanguard Small Cap Index Instl'),
    ('TISBX', 'TIAA-CREF Small-Cap Blend Index Fund—Institutional'),
    ('TISEX', 'TIAA-CREF Small-Cap Equity Fund—Institutional'),
    ('OTIIX', 'T. Rowe Price Small Cap Stock I'),
    ('AAERX', 'American Beacon International Equity R6'),
    ('VTSNX', 'Vanguard Total International Stock Index Ins'),
    ('MIDJX', 'MFS International New Discovery R4'),
    ('VREMX', 'Virtus Vontobel Emerging Markets Opportunities R6'),
    ('TCIEX', 'TIAA-CREF International Equity Index Fund—Institutional'),
    ('TEQLX', 'TIAA-CREF Emerging Markets Equity Index Fund—Institutional'),
    ('TIGRX', 'TIAA-CREF Growth & Income Fund—Institutional'),
    ('TISCX', 'TIAA-CREF Social Choice Equity Fund—Institutional'),
    ('TIREX', 'TIAA-CREF Real Estate Securities Fund—Institutional'),
    ('TIILX', 'TIAA-CREF Inflation-Linked Bond Fund—Institutional'),
    ('TBIIX', 'TIAA-CREF Bond Index Fund—Institutional'),
    ('TIBDX', 'TIAA-CREF Bond Fund—Institutional'),
    ('TIBFX', 'TIAA-CREF Bond Plus Fund—Institutional'),
    ('TIHYX', 'TIAA-CREF High-Yield Fund—Institutional'),
    ('CREF', 'CREF Stock Account R2')
]

# ========== Helper Functions ==========
def get_stock_data(tickers):
    data = []
    for ticker, name in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            history = stock.history(period="5y")

            div_yield = info.get('dividendYield', None)  # Get the dividend yield directly
            payout_ratio = info.get('payoutRatio', None)
            pe_ratio = info.get('trailingPE', None)
            market_cap = info.get('marketCap', None)

            # Calculate Dividend Growth
            if not history.empty:
                div_growth_5y = history['Dividends'].pct_change(periods=252 * 5).mean() * 100
            else:
                div_growth_5y = None  # No data available for dividend growth

            # Append stock data, handling None types gracefully
            data.append({
                'Ticker': ticker,
                'Company': name,
                'Price ($)': info.get('currentPrice'),
                'Div Yield (%)': div_yield,
                '5Y Div Growth (%)': div_growth_5y,
                'Payout Ratio (%)': (payout_ratio * 100) if payout_ratio is not None else None,
                'P/E Ratio': pe_ratio,
                'Market Cap ($B)': round(market_cap / 1e9, 2) if market_cap else None,
                'Revenue Growth (%)': info.get('revenueGrowth') * 100 if isinstance(info.get('revenueGrowth'), (int, float)) else None
            })
            
            time.sleep(1)  # Wait for 1 second between requests
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
    return pd.DataFrame(data)

# ========== App Interface ==========
st.title("Dividend Stock Analysis Toolkit")
st.subheader("Portfolio Builder for Long-Term Investors")

# User input for shares owned
shares_owned = st.number_input("Enter number of shares you plan to hold:", min_value=1, value=1)

# Main analysis section with two columns
col1, col2 = st.columns([3, 2])

# Dividend Aristocrats Analysis
with col1:
    st.header("Dividend Aristocrats Analysis")
    aristocrats_df = get_stock_data(dividend_aristocrats)

    # Display the data frame using styled format
    st.dataframe(
        aristocrats_df.style.format({
            'Price ($)': '${:,.2f}' if isinstance(aristocrats_df['Price ($)'].iloc[0], (int, float)) else 'N/A',
            'Div Yield (%)': '{:.2f}%' if isinstance(aristocrats_df['Div Yield (%)'].iloc[0], (int, float)) else 'N/A',
            '5Y Div Growth (%)': '{:.2f}' if isinstance(aristocrats_df['5Y Div Growth (%)'].iloc[0], (int, float)) else 'N/A',
            'Payout Ratio (%)': '{:.2f}%' if isinstance(aristocrats_df['Payout Ratio (%)'].iloc[0], (int, float)) else 'N/A',
            'Market Cap ($B)': '${:,.2f}' if isinstance(aristocrats_df['Market Cap ($B)'].iloc[0], (int, float)) else 'N/A'
        }),
        height=600
    )

    # Calculate projections for Dividend Aristocrats
    if not aristocrats_df.empty:
        total_price_aristocrats = aristocrats_df['Price ($)'].sum()
        avg_div_yield_aristocrats = aristocrats_df['Div Yield (%)'].mean() / 100  # Convert to decimal
        annual_div_aristocrats = (aristocrats_df['Price ($)'] * aristocrats_df['Div Yield (%)'] / 100).sum()

        # Total projected value with reinvestment
        total_projected_value_aristocrats = total_price_aristocrats  # Start with initial investment
        for year in range(1, 6):
            annual_div_aristocrats = (total_projected_value_aristocrats * avg_div_yield_aristocrats)  # Dividends for the year
            total_projected_value_aristocrats += annual_div_aristocrats * (1 + 0.07)  # Reinvest with projected growth

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
            """)

            # Fundamental Analysis 
            st.markdown(f"""
            **Fundamental Analysis**  
            • Current Yield: {row['Div Yield (%)']:.2f}% (S&P 500 Avg: 1.5%)  
            • 5Y Dividend Growth: {row['5Y Div Growth (%)'] if row['5Y Div Growth (%)'] is not None else "nan"}%  
            • Payout Ratio: {row['Payout Ratio (%)']:.1f}%  
            • Market Cap: ${row['Market Cap ($B)']:.2f}B  
            • Revenue Trend: {row['Revenue Growth (%)']:.2f}% YoY  
            """)

            # Yield Strength
            st.markdown(f"Yield Strength: {(row['Div Yield (%)'] / 1.5):.2f}x Market Average")

            # Risk/Reward Profile
            st.markdown(f"""
            **Risk/Reward Profile**  
            - Volatility Score: {(100 - abs(row['Payout Ratio (%)'] - 75)):.1f}/100  
            - Yield Sustainability: {"🔴 High Risk" if row['Payout Ratio (%)'] > 90 else "🟡 Moderate" if row['Payout Ratio (%)'] > 75 else "🟢 Stable"}  
            - Growth Potential: {"⭐" * int(row['Revenue Growth (%)'] / 5)}  
            - Value Indicator: {"Undervalued" if row['P/E Ratio'] < 15 else "Fair" if row['P/E Ratio'] < 25 else "Overvalued"}  
            """)

            # Strategic Rationale
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

# ========== Other Dividend Stocks Projection Section ==========
if not other_df.empty:
    total_price_other = other_df['Price ($)'].sum()
    avg_div_yield_other = other_df['Div Yield (%)'].mean() / 100  # Convert to decimal
    annual_div_other = (other_df['Price ($)'] * other_df['Div Yield (%)'] / 100).sum()

    # Total projected value with reinvestment
    total_projected_value_other = total_price_other  # Start with initial investment
    for year in range(1, 6):
        annual_div_other = (total_projected_value_other * avg_div_yield_other) 
        total_projected_value_other += annual_div_other * (1 + 0.07)  # Reinvest with projected growth

    st.markdown(f"""
    **Other Dividend Stocks Portfolio**  
    - Total Investment: ${total_price_other:,.2f}  
    - Immediate Annual Dividends: ${annual_div_other:.2f}  
    - Total Projected Value (5-Year With Reinvestment): ${total_projected_value_other:,.2f}
    - Average Yield: {other_df['Div Yield (%)'].mean():.2f}%
    """)

# Analysis for Other Dividend stocks
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
        """)

        # Fundamental Analysis
        st.markdown(f"""
        **Fundamental Analysis**  
        • Current Yield: {row['Div Yield (%)']:.2f}% (S&P 500 Avg: 1.5%)  
        • 5Y Dividend Growth: {row['5Y Div Growth (%)'] if row['5Y Div Growth (%)'] is not None else "nan"}%  
        • Payout Ratio: {row['Payout Ratio (%)']:.1f}%  
        • Market Cap: ${row['Market Cap ($B)']:.2f}B  
        • Revenue Trend: {row['Revenue Growth (%)']:.2f}% YoY  
        """)

        # Yield Strength
        st.markdown(f"Yield Strength: {(row['Div Yield (%)'] / 1.5):.2f}x Market Average")

        # Risk/Reward Profile
        st.markdown(f"""
        **Risk/Reward Profile**  
        - Volatility Score: {(100 - abs(row['Payout Ratio (%)'] - 75)):.1f}/100  
        - Yield Sustainability: {"🔴 High Risk" if row['Payout Ratio (%)'] > 90 else "🟡 Moderate" if row['Payout Ratio (%)'] > 75 else "🟢 Stable"}  
        - Growth Potential: {"⭐" * int(row['Revenue Growth (%)'] / 5)}  
        - Value Indicator: {"Undervalued" if row['P/E Ratio'] < 15 else "Fair" if row['P/E Ratio'] < 25 else "Overvalued"}  
        """)

        # Strategic Rationale
        st.markdown(f"""
        **Strategic Rationale**  
        - Projected 5Y Total Return: {0.4 * row['Div Yield (%)'] + 0.6 * row['Revenue Growth (%)']:.1f}%  
        - Dividend Coverage Ratio: {min(100 / (row['Payout Ratio (%)'] or 1), 5):.1f}x  
        - Sector Weighting Impact: {["Enhances Diversification", "Concentrates Exposure"][row['Market Cap ($B)'] > 50]}  
        """)

# ========== Reiva'j Retirement Fund Analysis Section ==========
st.header("Reiva'j Retirement Fund Analysis")
reiva_j_df = get_stock_data(reiva_j_retirement_fund)
st.dataframe(
    reiva_j_df.style.format({
        'Price ($)': '{:.2f}' if isinstance(reiva_j_df['Price ($)'].iloc[0], (int, float)) else '{}',
        'Div Yield (%)': '{:.2f}%' if isinstance(reiva_j_df['Div Yield (%)'].iloc[0], (int, float)) else '{}',
        '5Y Div Growth (%)': '{:.2f}%' if isinstance(reiva_j_df['5Y Div Growth (%)'].iloc[0], (int, float)) else '{}',
        'Payout Ratio (%)': '{:.1f}%' if isinstance(reiva_j_df['Payout Ratio (%)'].iloc[0], (int, float)) else '{}',
    }),
    height=400
)

# Projections for Reiva'j Retirement Fund
if not reiva_j_df.empty:
    total_price_reiva_j = reiva_j_df['Price ($)'].sum()
    avg_div_yield_reiva_j = reiva_j_df['Div Yield (%)'].mean() / 100  # Convert to decimal
    annual_div_reiva_j = (reiva_j_df['Price ($)'] * reiva_j_df['Div Yield (%)'] / 100).sum()

    # Total projected value with reinvestment
    total_projected_value_reiva_j = total_price_reiva_j  # Start with initial investment
    for year in range(1, 6):
        annual_div_reiva_j = (total_projected_value_reiva_j * avg_div_yield_reiva_j)  # Dividends for the year
        total_projected_value_reiva_j += annual_div_reiva_j * (1 + 0.07)  # Reinvest with projected growth

    st.markdown(f"""
    **Reiva'j Retirement Fund Portfolio**  
    - Total Investment: ${total_price_reiva_j:,.2f}  
    - Immediate Annual Dividends: ${annual_div_reiva_j:.2f}  
    - Total Projected Value (5-Year With Reinvestment): ${total_projected_value_reiva_j:,.2f}
    - Average Yield: {reiva_j_df['Div Yield (%)'].mean():.2f}%
    """)

# Analysis for Reiva'j Retirement Fund stocks
for _, row in reiva_j_df.iterrows():
    with st.expander(f"{row['Ticker']} - {row['Company']}"):
        st.subheader("Investment Thesis")
        div_yield = row['Div Yield (%)'] if row['Div Yield (%)'] is not None else 0
        five_y_div_growth = row['5Y Div Growth (%)'] if row['5Y Div Growth (%)'] is not None else 0
        payout_ratio = row['Payout Ratio (%)'] if row['Payout Ratio (%)'] is not None else 0
        price = row['Price ($)'] if row['Price ($)'] is not None else 0
        pe_ratio = row['P/E Ratio'] if row['P/E Ratio'] is not None else 0

        st.markdown(f"""
        **Why Hold:**  
        - {row['Company']} maintains a {div_yield:.2f}% dividend yield with
        {five_y_div_growth:.2f}% average annual growth over 5 years.
        - Payout ratio of {payout_ratio:.1f}% suggests sustainability.
        
        **Dividend Projections ({shares_owned} shares):**  
        - Annual Dividend Income: **${price * shares_owned * div_yield / 100:.2f}**  
        - 5-Year Projected Income (7% growth): **${price * shares_owned * div_yield / 100 * ((1.07 ** 5 - 1) / 0.07):.2f}**

        **Valuation:**  
        - Current P/E: {pe_ratio:.1f} vs Sector Average: {pe_ratio * 0.9:.1f}
        """)

        # Fundamental Analysis
        revenue_growth = row['Revenue Growth (%)'] if row['Revenue Growth (%)'] is not None else 0
        market_cap = row['Market Cap ($B)'] if row['Market Cap ($B)'] is not None else 0

        st.markdown(f"""
        **Fundamental Analysis**  
        • Current Yield: {div_yield:.2f}% (S&P 500 Avg: 1.5%)  
        • 5Y Dividend Growth: {five_y_div_growth:.2f}%  
        • Payout Ratio: {payout_ratio:.1f}%  
        • Market Cap: ${market_cap:.2f}B  
        • Revenue Trend: {revenue_growth:.2f}% YoY  
        """)


        # Yield Strength
        st.markdown(f"Yield Strength: {(row['Div Yield (%)'] / 1.5):.2f}x Market Average")

        # Risk/Reward Profile
        st.markdown(f"""
        **Risk/Reward Profile**  
        - Volatility Score: {(100 - abs(row['Payout Ratio (%)'] - 75)):.1f}/100  
        - Yield Sustainability: {"🔴 High Risk" if row['Payout Ratio (%)'] > 90 else "🟡 Moderate" if row['Payout Ratio (%)'] > 75 else "🟢 Stable"}  
        - Growth Potential: {"⭐" * int(row['Revenue Growth (%)'] / 5)}  
        - Value Indicator: {"Undervalued" if row['P/E Ratio'] < 15 else "Fair" if row['P/E Ratio'] < 25 else "Overvalued"}  
        """)

        # Strategic Rationale
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

# Continue for the PaperChasn section and the combined strategy in tabs 2 and 3...

st.sidebar.markdown("""
**How to Use:**  
1. Enter planned share count in the main input  
2. Explore Aristocrats in the left table  
3. Click ➕ icons for detailed analysis  
4. Compare all stock categories sequentially  
5. Analyze different portfolio strategies via tabs  
""")
