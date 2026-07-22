import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="Market Lens Agent", page_icon="📈")
st.title("📈 Market Lens Agent")

# Keep key in secrets or input
api_key = st.secrets.get("GEMINI_API_KEY") or st.text_input("Gemini API Key", type="password")
spot_price = st.text_input("Spot Price (Optional)", placeholder="e.g. 24865.30")

uploaded_files = st.file_uploader("Upload Screenshots", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if st.button("🚀 Analyze", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key!")
    elif not uploaded_files:
        st.warning("Upload at least one image.")
    else:
        with st.spinner("Analyzing..."):
            try:
                client = genai.Client(api_key=api_key)
                images = [Image.open(f) for f in uploaded_files]
                
                prompt = f"""
                You are an intraday trader analyzing Indian index charts.
                {'Spot price: ' + spot_price if spot_price else ''}
                Analyze these charts and option chains:
                1. Multi-timeframe trend & levels.
                2. Option chain read (Max OI, PCR).
                3. Market Bias (Bullish/Bearish/Neutral).
                4. Scalp Trade setups (Strict 15-point target min, 5-point stop-loss max).
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[prompt, *images]
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")