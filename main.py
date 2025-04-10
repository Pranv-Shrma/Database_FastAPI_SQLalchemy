import streamlit as st
import requests
import json

# FastAPI backend URL
BACKEND_URL = "http://localhost:8000"  # Replace with your actual FastAPI URL

def create_user():
    st.subheader("Create New User")
    name = st.text_input("Name:")
    email = st.text_input("Email:")
    if st.button("Create User"):
        if name and email:
            user_data = {"name": name, "email": email}
            try:
                response = requests.post(f"{BACKEND_URL}/users/create_user", json=user_data)
                response.raise_for_status()  # Raise an exception for bad status codes
                st.success(f"User created successfully! User details: {response.json()}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error creating user: {e}")
            except requests.exceptions.HTTPError as e:
                st.error(f"Error creating user: {response.json()}")
        else:
            st.warning("Please enter both name and email.")

def read_users():
    st.subheader("Read Users")
    skip = st.number_input("Skip:", min_value=0, value=0, step=1)
    limit = st.number_input("Limit:", min_value=1, value=10, step=1)
    if st.button("Read Users"):
        try:
            response = requests.get(f"{BACKEND_URL}/users/read_users?skip={skip}&limit={limit}")
            response.raise_for_status()
            users = response.json()
            if users:
                st.write("### List of Users:")
                for user in users:
                    st.write(f"**ID:** {user['id']}")
                    st.write(f"**Name:** {user['name']}")
                    st.write(f"**Email:** {user['email']}")
                    st.markdown("---")
            else:
                st.info("No users found.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error reading users: {e}")
        except requests.exceptions.HTTPError as e:
            st.error(f"Error reading users: {response.json()}")

def read_user():
    st.subheader("Read User by ID")
    user_id = st.number_input("User ID:", min_value=1, value=1, step=1)
    if st.button("Read User"):
        try:
            response = requests.get(f"{BACKEND_URL}/users/read_user/{user_id}")
            if response.status_code == 200:
                user = response.json()
                st.write("### User Details:")
                st.write(f"**ID:** {user['id']}")
                st.write(f"**Name:** {user['name']}")
                st.write(f"**Email:** {user['email']}")
            elif response.status_code == 404:
                st.warning("User not found.")
            else:
                st.error(f"Error reading user: {response.json()}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error reading user: {e}")

def update_user():
    st.subheader("Update User by ID")
    user_id = st.number_input("User ID to Update:", min_value=1, value=1, step=1)
    name = st.text_input("New Name (optional):")
    email = st.text_input("New Email (optional):")
    if st.button("Update User"):
        if name or email:
            update_data = {}
            if name:
                update_data["name"] = name
            if email:
                update_data["email"] = email
            try:
                response = requests.put(f"{BACKEND_URL}/users/update_user/{user_id}", json=update_data)
                if response.status_code == 200:
                    st.success(f"User updated successfully! Updated details: {response.json()}")
                elif response.status_code == 404:
                    st.warning("User not found.")
                else:
                    st.error(f"Error updating user: {response.json()}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error updating user: {e}")
        else:
            st.info("Please provide at least one field to update (name or email).")

def delete_user():
    st.subheader("Delete User by ID")
    user_id = st.number_input("User ID to Delete:", min_value=1, value=1, step=1)
    if st.button("Delete User"):
        try:
            response = requests.delete(f"{BACKEND_URL}/users/delete_user/{user_id}")
            if response.status_code == 200:
                st.success(response.json()["message"])
            elif response.status_code == 404:
                st.warning("User not found.")
            else:
                st.error(f"Error deleting user: {response.json()}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error deleting user: {e}")

def main():
    st.title("FastAPI User Management")

    menu = ["Create User", "Read Users", "Read User by ID", "Update User", "Delete User"]
    choice = st.sidebar.selectbox("Select Operation", menu)

    if choice == "Create User":
        create_user()
    elif choice == "Read Users":
        read_users()
    elif choice == "Read User by ID":
        read_user()
    elif choice == "Update User":
        update_user()
    elif choice == "Delete User":
        delete_user()

if __name__ == "__main__":
    main()