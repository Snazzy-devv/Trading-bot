# %%
import streamlit as st
#import bot
#import tools
from dotenv import load_dotenv
import os

from openai import OpenAI
import os
import json


# %%
load_dotenv(override=True)

# %%
os.environ["OPENROUTER_API_KEY"]= os.getenv("OPENROUTER_API_KEY")
os.environ["base_url"]= "https://openrouter.ai/api/v1"

ai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


# %%
def get_institutional_analysis(symbol, data, risk_level):
    # Adjusting the persona based on the UI slider
    risk_desc = "extremely conservative" if risk_level < 30 else "balanced" if risk_level < 70 else "aggressive"
    
    prompt = f"""
    You are a Senior Risk Officer at a Tier-1 Investment Bank. 
    Asset: {symbol}
    Current Data: {data}
    Client Risk Tolerance: {risk_desc} ({risk_level}/100)

    Instructions:
    1. If the risk exceeds the tolerance, return 'HOLD'.
    2. Analyze technicals and sentiment.
    3. You MUST identify one 'Primary Risk Factor' that could cause this trade to fail.
    
    Return ONLY a JSON object:
    {{
        "action": "BUY/SELL/HOLD",
        "quantity": 1.0,
        "risk_assessment": "The specific danger to this trade is...",
        "institutional_reasoning": "Professional explanation here",
        "stop_loss": 0.0,
        "take_profit": 0.0
    }}
    """
    response = ai_client.chat.completions.create(
        model="google/gemini-2.0-flash-exp:free",
        messages=[{"role": "system", "content": "You are an institutional trading agent."},
                  {"role": "user", "content":prompt}]
    )
    return json.loads(response.choices[0].message.content)


import pandas as pd
from datetime import datetime

# %%
LOG_FILE = "trade_history.csv"

# %%
def log_trade(symbol, side, qty, reason, status="Executed"):
    """Saves trade details to a CSV for the dashboard history."""
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
    """Retrieves the last 10 trades."""
    try:
        return pd.read_csv(LOG_FILE).tail(10).iloc[::-1] # Newest first
    except FileNotFoundError:
        return pd.DataFrame()








# %%
st.set_page_config(page_title="Institutional AI Terminal", layout="wide")

# %%
# --- SIDEBAR: LIVE DATA ---

# %%
st.sidebar.title("🏛️ Portfolio Monitor")

# %%
try:
    acc = tools.get_account_status()
    st.sidebar.metric("Paper Cash", f"${acc['cash']:,.2f}")
    st.sidebar.metric("Buying Power", f"${acc['buying_power']:,.2f}")
except:
    st.sidebar.error("API Connection Offline")


# %%
# --- MAIN UI ---
st.title("Agentic Multi-Asset Terminal")
st.info("Currently operating in **Paper Trading Mode** (Zero Financial Risk)")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. AI Market Analysis")
    asset = st.text_input("Ticker (e.g. BTC/USD, TSLA, ETH/USD)", "BTC/USD")
    risk_val = st.slider("Institutional Risk Tolerance", 0, 100, 20)
    context = st.text_area("Market Intelligence", "Analyzing 4h charts and recent FOMC sentiment.")

    if st.button("🧠 Run AI Agent"):
        with st.spinner("Agent generating risk-adjusted proposal..."):
            res = bot.get_institutional_analysis(asset, context, risk_val)
            st.session_state.current_analysis = res

with col2:
    st.subheader("2. Human-in-the-Loop Execution")
    if "current_analysis" in st.session_state:
        res = st.session_state.current_analysis
        
        # Professional UI for the Proposal
        with st.container(border=True):
            st.write(f"**Recommendation:** :{ 'green' if res['action'] == 'BUY' else 'red' if res['action'] == 'SELL' else 'orange' }[{res['action']}]")
            st.markdown(f"**Risk Factor:** {res['risk_assessment']}")
            st.caption(f"Reasoning: {res['institutional_reasoning']}")
            
            if res['action'] != "HOLD":
                # APPROVAL BUTTON
                if st.button(f"Confirm & Execute {res['action']} Order"):
                    try:
                        # 1. Physical Execution
                        tools.execute_bracket_order(asset, res['qty'], res['action'], res['tp'], res['sl'], "/" in asset)
                        # 2. Log for History
                        tools.log_trade(asset, res['action'], res['qty'], res['institutional_reasoning'])
                        st.success("Order filled with Bracket Protection.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Execution Failed: {e}")
            else:
                st.warning("Agent advises 'No Trade' under current risk parameters.")




# %%
# --- SECTION 3: TRADE HISTORY ---
st.markdown("---")
st.subheader("📜 Audit Trail (Trade History)")
#history = tools.get_logs()
#if not history.empty:
  #  st.dataframe(history, use_container_width=True)
#else:
  #  st.write("No trades recorded yet. Run an analysis and approve a trade to see the log.")


