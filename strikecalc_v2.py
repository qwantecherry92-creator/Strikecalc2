import streamlit as st
from math import log, ceil

st.title("🎯 StrikeCalc v2 — JMEM-Inspired Weaponeering & CDE")

st.markdown("""
Select the target type, desired effect, and munition to calculate rounds required and CDE level.
""")

# JMEM-inspired munition data (example)
munitions = {
    "155mm HE (M795)": {"pk": 0.22, "hazard": 85},
    "105mm HE (M1)": {"pk": 0.12, "hazard": 60},
    "120mm Mortar HE": {"pk": 0.15, "hazard": 70},
    "500lb JDAM (GBU-38)": {"pk": 0.50, "hazard": 150},
    "2000lb JDAM (GBU-31)": {"pk": 0.90, "hazard": 350},
    "60mm Mortar HE": {"pk": 0.08, "hazard": 35},
}

# Target types & desired effects
target_types = ["Personnel", "Light Vehicle", "Armored Vehicle", "Masonry Building", "Bunker", "Bridge"]
desired_effects = ["Suppress", "Neutralize", "Destroy"]

# User Inputs
target_name = st.text_input("Target Name", "Target X")
target_type = st.selectbox("Target Type", target_types)
desired_effect = st.selectbox("Desired Effect", desired_effects)
munition_choice = st.selectbox("Select Munition", list(munitions.keys()))
civilian_dist = st.number_input("Nearest Civilian Structure Distance (m)", min_value=0, value=50)

# Fetch JMEM data
pk = munitions[munition_choice]["pk"]
hazard_dist = munitions[munition_choice]["hazard"]

st.write(f"**Selected Munition Pₖ:** {pk}")
st.write(f"**Hazard Distance:** {hazard_dist} m")

if st.button("Calculate"):
    # Adjust desired confidence based on desired effect
    desired_conf_map = {"Suppress": 0.5, "Neutralize": 0.75, "Destroy": 0.9}
    desired_conf = desired_conf_map[desired_effect]

    failure_per_round = 1 - pk
    rounds_needed = ceil(log(1 - desired_conf) / log(failure_per_round))

    # CDE calculation
    if civilian_dist >= hazard_dist:
        cde = 1
    elif civilian_dist >= hazard_dist / 2:
        cde = 2
    else:
        cde = 3

    st.subheader(f"Results for {target_name}")
    st.write(f"📊 **Rounds Required:** {rounds_needed}")
    st.write(f"💥 **CDE Level:** {cde}")

    if cde <= 2:
        st.success("CDE Level within BCT approval authority.")
    else:
        st.warning("CDE Level may require higher HQ approval.")
