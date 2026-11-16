"""Shared look & feel: colours, CSS, logo, small HTML helpers and Plotly styling."""
import streamlit as st

TEAL, RED, AMBER, GREEN = "#00D1B2", "#FF5C7A", "#FFB020", "#2ED47A"
NAVY, CARD, BORDER, MUTED, TEXT = "#0B1220", "#111A2E", "#1E2A44", "#8FA0BD", "#E6EDF7"
RISK_COLORS = {"Low": GREEN, "Medium": AMBER, "High": RED}
PRED_COLORS = {"Normal": TEAL, "Fraud": RED}

LOGO_SVG = f"""
<svg width="{{s}}" height="{{s}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#00D1B2"/><stop offset="1" stop-color="#2F80ED"/></linearGradient></defs>
  <path d="M32 4 56 13v17c0 15-10 26-24 30C18 56 8 45 8 30V13z" fill="url(#g)"/>
  <rect x="17" y="24" width="30" height="20" rx="3" fill="#0B1220" opacity=".92"/>
  <rect x="17" y="29" width="30" height="4" fill="#00D1B2"/>
  <rect x="21" y="38" width="9" height="2.6" rx="1.3" fill="#8FA0BD"/>
</svg>"""

CSS = f"""
<style>
#MainMenu, footer {{visibility: hidden;}}
.block-container {{padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1250px;}}
h1, h2, h3 {{letter-spacing: -0.01em;}}
[data-testid="stSidebar"] {{border-right: 1px solid {BORDER};}}

.cg-hero {{display:flex; align-items:center; gap:22px; padding:26px 30px; border-radius:18px;
  background: radial-gradient(1200px 300px at 0% 0%, rgba(0,209,178,.16), transparent 60%),
              linear-gradient(135deg, #111A2E 0%, #0E1628 100%);
  border:1px solid {BORDER}; margin-bottom: 1.2rem;}}
.cg-hero h1 {{margin:0; font-size:2.1rem;}}
.cg-hero p {{margin:.35rem 0 0; color:{MUTED}; font-size:1.02rem; max-width: 780px; line-height:1.55;}}
.cg-tag {{display:inline-block; padding:2px 10px; border-radius:999px; font-size:.72rem; font-weight:600;
  color:{TEAL}; border:1px solid rgba(0,209,178,.45); background:rgba(0,209,178,.08); margin-bottom:.5rem;}}

.cg-kpi {{background:{CARD}; border:1px solid {BORDER}; border-radius:14px; padding:18px 20px; height:100%;}}
.cg-kpi .label {{color:{MUTED}; font-size:.78rem; text-transform:uppercase; letter-spacing:.06em;}}
.cg-kpi .value {{font-size:2rem; font-weight:700; margin-top:.15rem; line-height:1.15;}}
.cg-kpi .sub {{color:{MUTED}; font-size:.82rem; margin-top:.2rem;}}

.cg-card {{background:{CARD}; border:1px solid {BORDER}; border-radius:14px; padding:18px 22px; height:100%;}}
.cg-card h4 {{margin:0 0 .35rem; font-size:1.02rem;}}
.cg-card p, .cg-card li {{color:{MUTED}; font-size:.92rem; line-height:1.55;}}

.cg-result {{border-radius:16px; padding:22px 26px; border:1px solid; display:flex; align-items:center; gap:18px;}}
.cg-result .big {{font-size:2.2rem; font-weight:800; line-height:1;}}
.cg-result .small {{color:{MUTED}; font-size:.9rem; margin-top:.3rem;}}
.cg-pill {{display:inline-block; padding:3px 12px; border-radius:999px; font-weight:700; font-size:.8rem; border:1px solid;}}
.cg-section {{font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; color:{MUTED}; margin:1.4rem 0 .5rem;}}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def logo(size: int = 56) -> str:
    return LOGO_SVG.replace("{s}", str(size))


def hero(title: str, text: str, tag: str = "FRAUD DETECTION") -> None:
    st.markdown(
        f'<div class="cg-hero">{logo(78)}<div><span class="cg-tag">{tag}</span>'
        f"<h1>{title}</h1><p>{text}</p></div></div>",
        unsafe_allow_html=True,
    )


def kpi(label: str, value: str, sub: str = "", color: str = TEXT) -> str:
    return (f'<div class="cg-kpi"><div class="label">{label}</div>'
            f'<div class="value" style="color:{color}">{value}</div>'
            f'<div class="sub">{sub}</div></div>')


def card(title: str, body: str) -> str:
    return f'<div class="cg-card"><h4>{title}</h4>{body}</div>'


def section(text: str) -> None:
    st.markdown(f'<div class="cg-section">{text}</div>', unsafe_allow_html=True)


def style_fig(fig, height: int = 340):
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT), margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    return fig
