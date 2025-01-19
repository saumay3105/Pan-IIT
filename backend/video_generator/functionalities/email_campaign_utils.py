import pandas as pd
import sys

# --- Utility Functions ---
def filter_home_loan_users(df):
    """Filters users for home loans."""
    users = df[df['housing'] == 'no']  # Users without a home loan
    return prioritize_with_clickstream(users, "home_loan")


def filter_car_loan_users(df):
    """Filters users for car loans."""
    users = df[df['Has_4_Wheeler'] == False]  # Users without a 4-wheeler
    return prioritize_with_clickstream(users, "car_loan")


def filter_personal_loan_users(df):
    """Filters users for personal loans."""
    users = df[df['balance'] < 50000]  # Users with a balance < 50,000
    return prioritize_with_clickstream(users, "personal_loan")


def filter_health_insurance_users(df):
    """Filters users for health insurance."""
    users = df[df['age'] > 40]  # Users aged above 40
    return prioritize_with_clickstream(users, "health_insurance")


def filter_life_insurance_users(df):
    """Filters users for life insurance."""
    users = df[df['marital'] == 'married']  # Married users
    return prioritize_with_clickstream(users, "life_insurance")


def prioritize_with_clickstream(users, loan_type):
    """
    Prioritize users based on clickstream data by identifying users who spent
    significant time on loan-related websites.
    """
    loan_keywords = {
        "home_loan": ["home-loans", "mortgage"],
        "car_loan": ["auto-loans", "car-loans"],
        "personal_loan": ["personal-loans"],
        "health_insurance": ["health-insurance"],
        "life_insurance": ["life-insurance"],
    }

    # Filter for relevant clickstream data
    relevant_clicks = users[users['Highest_Time_Spent_Website'].str.contains("|".join(loan_keywords[loan_type]), case=False, na=False)]

    # Prioritize based on 'Highest_Time_Spent'
    relevant_clicks = relevant_clicks.sort_values(by='Highest_Time_Spent', ascending=False)
    return relevant_clicks


# --- Main Processing Function ---
def process_target_audience(loan_type, user_df, output_file):
    """Filters the dataset based on loan type and clickstream data and generates the output file."""
    loan_type = loan_type.lower()

    if loan_type == "home_loan":
        filtered_data = filter_home_loan_users(user_df)
    elif loan_type == "car_loan":
        filtered_data = filter_car_loan_users(user_df)
    elif loan_type == "personal_loan":
        filtered_data = filter_personal_loan_users(user_df)
    elif loan_type == "health_insurance":
        filtered_data = filter_health_insurance_users(user_df)
    elif loan_type == "life_insurance":
        filtered_data = filter_life_insurance_users(user_df)
    else:
        print(f"Error: Unsupported loan type '{loan_type}'.")
        sys.exit(1)

    # Save filtered data to CSV
    filtered_data.to_csv(output_file, index=False)
    print(f"Target audience file generated: {output_file}")