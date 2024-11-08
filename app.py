import streamlit as st
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Function to check the status of the website
def check_website_status(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
        response_time = response.elapsed.total_seconds()
        return status_code, response_time
    except requests.exceptions.RequestException as e:
        return None, None

# Store status history for plotting
if 'status_history' not in st.session_state:
    st.session_state['status_history'] = pd.DataFrame(columns=['Timestamp', 'Status Code', 'Response Time'])

# Streamlit app configuration
st.set_page_config(page_title="Website Status Checker", page_icon="🌐")

st.title("🌐 Website Status Checker")

# User input for website URL
url = st.text_input("Enter Website URL (e.g., https://example.com):", "https://example.com")

# Option to monitor website status continuously
monitor = st.checkbox("Monitor Website Continuously")

if url:
    if st.button("Check Website Status"):
        # Perform a one-time check
        status_code, response_time = check_website_status(url)

        if status_code is None:
            st.error(f"Error: Website could not be reached.")
        else:
            st.success(f"**{url}** is UP!")
            st.write(f"Status Code: {status_code}")
            st.write(f"Response Time: {response_time} seconds")

        # Log the data to session state for graphing
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_data = pd.DataFrame([[timestamp, status_code, response_time]], columns=['Timestamp', 'Status Code', 'Response Time'])
        
        # Use pd.concat instead of append
        st.session_state['status_history'] = pd.concat([st.session_state['status_history'], new_data], ignore_index=True)

        # Display timestamp of the check
        st.write(f"Last checked: {timestamp}")
        
    # Plot status history
    if not st.session_state['status_history'].empty:
        fig, ax1 = plt.subplots(figsize=(10, 5))

        # Plot response time
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Response Time (s)', color='tab:blue')
        ax1.plot(st.session_state['status_history']['Timestamp'], st.session_state['status_history']['Response Time'], color='tab:blue', label='Response Time')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        # Plot status code on a second y-axis
        ax2 = ax1.twinx()
        ax2.set_ylabel('Status Code', color='tab:red')
        ax2.plot(st.session_state['status_history']['Timestamp'], st.session_state['status_history']['Status Code'], color='tab:red', label='Status Code', linestyle='--')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        # Rotate labels for readability
        plt.xticks(rotation=45)
        fig.tight_layout()
        st.pyplot(fig)

    # Continuous Monitoring
    if monitor:
        st.write("Monitoring website status... (refresh every 10 seconds)")
        while True:
            status_code, response_time = check_website_status(url)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if status_code is None:
                st.write(f"**{url}** is down!")
            else:
                st.write(f"**{url}** is UP! Status Code: {status_code}, Response Time: {response_time} seconds")
            
            # Log the data to session state for graphing
            new_data = pd.DataFrame([[timestamp, status_code, response_time]], columns=['Timestamp', 'Status Code', 'Response Time'])
            st.session_state['status_history'] = pd.concat([st.session_state['status_history'], new_data], ignore_index=True)
            time.sleep(10)

else:
    st.warning("Please enter a valid website URL.")
