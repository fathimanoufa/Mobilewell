import streamlit as st
import pandas as pd
import requests
API_URL = "https://mobilewell.onrender.com"

st.set_page_config(page_title="MobileWell | Digital Wellness", page_icon="🌿",
                   layout="wide", initial_sidebar_state="collapsed")

# Load the already-trained model and preprocessing objects



# Aesthetic theme
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 8% 8%, #183d38 0, transparent 32%),
        radial-gradient(circle at 95% 35%, #302b3d 0, transparent 30%),
        linear-gradient(
            135deg,
            #101b1b 0%,
            #172827 55%,
            #1d2529 100%
        );
    color: #edf5f1;
}
#MainMenu, footer {visibility:hidden;}
[data-testid="stHeader"] {background:transparent;}
.block-container {max-width:1120px;padding-top:2rem;padding-bottom:2rem;}
.hero {
  background:linear-gradient(120deg,#173e3b,#236c60 58%,#3c8a76);
  padding:42px 44px;border-radius:28px;color:white;margin:5px 0 30px;
  box-shadow:0 18px 45px rgba(28,83,72,.16);
}
.hero h1 {color:white!important;font-size:43px;font-weight:800;margin:0 0 8px;}
.hero p {color:#e1f1e9!important;font-size:16px;line-height:1.8;margin:0;}
.eyebrow {color:#b9e4d2;text-transform:uppercase;letter-spacing:2px;
  font-size:11px;font-weight:800;margin-bottom:10px;}
.section-title {color:#1c5148;font-size:27px;font-weight:800;margin:20px 0 5px;}
.section-subtitle {color:#71877e;font-size:14px;line-height:1.7;margin-bottom:22px;}
[data-testid="stForm"] {
  background:rgba(255,255,255,.86);border:1px solid #dcebe2;
  border-radius:24px;padding:26px 28px 22px;
  box-shadow:0 12px 35px rgba(35,78,65,.07);
}
h3 {color:#24564c!important;font-weight:750!important;}
label,[data-testid="stWidgetLabel"] p {color:#355b51!important;font-weight:650!important;}
div[data-baseweb="input"] input,div[data-baseweb="select"]>div {
  background:white!important;border:1px solid #d8e8df!important;border-radius:12px!important;
}
[data-testid="stFormSubmitButton"] button {
  width:100%;min-height:3.1rem;border:0;border-radius:14px;color:white;
  font-size:16px;font-weight:750;background:linear-gradient(110deg,#246c5e,#48a184);
  box-shadow:0 8px 18px rgba(48,128,103,.2);transition:.2s;
}
[data-testid="stFormSubmitButton"] button:hover {
  color:white;border:0;transform:translateY(-2px);
  background:linear-gradient(110deg,#1c594e,#358b70);
}
hr {border-color:#e2eee7!important;margin:22px 0!important;}
.result-card {padding:34px 30px;border-radius:24px;text-align:center;
  margin-top:16px;box-shadow:0 12px 30px rgba(44,73,61,.07);}
.positive-card {background:linear-gradient(135deg,#fff4ed,#fbe4d8);border:1px solid #f0cbb8;}
.negative-card {background:linear-gradient(135deg,#eaf8f0,#d9efe3);border:1px solid #bfdfcb;}
.result-emoji {font-size:45px;margin-bottom:8px;}
.result-heading {font-size:28px;line-height:1.3;font-weight:850;margin:5px 0 8px;}
.positive-heading {color:#99573d;} .negative-heading {color:#286b55;}
.result-tag {display:inline-block;padding:6px 13px;border-radius:30px;
  font-size:12px;font-weight:800;letter-spacing:1px;margin:7px 0 14px;}
.positive-tag {color:#945037;background:#f7d8c8;}
.negative-tag {color:#286b55;background:#c8e8d5;}
.result-message {color:#526c62;font-size:15px;line-height:1.85;max-width:760px;margin:0 auto;}
.tip-box {background:rgba(255,255,255,.95);padding:23px 26px;border-radius:20px;
  border:1px solid #e0ece5;border-left:5px solid #55a184;margin-top:18px;
  box-shadow:0 8px 24px rgba(44,73,61,.05);}
.tip-box h4 {color:#286b5a;font-size:18px;margin:0 0 13px;}
.tip-item {color:#526c62;font-size:14px;line-height:1.8;padding:5px 0;}
.disclaimer {color:#82948b;font-size:12px;line-height:1.6;text-align:center;margin-top:18px;}
.footer {text-align:center;color:#82958d;font-size:12px;line-height:1.8;padding:38px 0 10px;}
@media(max-width:700px) {
 .block-container{padding-left:1rem;padding-right:1rem;}
 .hero{padding:30px 24px;border-radius:22px;}
 .hero h1{font-size:34px;}.result-heading{font-size:23px;}
 [data-testid="stForm"]{padding:20px 16px;}
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">A LITTLE MORE BALANCE, EVERY DAY</div>
  <h1>🌿 MobileWell</h1>
  <p>Your digital wellness journey starts here.<br>
  Understand your mobile habits and build a healthier relationship
  with technology — one small step at a time.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Discover Your Digital Wellness</div>',
            unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Share a few details about your daily '
            'routine to receive a machine-learning based wellness prediction '
            'and practical suggestions.</div>', unsafe_allow_html=True)

# Input form
with st.form("mobile_wellness_form"):
    st.markdown("### 👤 Personal Information")
    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Age", min_value=2, max_value=45, value=22, step=1)
    with c2:
        gender = st.selectbox("Gender", ["Female", "Male", "Other"])

    st.markdown("---")
    st.markdown("### 📱 Mobile Usage")
    c1, c2 = st.columns(2)
    with c1:
        daily_screen_time_hours = st.number_input(
            "Daily Screen Time (hours)", 0.0, 24.0, 5.0, step=0.5)
        social_media_hours = st.number_input(
            "Social Media Usage (hours)", 0.0, 24.0, 2.0, step=0.5)
        gaming_hours = st.number_input(
            "Gaming Time (hours)", 0.0, 24.0, 1.0, step=0.5)
        app_opens_per_day = st.number_input(
            "App Opens Per Day", 0, 1000, 80, step=1)
    with c2:
        weekend_screen_time = st.number_input(
            "Weekend Screen Time (hours)", 0.0, 24.0, 6.0, step=0.5)
        notifications_per_day = st.number_input(
            "Notifications Per Day", 0, 2000, 80, step=1)
        work_study_hours = st.number_input(
            "Work / Study Usage (hours)", 0.0, 24.0, 3.0, step=0.5)
        sleep_hours = st.number_input(
            "Sleep Hours", 0.0, 24.0, 7.0, step=0.5)

    st.markdown("---")
    st.markdown("### 🧠 Lifestyle & Well-being")
    c1, c2 = st.columns(2)
    with c1:
        stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])
    with c2:
        academic_work_impact = st.selectbox(
            "Does mobile usage affect your work or studies?", ["Yes", "No"])
    submitted = st.form_submit_button("🌱  Check My Digital Wellness")

# Prediction
if submitted:

    input_data = {
        "age": age,
        "daily_screen_time_hours": daily_screen_time_hours,
        "social_media_hours": social_media_hours,
        "gaming_hours": gaming_hours,
        "work_study_hours": work_study_hours,
        "sleep_hours": sleep_hours,
        "notifications_per_day": notifications_per_day,
        "app_opens_per_day": app_opens_per_day,
        "weekend_screen_time": weekend_screen_time,
        "gender": gender,
        "stress_level": stress_level,
        "academic_work_impact": academic_work_impact
    }

    try:
        # Send user data to FastAPI
        response = requests.post(
            f"{API_URL}/predict",
            json=input_data
        )

        response.raise_for_status()

        # Receive prediction
        result = response.json()
        prediction = result["prediction"]

        st.markdown("---")
        st.markdown(
            '<div class="section-title">Your Wellness Result</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-subtitle">Here is what the model '
            'predicted from the details you entered.</div>',
            unsafe_allow_html=True
        )

        # Positive prediction
        if prediction == 1:
            st.markdown("""
            <div class="result-card positive-card">
              <div class="result-emoji">🌱</div>
              <div class="result-heading positive-heading">
                A Little Awareness Goes a Long Way!
              </div>
              <div class="result-tag positive-tag">POSITIVE PREDICTION</div>
              <p class="result-message">
                Your answers match patterns that the model associates with
                mobile addiction. This is not a reason to feel bad. Becoming
                aware of your habits is a positive first step. Small,
                realistic changes can help you build a healthier relationship
                with your phone. You can do this! 💚
              </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="tip-box">
              <h4>💡 Your Digital Wellness Action Plan</h4>
              <div class="tip-item">🌿 <b>Set screen-time limits:</b>
                Start by reducing recreational phone use by 15–30 minutes a day.</div>
              <div class="tip-item">🔕 <b>Quiet the notifications:</b>
                Turn off unimportant alerts and keep your phone away while studying or working.</div>
              <div class="tip-item">⏳ <b>Take screen breaks:</b>
                Follow a regular break routine and rest your eyes during long sessions.</div>
              <div class="tip-item">🌙 <b>Protect your sleep:</b>
                Try keeping your phone away for the last 30–60 minutes before bedtime.</div>
              <div class="tip-item">🌳 <b>Make room for offline life:</b>
                Add a walk, exercise, reading, hobbies, or face-to-face time to your day.</div>
              <div class="tip-item">📊 <b>Track your progress:</b>
                Review your screen-time report weekly and celebrate small improvements.</div>
            </div>
            """, unsafe_allow_html=True)

        # Negative prediction
        elif prediction == 0:
            st.markdown("""
            <div class="result-card negative-card">
              <div class="result-emoji">🌟</div>
              <div class="result-heading negative-heading">
                Keep Up the Great Balance!
              </div>
              <div class="result-tag negative-tag">NEGATIVE PREDICTION</div>
              <p class="result-message">
                Your answers do not match the patterns that this model
                associates with mobile addiction. Keep making mindful choices
                and enjoying the world beyond your screen. Remember, balance
                matters more than perfection. 💚
              </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="tip-box">
              <h4>✨ Keep Your Healthy Habits</h4>
              <div class="tip-item">🌿 <b>Maintain your balance:</b>
                Keep recreational screen time within limits that work for you.</div>
              <div class="tip-item">📵 <b>Stay intentional:</b>
                Open apps with a purpose instead of scrolling automatically.</div>
              <div class="tip-item">🌙 <b>Keep sleep a priority:</b>
                Maintain a regular sleep schedule and screen-free time before bed.</div>
              <div class="tip-item">🏃 <b>Stay active:</b>
                Make time for movement, hobbies, friends, and family.</div>
              <div class="tip-item">🔔 <b>Review notifications:</b>
                Keep only useful alerts switched on.</div>
              <div class="tip-item">💚 <b>Check in with yourself:</b>
                If phone habits begin affecting daily life, adjust your routine early.</div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.warning(f"Unexpected prediction value: {prediction}")

        # Disclaimer
        st.markdown("""
        <div class="disclaimer">
          <b>Friendly reminder:</b> This is an educational machine-learning
          project for digital-wellness awareness. It is not a medical test
          or diagnosis. A prediction cannot determine whether someone has
          a clinical addiction.
        </div>
        """, unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to FastAPI. Please start your backend.")

    except requests.exceptions.RequestException as error:
        st.error(f"Prediction request failed: {error}")
      

# Prediction History
st.markdown("---")
st.subheader("📊 Prediction History")

if st.button("View Prediction History"):
    try:
        response = requests.get(f"{API_URL}/history")
        response.raise_for_status()

        history = response.json()

        if history:
            history_df = pd.DataFrame(history)
            st.dataframe(history_df, use_container_width=True)
        else:
            st.info("No prediction history available yet.")

    except requests.exceptions.RequestException as error:
        st.error(f"Unable to load history: {error}")
      
       

# Footer
st.markdown("""
<div class="footer">
  Made with 💚 for a healthier digital lifestyle.<br>
  <b>MobileWell | Digital Wellness Project</b>
</div>
""", unsafe_allow_html=True)
 