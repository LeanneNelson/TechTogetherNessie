import streamlit as st
import requests
import json
import time
st.set_page_config(layout="wide")

api_key = "325e2ddfa69504f8dec4ba8927253a02"
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

@st.cache_data
def url(category_list, parameters):
    url_str = "http://api.nessieisreal.com"

    for category in category_list:
        url_str += f"/{category}"

    url_str += f"?key={api_key}"
    for key, value in parameters.items():
        url_str += f"&{key}={value}"

    return url_str


status = ""
login_page = st.empty()
with login_page.container():
    st.subheader("Welcome to Nessie Bank!")
    with st.form("customer_login"):
        customer_id = st.text_input("**Enter your Customer ID**", type="password")
        successful = True
        logged_in = st.form_submit_button("Login")

    with st.expander("**Don't have an ID?**"):
        with st.form("registration"):
            user = {"address": {}}
            user_type = "customers"

            left, right = st.columns(2)
            with left:
                user["first_name"] = st.text_input("**First Name**", "Johnie")
                user["last_name"] = st.text_input("**Last Name**", "Doe")

                street = st.text_input("**Street**", "2nd Avenue").split(" ")
                user["address"]["street_number"] = street[0]
                user["address"]["street_name"] = " ".join(street[1:len(street)])
            with right:
                user["address"]["state"] = us_state_to_abbrev[st.text_input("**State**", "Florida")]
                user["address"]["city"] = st.text_input("**City**", "Miami")
                user["address"]["zip"] = st.text_input("**Zip Code**", "33132")

            registered = st.form_submit_button("Create Account")

        if registered:
            response = requests.post(url([user_type], {}),
                                     data=json.dumps(user),
                                     headers={'content-type': 'application/json'}).json()
            if response["code"] == 201:
                status = response["message"]
                successful = True
            else:
                status = response

if logged_in or registered:
    customer_info = requests.get(url(["customers", customer_id], {})).json()

    if "code" not in customer_info or (successful and status):
        login_page.empty()

        if not status:
            status = "Success!"

        login_page.success(status)
        time.sleep(3)
        login_page.empty()

        dashboard, bills, deposits, loans, purchases, transfers, withdrawals,profile = st.tabs(["Dashboard", "Bills",
                                                                                                "Deposits", "Loans",
                                                                                                "Purchases", "Transfers",
                                                                                                "Withdrawals", "Profile"])
        with
    elif not successful:
        st.error(status)
    else:
        st.error(customer_info["message"])

