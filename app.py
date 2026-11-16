import streamlit as st

st.set_page_config(page_title="CreditGuard AI", page_icon="🛡️", layout="wide",
                   initial_sidebar_state="expanded")

from core import get_detector, init_state, version_mismatches  # noqa: E402
from ui import MUTED, inject_css, logo  # noqa: E402

inject_css()
init_state()
detector = get_detector()

pages = [
    st.Page("views/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True),
    st.Page("views/single.py", title="Single Transaction", icon=":material/credit_card:", url_path="single"),
    st.Page("views/batch.py", title="Batch Prediction", icon=":material/upload_file:", url_path="batch"),
    st.Page("views/model_info.py", title="Model Information", icon=":material/insights:", url_path="model"),
]
nav = st.navigation(pages)

with st.sidebar:
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:12px;margin:.2rem 0 1rem">{logo(40)}'
        f'<div><div style="font-weight:800;font-size:1.15rem">CreditGuard AI</div>'
        f'<div style="color:{MUTED};font-size:.78rem">Credit Card Fraud Detection</div></div></div>',
        unsafe_allow_html=True,
    )
    st.caption(f"Model: **{detector.report['model_name']}**  \nThreshold: **{detector.threshold:.3f}**")
    for msg in version_mismatches(detector.report):
        st.warning(f"Library version mismatch — {msg}. Pin the training versions in requirements.txt.")

nav.run()
