import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(page_title="Dividend Aristocrat Analyzer", layout="wide")

# ========== Insight Function ==========
def generate_insight(ticker):
    insights = {
        'JNJ': "Johnson & Johnson has a strong history of dividend payments and a diverse product portfolio, making it a reliable choice for income investors.",
        'PG': "Procter & Gamble is a leader in consumer goods with consistent revenue growth and strong brand loyalty.",
        'KO': "Coca-Cola benefits from a global brand presence and strong cash flow, supported by its extensive distribution network.",
        'PEP': "PepsiCo's diversification in snacks and beverages ensures steady growth, even in fluctuating markets.",
        'ABBV': "AbbVie has a strong pipeline of drugs and a commitment to returning value to shareholders through dividends.",
        'TGT': "Target's robust e-commerce strategy and strong brand positioning help it maintain competitive advantages.",
        'ED': "Consolidated Edison provides stable dividends backed by regulated utility operations, appealing to conservative investors.",
        'MMM': "3M Company is known for its innovation and has a diverse product range, contributing to its long-term stability.",
        'CL': "Colgate-Palmolive focuses on personal care and household products, ensuring consistent demand and revenue.",
        'ADM': "Archer-Daniels-Midland is a global leader in agricultural processing, benefiting from diverse revenue streams.",
        'AOS': "A. O. Smith has a strong presence in the water heating industry, with consistent demand for its products.",
        'ABT': "Abbott Laboratories is known for its medical devices and diagnostics, maintaining a strong dividend growth track record.",
        'APD': "Air Products and Chemicals is a leader in industrial gases, benefiting from long-term contracts and stable cash flows.",
        'ALB': "Albemarle Corporation is a key player in lithium production, positioned well in the growing electric vehicle market.",
        'AMCR': "Amcor's focus on sustainable packaging solutions aligns with global trends towards environmental responsibility.",
        'T': "AT&T offers high dividend yields, but investors should consider its debt levels and competitive landscape.",
        'ADP': "Automatic Data Processing provides payroll and HR services, benefiting from recurring revenue models.",
        'BDX': "Becton Dickinson is a leader in medical technology, with strong growth prospects in the healthcare sector.",
        'BRO': "Brown & Brown is a leading insurance brokerage firm, known for its consistent financial performance.",
        'CHRW': "C.H. Robinson's logistics and supply chain solutions make it a vital player in global trade.",
        'CAH': "Cardinal Health's role in healthcare distribution provides stability and growth potential.",
        'CVX': "Chevron is a major player in the energy sector, with a focus on returning capital to shareholders through dividends.",
        'CINF': "Cincinnati Financial has a strong track record in property and casualty insurance, appealing to risk-averse investors.",
        'CLX': "Clorox's strong brand portfolio in cleaning and consumer products supports consistent revenue growth.",
        'DOV': "Dover Corporation's diverse industrial products ensure stability and growth across various sectors.",
        'EMR': "Emerson Electric is a leader in automation solutions, benefiting from increased industrial demand.",
        'ESS': "Essex Property Trust focuses on high-quality residential properties in prime locations, ensuring steady rental income.",
        'XOM': "ExxonMobil is a leading integrated oil and gas company, providing strong dividends despite market volatility.",
        'FRT': "Federal Realty Investment Trust focuses on retail properties, benefiting from strong consumer demand.",
        'BEN': "Franklin Resources is a global investment management firm, known for its consistent dividend payments.",
        'GD': "General Dynamics is a leader in defense and aerospace, providing stability amid government contracts.",
        'GPC': "Genuine Parts Company is a distributor of automotive and industrial parts, benefiting from steady demand.",
        'HRL': "Hormel Foods has a diverse product line in the food sector, ensuring consistent revenue streams.",
        'ITW': "Illinois Tool Works is known for its diversified industrial products, providing stability and growth.",
        'KMB': "Kimberly-Clark's strong brand portfolio in consumer goods supports consistent cash flow.",
        'LOW': "Lowe's benefits from a strong position in the home improvement sector, appealing to DIY consumers.",
        'MKC': "McCormick & Company is a leader in spices and flavorings, benefiting from steady consumer demand.",
        'NEE': "NextEra Energy is a leader in renewable energy, positioning itself well for future growth.",
        'NDSN': "Nordson Corporation specializes in adhesive dispensing equipment, benefiting from diverse industrial applications.",
        'SHW': "Sherwin-Williams is a leader in paint and coatings, with a strong brand presence and growth potential.",
        'SWK': "Stanley Black & Decker is known for its tools and storage solutions, appealing to both consumers and professionals.",
        'SYY': "Sysco is a leading foodservice distributor, benefiting from strong demand in the hospitality sector.",
        'TROW': "T. Rowe Price is a global investment management firm, known for its strong performance and dividends.",
        'TR': "Tootsie Roll Industries has a strong brand presence in the confectionery market, ensuring steady sales.",
        'VFC': "V.F. Corporation is a leader in branded apparel, benefiting from strong consumer loyalty and brand recognition.",
        'O': "Realty Income is known for its monthly dividends and focus on commercial real estate, appealing to income investors.",
        'MAIN': "Main Street Capital focuses on providing debt and equity capital to lower middle-market companies, offering strong yields.",
        'HD': "Home Depot benefits from a strong position in home improvement, appealing to both DIY and professional markets.",
        'IBM': "International Business Machines is focused on cloud computing and AI, providing growth potential in tech.",
        'AFL': "Aflac is a leader in supplemental insurance, known for its strong dividend history.",
        'ARE': "Alexandria Real Estate Equities focuses on life science real estate, benefiting from consistent demand.",
        'ALL': "Allstate provides insurance products, known for its focus on customer service and steady dividends.",
        'MO': "Altria Group is a major player in the tobacco industry, with a focus on returning capital to shareholders.",
        'AEE': "Ameren provides utility services with a focus on renewable energy, appealing to environmentally conscious investors.",
        'AEP': "American Electric Power is a major utility provider, known for its stable dividends.",
        'AWR': "American States Water provides essential water services, ensuring stable revenue streams.",
        'AMT': "American Tower Corporation benefits from the growing demand for telecommunications infrastructure.",
        'COLD': "Americold Realty Trust focuses on temperature-controlled warehouses, appealing to the food supply chain.",
        'APTV': "Aptiv is a leader in automotive technology, benefiting from trends towards electric vehicles.",
        'AVB': "AvalonBay Communities focuses on residential properties, ensuring steady rental income.",
        'BRK-B': "Berkshire Hathaway is a diversified holding company, known for strong management and long-term value.",
        'BBY': "Best Buy benefits from a strong retail presence in electronics, appealing to tech-savvy consumers.",
        'BLK': "BlackRock is a global leader in investment management, known for its strong performance and dividends.",
        'BWA': "BorgWarner specializes in automotive components, benefiting from trends towards electric vehicles.",
        'BXP': "Boston Properties focuses on high-quality office spaces, appealing to corporate clients.",
        'BMY': "Bristol-Myers Squibb has a strong pipeline of drugs, providing growth potential in healthcare.",
        'AVGO': "Broadcom is a leader in semiconductor technology, benefiting from strong demand in tech.",
        'CCJ': "Cameco is a major player in uranium production, benefiting from the growing demand for nuclear energy.",
        'CAT': "Caterpillar is a leader in construction and mining equipment, with a strong global presence.",
        'ATO': "Atmos Energy provides natural gas distribution, appealing to utility investors.",
        'CSCO': "Cisco Systems is a leader in networking hardware and software, benefiting from the growth in digital infrastructure.",
        'D': "Dominion Energy focuses on utility services with a commitment to renewable energy.",
        'DUK': "Duke Energy is a major utility provider, known for its stable dividends and focus on sustainability.",
        'DTE': "DTE Energy focuses on utility services in the Midwest, appealing to conservative investors.",
        'ETN': "Eaton Corporation specializes in power management solutions, benefiting from industrial demand.",
        'EVRG': "Evergy provides utility services in the Midwest, ensuring stable revenue streams.",
        'ES': "Eversource Energy focuses on utility services in New England, known for reliable service.",
        'EXC': "Exelon is a major utility provider with a focus on renewable energy, appealing to environmentally conscious investors.",
        'FE': "FirstEnergy provides utility services in the Midwest and Northeast, known for stable dividends.",
        'GIS': "General Mills is a leader in consumer packaged goods, ensuring consistent demand for its products.",
        'HRL': "Hormel Foods has a diverse product line in the food sector, ensuring consistent revenue streams.",
        'HST': "Host Hotels & Resorts focuses on high-quality hotel properties, appealing to tourism and travel markets.",
        'ICE': "Intercontinental Exchange operates financial markets and data services, benefiting from steady demand.",
        'IRM': "Iron Mountain specializes in information management, appealing to businesses needing secure storage.",
        'JNJ': "Johnson & Johnson has a strong history of dividend payments and a diverse product portfolio.",
        'KIM': "Kimco Realty focuses on retail real estate, benefiting from consumer demand.",
        'KMI': "Kinder Morgan is a leader in energy infrastructure, known for its strong dividends.",
        'KR': "Kroger is a major player in the grocery sector, ensuring consistent revenue.",
        'LMT': "Lockheed Martin is a leader in defense contracting, providing stability amid government contracts.",
        'LNT': "Alliant Energy provides utility services in the Midwest, appealing to conservative investors.",
        'LHX': "L3Harris Technologies focuses on defense and aerospace technology, benefiting from government contracts.",
        'MAA': "Mid-America Apartment Communities focuses on residential properties, ensuring steady rental income.",
        'MMM': "3M Company is known for its innovation and diverse product range, contributing to its long-term stability.",
        'NEE': "NextEra Energy is a leader in renewable energy, positioning itself well for future growth.",
        'NI': "NiSource provides utility services in the Midwest, known for stable dividends.",
        'NTRS': "Northern Trust is a leader in asset management, known for strong performance and dividends.",
        'NUE': "Nucor is a major player in steel production, benefiting from industrial demand.",
        'OKE': "ONEOK focuses on natural gas distribution, appealing to utility investors.",
        'PPL': "PPL Corporation provides utility services in the Northeast, known for stable dividends.",
        'PEG': "Public Service Enterprise Group focuses on utility services in New Jersey, appealing to conservative investors.",
        'PEP': "PepsiCo's diversification in snacks and beverages ensures steady growth.",
        'PFG': "Principal Financial Group is a leader in financial services, known for strong performance.",
        'PG': "Procter & Gamble is a leader in consumer goods with consistent revenue growth.",
        'PNW': "Pinnacle West Capital provides utility services in Arizona, known for stable dividends.",
        'RTX': "Raytheon Technologies focuses on defense and aerospace, benefiting from government contracts.",
        'SBUX': "Starbucks has a strong brand presence in the coffee sector, ensuring consistent revenue.",
        'SO': "Southern Company provides utility services in the Southeast, appealing to conservative investors.",
        'SPG': "Simon Property Group focuses on retail real estate, benefiting from consumer demand.",
        'T': "AT&T offers high dividend yields, but investors should consider its debt levels and competitive landscape.",
        'TGT': "Target's robust e-commerce strategy and strong brand positioning help it maintain competitive advantages.",
        'TRV': "The Travelers Companies provides insurance products, known for its focus on customer service.",
        'UDR': "UDR focuses on residential properties, ensuring steady rental income.",
        'USB': "U.S. Bancorp is a major player in banking, known for strong performance and dividends.",
        'VLO': "Valero Energy is a major player in refining, benefiting from strong demand for fuels.",
        'VTR': "Ventas focuses on healthcare real estate, appealing to income investors.",
        'VZ': "Verizon Communications is a leader in telecommunications, known for steady dividends.",
        'WEC': "WEC Energy Group provides utility services in the Midwest, appealing to conservative investors.",
        'WFC': "Wells Fargo is a major player in banking, known for strong performance and dividends.",
        'WMB': "Williams Companies focuses on natural gas infrastructure, appealing to utility investors.",
        'XEL': "Xcel Energy focuses on renewable energy, appealing to environmentally conscious investors."
    }
    return insights.get(ticker, "No specific insight available.")

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
                total_comb = combined_df['Price ($)'].sum()
        annual_div_comb = (combined_df['Price ($)'] * combined_df['Div Yield (%)'] / 100).sum()
        five_year_comb = annual_div_comb * ((1.07 ** 5 - 1) / 0.07)
        
        st.markdown(f"""
        **Combined Portfolio**  
        - Total Investment: ${total_comb:,.2f}  
        - Immediate Annual Dividends: ${annual_div_comb:.2f}  
        - 5-Year Projection (7% growth): ${five_year_comb:.2f}  
        - Average Yield: {combined_df['Div Yield (%)'].mean():.2f}%
        """)
    else:
        st.warning("No data available for the combined portfolio.")

# ========== Conclusion ==========
st.header("Conclusion")
st.markdown("""
Investing in dividend stocks can provide a steady income stream and potential for capital appreciation. By analyzing dividend aristocrats and other reliable dividend payers, investors can build a robust portfolio that offers both stability and growth.

Consider your investment horizon and risk tolerance when selecting stocks, and always diversify your holdings to mitigate risks.
""")

# ========== Final Notes ==========
st.sidebar.header("Additional Resources")
st.sidebar.markdown("""
- [Investopedia - Dividend Investing](https://www.investopedia.com/terms/d/dividend.asp)
- [Yahoo Finance](https://finance.yahoo.com/)
- [Seeking Alpha](https://seekingalpha.com/)
""")


