import streamlit as st
from datetime import datetime
from backend.bookings import save_booking
from backend.emailer import send_confirmation

st.set_page_config(page_title="Book with QuickSlot", layout="centered")

st.image("assets/logo.png", width=100)
st.title("📅 Book an Appointment")

with st.form("booking_form"):
    service = st.selectbox("Choose a service", ["Car Wash", "Haircut", "Braiding", "Handyman", "Tutoring"])
    date = st.date_input("Pick a date", min_value=datetime.today())
    time = st.time_input("Pick a time")
    location = st.text_input("Location (address or area)")
    name = st.text_input("Your name")
    email = st.text_input("Email")
    phone = st.text_input("Phone (optional)")
    
    payment = st.selectbox("How will you pay?", [
        "CashApp", 
        "Venmo", 
        "PayPal", 
        "Zelle", 
        "Apple Pay (iMessage or tap)", 
        "Cash in person",
        "Other (custom link)"
    ])
    
    custom_link = None
    if payment == "Other (custom link)":
        custom_link = st.text_input("Enter your custom payment or contact link")

    require_deposit = st.checkbox("Require deposit to confirm booking?")
    deposit_amount = 0
    if require_deposit:
        deposit_amount = st.number_input("Deposit amount ($)", min_value=0, value=25)

    submitted = st.form_submit_button("Book Now")
    if submitted:
        if not all([name, email, location]):
            st.error("Please fill in all required fields.")
        else:
            booking = {
                "service": service,
                "datetime": f"{date} {time}",
                "location": location,
                "name": name,
                "email": email,
                "phone": phone,
                "payment": payment,
                "deposit_required": require_deposit,
                "deposit_amount": deposit_amount if require_deposit else 0,
                "status": "Pending" if require_deposit else "Confirmed",
                "created_at": datetime.now().isoformat()
            }
            save_booking(booking)
            send_confirmation(
                to_email=email,
                name=name,
                service=service,
                datetime_str=f"{date} {time}",
                payment=payment
            )
            st.success("✅ Booking submitted! You’ll receive a confirmation soon.")

            if require_deposit:
                st.warning(f"This booking is **pending** until the ${deposit_amount} deposit is received.")
                if payment != "Cash in person":
                    st.subheader("💳 Deposit Instructions")
                    if payment == "CashApp":
                        st.markdown(f"Send **${deposit_amount}** to **$YourCashAppHandle**")
                    elif payment == "Venmo":
                        st.markdown(f"Pay **${deposit_amount}** to **@YourVenmoHandle**")
                    elif payment == "PayPal":
                        st.markdown(f"[Pay ${deposit_amount} via PayPal](https://paypal.me/YourLink/{deposit_amount})")
                    elif payment == "Zelle":
                        st.markdown(f"Zelle **${deposit_amount}** to your-email@example.com")
                    elif payment == "Apple Pay (iMessage or tap)":
                        st.markdown("Send via iMessage to **+1 (555) 123-4567**")
                    elif payment == "Other (custom link)" and custom_link:
                        st.markdown(f"[Click here to pay]({custom_link})")
            else:
                st.info("If paying online, check your email for the payment link.")
