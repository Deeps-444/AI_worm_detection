

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from simulation import (
    MultiAgentSystem,
    run_normal_simulation,
    run_worm_attack
)

st.set_page_config(
    page_title="AI Worm Detection",
    page_icon="🛡️",
    layout="wide"
)

# ======================================================
# STYLING
# ======================================================

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #f5f5f5;
        margin-bottom: 0;
    }
    .subtitle {
        color: #9aa0a6;
        font-size: 0.95rem;
        margin-top: 0;
        margin-bottom: 1.2rem;
    }
    .status-banner {
        padding: 14px 20px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
        border: 1px solid;
    }
    .status-safe {
        background: rgba(46, 204, 113, 0.10);
        border-color: #2ecc71;
        color: #2ecc71;
    }
    .status-warning {
        background: rgba(241, 196, 15, 0.10);
        border-color: #f1c40f;
        color: #f1c40f;
    }
    .status-danger {
        background: rgba(231, 76, 60, 0.12);
        border-color: #e74c3c;
        color: #e74c3c;
    }
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #262d38;
        border-radius: 10px;
        padding: 14px 10px;
    }
    .badge {
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-block   { background: rgba(231,76,60,0.15); color: #e74c3c; }
    .badge-restrict{ background: rgba(230,126,34,0.15); color: #e67e22; }
    .badge-monitor { background: rgba(241,196,15,0.15); color: #f1c40f; }
    .badge-allow   { background: rgba(46,204,113,0.15); color: #2ecc71; }
    .badge-yes     { background: rgba(231,76,60,0.15); color: #e74c3c; }
    .badge-no      { background: rgba(46,204,113,0.12); color: #2ecc71; }

    .event-line {
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        padding: 3px 0;
        color: #d1d5db;
        border-bottom: 1px solid #1c222c;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================

st.markdown('<p class="main-title">🛡️ AI Worm Detection & Containment</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Runtime monitoring simulation for a multi-agent system</p>', unsafe_allow_html=True)

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.header("⚙️ Simulation Controls")

num_agents = st.sidebar.slider("Number of Agents", 4, 10, 6)

st.sidebar.markdown("---")
st.sidebar.markdown("**Legend**")
st.sidebar.markdown("🟢 Healthy  🟠 Compromised  🔴 Isolated")

if "system" not in st.session_state:
    st.session_state.system = MultiAgentSystem(num_agents)

system = st.session_state.system

# ======================================================
# CONTROL BUTTONS
# ======================================================

col1, col2, col3 = st.columns(3)

with col1:
    run_normal = st.button("▶️  Run Normal Traffic", use_container_width=True)

with col2:
    run_attack = st.button("☣️  Start Worm Attack", use_container_width=True, type="primary")

with col3:
    reset = st.button("🔄  Reset Simulation", use_container_width=True)

if run_normal:
    run_normal_simulation(system)

if run_attack:
    run_worm_attack(system)

if reset:
    st.session_state.system = MultiAgentSystem(num_agents)
    st.rerun()

# ======================================================
# STATUS BANNER
# ======================================================

isolated_count = sum(a.isolated for a in system.agents.values())
compromised_count = sum(a.compromised for a in system.agents.values())
blocked = system.monitor.blocked_messages

if blocked > 0 or isolated_count > 0:
    st.markdown(
        f'<div class="status-banner status-danger">🚨 THREAT CONTAINED — '
        f'{blocked} message(s) blocked, {isolated_count} agent(s) isolated</div>',
        unsafe_allow_html=True
    )
elif compromised_count > 0:
    st.markdown(
        '<div class="status-banner status-warning">⚠️ COMPROMISED AGENT DETECTED — monitoring traffic</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="status-banner status-safe">✅ SYSTEM NOMINAL — no threats detected</div>',
        unsafe_allow_html=True
    )

# ======================================================
# METRICS
# ======================================================

total_messages = sum(a.messages_sent for a in system.agents.values())
detected_agents = len(system.monitor.detected_agents)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Agents", len(system.agents))
c2.metric("Messages Sent", total_messages)
c3.metric("Blocked", blocked, delta=None)
c4.metric("Isolated", isolated_count)
c5.metric("Compromised", compromised_count)

st.write("")

# ======================================================
# TABS
# ======================================================

tab_network, tab_agents, tab_logs, tab_events = st.tabs(
    ["🕸️ Network", "🧑‍💻 Agent Status", "📋 Monitoring Logs", "🖥️ Event Feed"]
)

# --- NETWORK TAB ---
with tab_network:
    G = nx.DiGraph()
    for agent in system.agents.values():
        G.add_node(agent.agent_id)
        for receiver in agent.connections:
            G.add_edge(agent.agent_id, receiver)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")

    pos = nx.spring_layout(G, seed=42) if len(G.nodes) else {}

    node_colors = []
    for node in G.nodes:
        agent = system.agents[node]
        if agent.isolated:
            node_colors.append("#e74c3c")
        elif agent.compromised:
            node_colors.append("#e67e22")
        else:
            node_colors.append("#3498db")

    nx.draw(
        G, pos, ax=ax,
        with_labels=True,
        node_color=node_colors if node_colors else "#3498db",
        node_size=2200,
        edge_color="#4b5563",
        font_color="white",
        font_weight="bold",
        font_size=9,
        arrows=True,
        arrowsize=18,
        width=1.4
    )
    st.pyplot(fig)

    st.markdown(
        "🔵 Healthy &nbsp;&nbsp; 🟠 Compromised &nbsp;&nbsp; 🔴 Isolated",
        unsafe_allow_html=True
    )

# --- AGENT STATUS TAB ---
with tab_agents:
    agent_data = []
    for agent in system.agents.values():
        agent_data.append({
            "Agent": agent.agent_id,
            "Compromised": "🟠 Yes" if agent.compromised else "🟢 No",
            "Isolated": "🔴 Yes" if agent.isolated else "🟢 No",
            "Messages Sent": agent.messages_sent,
            "Messages Received": agent.messages_received,
        })
    st.dataframe(pd.DataFrame(agent_data), use_container_width=True, hide_index=True)

# --- LOGS TAB ---
with tab_logs:
    logs = system.monitor.logs
    if logs:
        df_logs = pd.DataFrame(logs)

        def decision_badge(d):
            colors = {"BLOCK": "🔴", "RESTRICT": "🟠", "MONITOR": "🟡", "ALLOW": "🟢"}
            return f"{colors.get(d, '')} {d}"

        df_logs["decision"] = df_logs["decision"].apply(decision_badge)
        st.dataframe(df_logs, use_container_width=True, hide_index=True)
    else:
        st.info("No suspicious activity detected yet.")

# --- EVENTS TAB ---
with tab_events:
    if system.events:
        for event in reversed(system.events):
            if "BLOCK" in event:
                icon = "🔴"
            elif "compromised" in event.lower():
                icon = "🟠"
            elif "RESTRICT" in event:
                icon = "🟡"
            else:
                icon = "🟢"
            st.markdown(f'<div class="event-line">{icon} {event}</div>', unsafe_allow_html=True)
    else:
        st.info("No events yet — run a simulation to see activity here.")