import streamlit as st
from datetime import datetime
from backend.bookings import save_booking
from backend.emailer import send_confirmation

st.set_page_config(page_title="Book a Gig • QuickSlot", layout="centered")

st.image("assets/logo.png", width=100)
st.title("🎤 Book a Gig or Session")

with st.form("gig_booking_form"):
    gig_type = st.selectbox("What are you booking?", [
        "DJ Set", "Photography Session", "Tattoo Appointment",
        "Makeup Artist", "Private Chef", "Trainer Session", "Other"
    ])
    event_title = st.text_input("Event or Session Name")
    date = st.date_input("Event Date", min_value=datetime.today())
    time = st.time_input("Start Time")
    location = st.text_input("Event Location")
    deposit_required = st.checkbox("Require deposit to confirm?", value=True)
    deposit_amount = st.number_input("Deposit amount ($)", min_value=0, value=50)
    total_price = st.number_input("Total cost ($)", min_value=0, value=200)
    notes = st.text_area("Details or special requests")
    name = st.text_input("Your name")
    email = st.text_input("Email")
    payment = st.selectbox("Payment Method", [
        "CashApp", "Venmo", "PayPal", "Zelle", "Apple Pay (iMessage)", "Cash in person"
    ])

    preview = st.form_submit_button("Preview Booking")

if preview:
    st.subheader("📋 Confirm Your Booking Details")
    st.markdown(f"**Name:** {name}")
    st.markdown(f"**Email:** {email}")
    st.markdown(f"**Event:** {gig_type} – {event_title}")
    st.markdown(f"**Date & Time:** {date} at {time}")
    st.markdown(f"**Location:** {location}")
    st.markdown(f"**Payment Method:** {payment}")
    st.markdown(f"**Deposit Required:** {'Yes' if deposit_required else 'No'}")
    if deposit_required:
        st.markdown(f"**Deposit Amount:** ${deposit_amount}")
    st.markdown(f"**Total Price:** ${total_price}")
    if notes:
        st.markdown(f"**Notes:** {notes}")

    confirm = st.button("✅ Confirm & Submit Booking")

    if confirm:
        booking = {
            "service": gig_type + " – " + event_title,
            "datetime": f"{date} {time}",
            "location": location,
            "name": name,
            "email": email,
            "phone": "",
            "payment": payment,
            "deposit_required": deposit_required,
            "deposit_amount": deposit_amount,
            "status": "Pending" if deposit_required else "Confirmed",
            "created_at": datetime.now().isoformat()
        }
        save_booking(booking)
        send_confirmation(
            to_email=email,
            name=name,
            service=gig_type,
            datetime_str=f"{date} {time}",
            payment=payment
        )
        st.success("✅ Booking confirmed! Check your email for next steps.")
        if deposit_required:
            st.warning(f"This gig is pending until the ${deposit_amount} deposit is received.")
