import streamlit as st
from datetime import datetime
from backend.users import save_user

st.set_page_config(page_title="Create Your QuickSlot", layout="centered")

st.title("🛠️ Set Up Your Booking Link")

with st.form("user_setup_form"):
    handle = st.text_input("Your booking link handle (e.g. djskeme)", max_chars=30)
    name = st.text_input("Your name or business name")
    email = st.text_input("Contact email")
    
    services = st.text_area("List your services (one per line)")
    payment_options = st.multiselect("Accepted payment methods", [
        "CashApp", "Venmo", "PayPal", "Zelle", "Apple Pay", "Cash in person"
    ])
    
    deposit_required = st.checkbox("Require deposit to confirm?", value=True)
    deposit_amount = st.number_input("Deposit amount ($)", min_value=0, value=50)
    
    submitted = st.form_submit_button("Create My QuickSlot")

    if submitted:
        if not all([handle, name, email, services, payment_options]):
            st.error("Please fill in all required fields.")
        else:
            profile = {
                "handle": handle.lower(),
                "name": name,
                "email": email,
                "services": [s.strip() for s in services.splitlines() if s.strip()],
                "payment_methods": payment_options,
                "deposit_required": deposit_required,
                "deposit_amount": deposit_amount,
                "created_at": datetime.now().isoformat()
            }
            save_user(profile)
            st.success(f"✅ Your booking page is ready at: `/pages/{handle}.py` (coming next)")
