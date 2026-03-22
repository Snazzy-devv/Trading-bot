🏛️ Institutional AI Trading Terminal
An Agentic Multi-Asset Trading Terminal that bridges the gap between LLM-based market reasoning and real-world execution. This bot doesn't just "trade"—it acts as a Senior Risk Officer, subjecting every trade idea to institutional-grade scrutiny before allowing human-confirmed execution.

🧠 Core Philosophy: "Human-in-the-Loop"
Unlike "black-box" algorithmic bots, this terminal uses an Agentic Workflow:

Analysis: The AI synthesizes technical data and market sentiment.

Stress Test: The agent identifies a "Primary Risk Factor" that could cause the trade to fail.

Approval: A human trader reviews the AI’s reasoning and confirms execution with one click.

✨ Key Features
Institutional Persona: Powered by Gemini-2.0-Flash via OpenRouter, simulating a Tier-1 Investment Bank's risk assessment protocol.

Dynamic Risk Tolerance: A slider-based UI that shifts the AI's logic from Extremely Conservative to Aggressive.

Bracket Order Protection: Automatically proposes Stop-Loss and Take-Profit levels for every trade.

Paper Trading Integration: Operating in a zero-risk environment for strategy validation.

Audit Trail: Persistent logging of AI reasoning and execution history to trade_history.csv for post-trade analysis.

🛠️ Technical Stack
Frontend: Streamlit

LLM Orchestration: OpenRouter API

Reasoning Engine: Google Gemini 2.0 Flash

Data Science: Pandas & NumPy

Environment: Python-Dotenv for secure API management

🚀 Quick Start
1. Prerequisites
Ensure you have an OpenRouter API key and your trading provider keys (Alpaca/MetaTrader/etc.).

2. Installation
Bash
# Clone the repository
git clone https://github.com/Snazzy-devv/Trading-bot.git
cd Trading-bot

# Install dependencies
pip install -r requirements.txt
3. Environment Setup
Create a .env file in the root directory:

Code snippet
OPENROUTER_API_KEY=your_key_here
# Add other provider keys used in tools.py
4. Launch the Terminal
Bash
streamlit run app.py
📈 Terminal Workflow
Input Asset: Enter any ticker (e.g., BTC/USD or TSLA).

Define Context: Provide current market intelligence (e.g., "FOMC meeting today").

Run Agent: The AI generates a structured JSON proposal including:

Action: BUY/SELL/HOLD

Risk Assessment: A specific warning on why the trade might fail.

Institutional Reasoning: A professional-grade thesis.

Execute: Review the bracket order and hit "Confirm" to push to the exchange.

⚠️ Disclaimer
This project is for educational purposes only. The "Paper Trading" mode should always be used for testing. Trading involves significant financial risk.
