import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data import competitors, market_data, porters_five_forces

st.set_page_config(page_title="Market Entry Analysis Tool", layout="wide")

st.title("🔍 Market Entry Analysis Tool")
st.subheader("Indian D2C Skincare Market — 2026")
st.markdown("---")

# --- SECTION 1: MARKET OVERVIEW ---
st.header("📊 Market Overview")
col1, col2, col3 = st.columns(3)
col1.metric("TAM", market_data["TAM"])
col2.metric("SAM", market_data["SAM"])
col3.metric("SOM", market_data["SOM"])

st.markdown(f"**Growth Rate:** {market_data['growth_rate']}")
st.markdown("**Key Market Trends:**")
for trend in market_data["key_trends"]:
    st.markdown(f"- {trend}")

st.markdown("---")

# --- SECTION 2: COMPETITOR TABLE ---
st.header("🏢 Competitor Landscape")
df = pd.DataFrame(competitors)
st.dataframe(df[["name", "founded", "funding", "price_range",
                   "target_segment", "distribution", "tier2_presence"]])

st.markdown("---")

# --- SECTION 3: PORTER'S FIVE FORCES ---
st.header("⚡ Porter's Five Forces Analysis")

forces = list(porters_five_forces.keys())
scores = [porters_five_forces[f]["score"] for f in forces]
labels = [f.replace("_", " ").title() for f in forces]

fig = go.Figure(go.Bar(
    x=scores,
    y=labels,
    orientation='h',
    marker_color=['red' if s >= 4 else 'orange' if s == 3 else 'green' for s in scores]
))
fig.update_layout(xaxis=dict(range=[0, 5]), title="Force Intensity (1=Low, 5=High)")
st.plotly_chart(fig, use_container_width=True)

for force, details in porters_five_forces.items():
    with st.expander(f"{force.replace('_', ' ').title()} — {details['level']}"):
        st.write(details["reasoning"])

st.markdown("---")

# --- SECTION 4: RECOMMENDATION ---
st.header("✅ Market Entry Recommendation")

avg_score = sum(scores) / len(scores)

if avg_score >= 4:
    verdict = "⚠️ HIGH RISK — Entry not recommended without strong differentiation"
    color = "red"
elif avg_score >= 3:
    verdict = "🟡 MODERATE RISK — Entry viable with a niche, differentiated strategy"
    color = "orange"
else:
    verdict = "✅ LOW RISK — Attractive market for entry"
    color = "green"

st.markdown(f"**Overall Market Attractiveness Score: {avg_score:.1f}/5**")
st.markdown(f"**Verdict: {verdict}**")

st.markdown("""
**Entry Hypothesis:**
A new entrant should target **Tier 2 cities** with **dermatologist-backed, 
affordable serums priced ₹300–₹600**, distributed via **quick commerce first 
(Blinkit/Zepto)** before expanding offline. Focus on an underserved segment — 
**men's skincare** or **sensitive skin** — to avoid direct competition with 
Minimalist and Mamaearth.
""")