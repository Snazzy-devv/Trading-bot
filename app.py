# %%
import streamlit as st
from dotenv import load_dotenv
import os
import json
import pandas as pd
from datetime import datetime
from openai import OpenAI

# %% Load environment variables
load_dotenv(override=True)

# Set OpenRouter API Key & Base URL
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"

# Instantiate OpenAI client
ai_client = OpenAI(
    base_url=BASE_URL,
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

# %% Trade log file
LOG_FILE = "trade_history.csv"

# %% AI Analysis Function
def get_institutional_analysis(symbol, data, risk_level):
    """Generates AI-based trading recommendation."""
    risk_desc = (
        "extremely conservative" if risk_level < 30
        else "balanced" if risk_level < 70
        else "aggressive"
    )
    
    prompt = f"""
You are a Senior Risk Officer at a Tier-1 Investment Bank. 
Asset: {symbol}
Current Data: {data}
Client Risk Tolerance: {risk_desc} ({risk_level}/100)

Instructions:
1. Provide the most suitable action: BUY, SELL, or HOLD, based on market data and risk.
2. Explain reasoning in 'institutional_reasoning'.
3. Identify one 'Primary Risk Factor' that could cause failure.
4. Suggest qty, stop-loss (sl), and take-profit (tp).

Return ONLY a JSON object:
{{
    "action": "BUY/SELL/HOLD",
    "qty": 1.0,
    "risk_assessment": "Describe the main risk",
    "institutional_reasoning": "Professional explanation here",
    "sl": 0.0,
    "tp": 0.0
}}
"""
    response = ai_client.chat.completions.create(
        model="gpt-4o-mini",  # <--- Changed from invalid Gemini model
        messages=[
            {"role": "system", "content": "You are an institutional trading agent."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return json.loads(response.choices[0].message.content)

# %% Trade Logging Functions
def log_trade(symbol, side, qty, reason, status="Executed"):
    """Save trade details to CSV log."""
    new_entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Asset": symbol,
        "Action": side,
        "Qty": qty,
        "Status": status,
        "AI_Reasoning": reason
    }
    try:
        df = pd.read_csv(LOG_FILE)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([new_entry])
    df.to_csv(LOG_FILE, index=False)

def get_logs():
    """Return last 10 trades."""
    try:
        return pd.read_csv(LOG_FILE).tail(10).iloc[::-1]
    except FileNotFoundError:
        return pd.DataFrame()

# %% Fake Execution Function (replace with real broker API)
def execute_bracket_order(symbol, qty, action, tp, sl, is_forex=False):
    """Mock order execution."""
    print(f"Executing {action} order for {symbol} qty={qty}, TP={tp}, SL={sl}")
    return True

# %% Streamlit UI Setup
st.set_page_config(page_title="Institutional AI Terminal", layout="wide")
st.title("Agentic Multi-Asset Terminal")
st.info("Currently in **Paper Trading Mode** (Zero Financial Risk)")

col1, col2 = st.columns([1,1])

# %% Column 1: AI Analysis
with col1:
    st.subheader("1. AI Market Analysis")
    asset = st.text_input("Ticker (e.g. BTC/USD, TSLA, ETH/USD)", "BTC/USD")
    risk_val = st.slider("Institutional Risk Tolerance", 0, 100, 20)
    context = st.text_area("Market Intelligence", "Analyzing 4h charts and recent sentiment.")

    if st.button("🧠 Run AI Agent"):
        with st.spinner("Agent generating risk-adjusted proposal..."):
            try:
                res = get_institutional_analysis(asset, context, risk_val)
                st.session_state.current_analysis = res
                st.success("Analysis Complete!")
            except Exception as e:
                st.error(f"AI Analysis Failed: {e}")

# %% Column 2: Human-in-the-loop Execution
with col2:
    st.subheader("2. Human-in-the-Loop Execution")
    if "current_analysis" in st.session_state:
        res = st.session_state.current_analysis
        st.write(f"**Recommendation:** [{res['action']}]")
        st.write(f"**Risk Factor:** {res['risk_assessment']}")
        st.caption(f"Reasoning: {res['institutional_reasoning']}")
        
        if res['action'] != "HOLD":
            if st.button(f"Confirm & Execute {res['action']} Order"):
                try:
                    execute_bracket_order(asset, res['qty'], res['action'], res['tp'], res['sl'], "/" in asset)
                    log_trade(asset, res['action'], res['qty'], res['institutional_reasoning'])
                    st.success("Order filled with Bracket Protection.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Execution Failed: {e}")
        else:
            st.warning("Agent advises 'No Trade' under current risk parameters.")

# %% Trade History Section
st.markdown("---")
st.subheader("📜 Audit Trail (Trade History)")
history = get_logs()
if not history.empty:
    st.dataframe(history, use_container_width=True)
else:
    st.write("No trades recorded yet.")
