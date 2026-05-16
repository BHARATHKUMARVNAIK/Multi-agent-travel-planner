
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(page_title="Multi-Agent Travel Planner", page_icon="✈️")
st.title("✈️ Multi-Agent Travel Planner")
st.info("⚡ First load may take 30-60 seconds to wake up the server.")

# ── inputs ──────────────────────────────────────────────────
departure    = st.text_input("Flying from", value="New York")
destination  = st.text_input("Destination", value="Paris")
num_days     = st.number_input("Number of days", min_value=1, max_value=30, value=5)
budget       = st.number_input("Max Budget (₹/$)", min_value=1000, max_value=1000000, value=50000, step=1000)
travel_style = st.selectbox("Travel Style", ["Budget Travel", "Mid-range", "Luxury Travel", "Family", "Solo"])
interests    = st.multiselect("Your Interests",
                   ["Food & cuisine", "History & culture", "Nature & outdoors",
                    "Nightlife", "Shopping", "Art & museums", "Adventure & sports"],
                   default=["Food & cuisine", "History & culture"])

# ── session state ───────────────────────────────────────────
if "result"            not in st.session_state: st.session_state.result            = None
if "destination_saved" not in st.session_state: st.session_state.destination_saved = None
if "num_days_saved"    not in st.session_state: st.session_state.num_days_saved    = None

# ── single button ───────────────────────────────────────────
if st.button("✈️ Plan My Trip!"):
    from crew import run_crew
    from map_builder import build_map
    from pdf_export import generate_pdf

    with st.spinner("Your agents are working... this takes 2-3 minutes"):
        result = run_crew(departure, destination, int(num_days), budget, travel_style, interests)

    st.session_state.result            = result.raw
    st.session_state.destination_saved = destination
    st.session_state.num_days_saved    = int(num_days)

# ── display ─────────────────────────────────────────────────
if st.session_state.result:
    from pdf_export import generate_pdf
    from map_builder import build_map

    st.success("Trip planned!")
    st.markdown("### Your Itinerary")
    st.markdown(st.session_state.result)

    pdf_bytes = generate_pdf(
        st.session_state.result,
        st.session_state.destination_saved,
        st.session_state.num_days_saved
    )
    st.download_button(
        label="📄 Download Itinerary as PDF",
        data=pdf_bytes,
        file_name=f"{st.session_state.destination_saved}_{st.session_state.num_days_saved}days_itinerary.pdf",
        mime="application/pdf"
    )

    st.markdown("### 📍 Places on the Map")
    map_result = build_map(st.session_state.result, st.session_state.destination_saved)

    if map_result is None:
        st.warning("Could not generate map for this destination.")
    else:
        travel_map, place_count = map_result
        st.caption(f"Found {place_count} places from your itinerary")
        st_folium(travel_map, width=700, height=500)