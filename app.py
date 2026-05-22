import streamlit as st
import google.generativeai as genai
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
page_title="AI Financial Assistant",
page_icon="💰",
layout="wide"
)

st.markdown(
""" <style>
.main {
background-color: #0E1117;
}

```
h1, h2, h3 {
    color: #00BFFF;
}

.stButton>button {
    background-color: #00BFFF;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}

.stTextInput>div>div>input {
    border-radius: 10px;
}

.stTextArea textarea {
    border-radius: 10px;
}
</style>
""",
unsafe_allow_html=True

)

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-2.0-flash-lite")

st.markdown(
""" <h1 style='text-align: center;'>
💰 AI Financial Assistant </h1>
""",
unsafe_allow_html=True
)

st.markdown(
""" <p style='text-align: center; font-size:18px;'>
AI-powered financial assistant using Generative AI,
NLP workflows, and real-time financial analytics. </p>
""",
unsafe_allow_html=True
)

st.markdown("---")

st.sidebar.title("💼 Dashboard")

st.sidebar.info(
"AI-powered finance assistant for intelligent financial insights."
)

feature = st.sidebar.radio(
"Select Feature",
[
"Financial Chatbot",
"Financial Sentiment Analysis",
"Finance News Summarizer",
"Stock Market Dashboard",
"Portfolio Analyzer"
]
)

st.sidebar.markdown("---")

st.sidebar.caption(
"Built using Streamlit + Gemini API"
)

if feature == "Financial Chatbot":
    st.subheader("🤖 Financial Chatbot")

st.info(
    "Ask finance-related questions powered by Generative AI."
)

question = st.text_area(
    "Ask any finance-related question"
)

if st.button("Generate Answer"):

    if question:

        prompt = f"""
        You are a professional AI financial assistant.

        Provide clean and professional responses in plain text.

        Rules:
        - No markdown
        - No stars (**)
        - No hashtags (###)
        - Use short paragraphs
        - Keep explanations concise and structured

        Question:
        {question}
        """

        try:

            with st.spinner("Generating AI response..."):

                response = model.generate_content(prompt)

                clean_response = (
                    response.text
                    .replace("###", "")
                    .replace("**", "")
                )

            st.success("Response Generated")

            st.write(clean_response)

        except Exception as e:

            st.error(f"Error: {e}")
            
elif feature == "Financial Sentiment Analysis":
    st.subheader("📈 Financial Sentiment Analysis")

st.info(
    "Analyze sentiment of financial headlines and news."
)

news = st.text_area(
    "Paste financial news headline/article"
)

if st.button("Analyze Sentiment"):

    if news:

        prompt = f"""
        Analyze the sentiment of this financial news.

        Return ONLY:
        Positive
        Neutral
        Negative

        News:
        {news}
        """

        try:

            with st.spinner("Analyzing sentiment..."):

                response = model.generate_content(prompt)

                sentiment = response.text.strip()

            if "Positive" in sentiment:
                st.success(f"Sentiment: {sentiment}")

            elif "Negative" in sentiment:
                st.error(f"Sentiment: {sentiment}")

            else:
                st.warning(f"Sentiment: {sentiment}")

        except Exception as e:

            st.error(f"Error: {e}")
            
elif feature == "Finance News Summarizer":
    st.subheader("📰 Finance News Summarizer")

st.info(
    "Generate concise AI summaries from financial articles."
)

article = st.text_area(
    "Paste finance news/article"
)

if st.button("Summarize News"):

    if article:

        prompt = f"""
        Summarize the following financial article.

        Rules:
        - Keep summary concise
        - Use plain text
        - Avoid markdown
        - Mention important financial insights

        Article:
        {article}
        """

        try:

            with st.spinner("Generating summary..."):

                response = model.generate_content(prompt)

                clean_response = (
                    response.text
                    .replace("###", "")
                    .replace("**", "")
                )

            st.success("Summary Generated")

            st.write(clean_response)

        except Exception as e:

            st.error(f"Error: {e}")

elif feature == "Stock Market Dashboard":
    st.subheader("📊 Stock Market Dashboard")

st.info(
    "Visualize stock performance and AI-generated insights."
)

ticker = st.text_input(
    "Enter Stock Ticker",
    value="AAPL"
)

if st.button("Fetch Stock Data"):

    try:

        stock = yf.Ticker(ticker)

        hist = stock.history(period="6mo")

        if hist.empty:

            st.error("No stock data found")

        else:

            latest_price = hist["Close"].iloc[-1]

            highest_price = hist["High"].max()

            lowest_price = hist["Low"].min()

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Latest Price",
                round(latest_price, 2)
            )

            col2.metric(
                "Highest Price",
                round(highest_price, 2)
            )

            col3.metric(
                "Lowest Price",
                round(lowest_price, 2)
            )

            st.subheader(f"{ticker} Stock Data")

            st.dataframe(hist.tail())

            fig, ax = plt.subplots(figsize=(10, 5))

            ax.plot(
                hist.index,
                hist["Close"],
                linewidth=3
            )

            ax.set_title(f"{ticker} Closing Prices")

            ax.set_xlabel("Date")

            ax.set_ylabel("Price")

            ax.grid(True, linestyle="--", alpha=0.5)

            st.pyplot(fig)

            prompt = f"""
            Analyze this stock information.

            Ticker: {ticker}

            Latest Price: {latest_price}

            Highest Price: {highest_price}

            Lowest Price: {lowest_price}

            Provide:
            1. Trend summary
            2. Risk observation
            3. General financial insight

            Keep answer concise.
            """

            with st.spinner("Generating AI stock insights..."):

                response = model.generate_content(prompt)

                clean_response = (
                    response.text
                    .replace("###", "")
                    .replace("**", "")
                )

            st.subheader("📌 AI Stock Insights")

            st.write(clean_response)

    except Exception as e:

        st.error(f"Error: {e}")

elif feature == "Portfolio Analyzer":
    st.subheader("📂 Portfolio Analyzer")

st.info(
    "Analyze stock portfolios using AI-driven insights."
)

portfolio = st.text_input(
    "Enter stock tickers separated by commas",
    value="AAPL,MSFT,TSLA"
)

if st.button("Analyze Portfolio"):

    try:

        stocks = portfolio.split(",")

        portfolio_data = {}

        for stock_name in stocks:

            stock_name = stock_name.strip()

            stock = yf.Ticker(stock_name)

            hist = stock.history(period="1mo")

            if not hist.empty:

                latest_close = hist["Close"].iloc[-1]

                portfolio_data[stock_name] = latest_close

        portfolio_df = pd.DataFrame(
            portfolio_data.items(),
            columns=["Stock", "Latest Price"]
        )

        st.subheader("📋 Portfolio Overview")

        st.dataframe(portfolio_df)

        prompt = f"""
        Analyze this stock portfolio.

        Portfolio Data:
        {portfolio_df.to_string(index=False)}

        Provide:
        1. Diversification insight
        2. Risk observation
        3. General market suggestion

        Keep response concise.
        """

        with st.spinner("Generating AI portfolio insights..."):

            response = model.generate_content(prompt)

            clean_response = (
                response.text
                .replace("###", "")
                .replace("**", "")
            )

        st.subheader("📌 AI Portfolio Insights")

        st.write(clean_response)

    except Exception as e:

        st.error(f"Error: {e}")

st.markdown("---")

st.caption(
"AI Financial Assistant • Built with Streamlit, Gemini API, and Financial Analytics"
)