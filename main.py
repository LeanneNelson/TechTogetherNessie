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
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    with login_page.container():
        st.subheader("Welcome to Nessie Bank!")
        with st.form("customer_login"):
            st.session_state.customer_id = st.text_input("**Enter your Customer ID**", "64563cea9683f20dd51879a7", type="password")
            successful = True
            logged_in = st.form_submit_button("Login")

        with st.expander("**Don't have an ID?**"):
            with st.form("registration"):
                user = {"address": {}}
                user_type = "customers"

                left, right = st.columns(2)
                with left:
                    user["first_name"] = st.text_input("**First Name**", placeholder="Johnie")
                    user["last_name"] = st.text_input("**Last Name**", placeholder="Doe")

                    street = st.text_input("**Street**", placeholder="2nd Avenue").split(" ")
                    user["address"]["street_number"] = street[0]
                    user["address"]["street_name"] = " ".join(street[1:len(street)])
                with right:
                    state = st.text_input("**State**", placeholder="Florida")
                    if state:
                        user["address"]["state"] = us_state_to_abbrev[state]
                    user["address"]["city"] = st.text_input("**City**", placeholder="Miami")
                    user["address"]["zip"] = st.text_input("**Zip Code**", placeholder="33132")

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

if st.session_state.logged_in or logged_in or registered:
    customer_info = requests.get(url(["customers", st.session_state.customer_id], {})).json()

    if "code" not in customer_info or (successful and status):
        if not st.session_state.logged_in:
            login_page.empty()
            st.session_state.logged_in = True

            if not status:
                status = "Success!"

            login_page.success(status)
            time.sleep(3)
            login_page.empty()

        dashboard, bills, deposits, loans, purchases, transfers, withdrawals, profile = st.tabs(["Dashboard", "Bills",
                                                                                                 "Deposits", "Loans",
                                                                                                 "Purchases",
                                                                                                 "Transfers",
                                                                                                 "Withdrawals",
                                                                                                 "Profile"])
        with dashboard:
            st.write(requests.get(url(["accounts"], {})).json())
            # account_list = requests.get(url(["customers", st.session_state.customer_id, "accounts"], {})).json()
            # if not account_list:
            #     st.write("You don't have any accounts.")
            #     create_account = st.button("Make an Account")
            #     if create_account:
            #


        with profile:
            name_column, address_column = st.columns(2)
            with name_column:
                if "edit_name" not in st.session_state:
                    st.session_state.edit_name = True
                new_name = st.text_input("**Name**",
                              " ".join([customer_info["first_name"], customer_info["last_name"]]),
                              disabled=st.session_state.edit_name)
                st.session_state.edit_name = not st.button("Edit Name")
                user = {}
                user["first_name"], user["last_name"] = new_name.split(" ")

            with address_column:
                st.text_input("**Address**",
                              ", ".join([" ".join([customer_info["address"]["street_number"],
                                                   customer_info["address"]["street_name"]]),
                                         customer_info["address"]["city"],
                                         " ".join([customer_info["address"]["state"],
                                                   customer_info["address"]["zip"]])]),
                              disabled = True)
                edit_address = st.button("Edit Address")
                if edit_address:
                    user = {"address":{}}
                    street = st.text_input("**Street**", placeholder="2nd Avenue").split(" ")
                    user["address"]["street_number"] = street[0]
                    user["address"]["street_name"] = " ".join(street[1:len(street)])
                    state = st.text_input("**State**", placeholder="Florida")
                    if state:
                        user["address"]["state"] = us_state_to_abbrev[state]
                    user["address"]["city"] = st.text_input("**City**", placeholder="Miami")
                    user["address"]["zip"] = st.text_input("**Zip Code**", placeholder="33132")


    elif not successful:
        st.error(status)
    else:
        st.error(customer_info["message"])

