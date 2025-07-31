import streamlit as st
import os

st.set_page_config(page_title="QuickSlot", layout="centered")

st.image("assets/logo.png", width=100)
st.title("⚡ QuickSlot")

st.markdown("""
Welcome to QuickSlot — the booking link for hustlers, creatives, and mobile pros.

Use the sidebar to:
- Create your own QuickSlot
- Share your booking link
- Manage bookings (admin only)
""")

# Helpful dev message
st.info("ℹ️ This is the main entry — all pages are in the sidebar on the left.")
