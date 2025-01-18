# Install required libraries if not already installed
!pip install faker
!pip install PyPDF2
!pip install nltk
!pip install scikit-learn

import pandas as pd
from faker import Faker
import re
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


# Utility functions
def generate_10_digit_phone():
    """Generates a random 10-digit phone number."""
    fake = Faker()
    while True:
        phone = fake.phone_number()
        cleaned_phone = re.sub(r'\D', '', phone)
        if len(cleaned_phone) == 10:
            return cleaned_phone


def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file."""
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text


def clean_text(text):
    """Cleans text by removing non-alphanumeric characters and stop words."""
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)


def load_user_data(csv_file):
    """Loads user data from a CSV file and adds fake data for Phone, Email, and Address."""
    try:
        df = pd.read_csv(csv_file)
        if not df.empty:
            fake = Faker()
            df['Phone'] = [generate_10_digit_phone() for _ in range(len(df))]
            df['Email'] = [fake.email() for _ in range(len(df))]
            df['Address'] = [fake.address() for _ in range(len(df))]
        return df
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
        return pd.DataFrame()


def find_target_audience(user_data, policy_text, user_text_column):
    """Finds the target audience based on cosine similarity."""
    # Vectorize user data and policy text
    vectorizer = TfidfVectorizer()
    user_vectors = vectorizer.fit_transform(user_data[user_text_column].fillna(''))
    policy_vector = vectorizer.transform([policy_text])

    # Calculate cosine similarities
    similarities = cosine_similarity(user_vectors, policy_vector).flatten()
    user_data['Relevance'] = similarities

    # Sort users by relevance
    sorted_users = user_data.sort_values(by='Relevance', ascending=False)
    return sorted_users


def save_results(target_audience, output_file):
    """Saves the target audience to a CSV file."""
    target_audience.to_csv(output_file, index=False)
    print(f"Target audience saved to {output_file}")


# Loan and Policy Functions
def process_home_loan(user_data, policy_pdf, output_file):
    """Filters users and identifies target audience for home loans."""
    # Filter users who do not have a housing loan
    filtered_users = user_data[user_data['housing'] == 'no']

    # Process policy text
    policy_text = extract_text_from_pdf(policy_pdf)
    policy_text = clean_text(policy_text)

    # Find target audience
    target_audience = find_target_audience(filtered_users, policy_text, 'housing')

    # Save results
    save_results(target_audience, output_file)


def process_car_loan(user_data, policy_pdf, output_file):
    """Filters users and identifies target audience for car loans."""
    # Filter users who do not have a car (based on custom logic)
    filtered_users = user_data[user_data['Has_4_Wheeler'] == False]

    # Process policy text
    policy_text = extract_text_from_pdf(policy_pdf)
    policy_text = clean_text(policy_text)

    # Find target audience
    target_audience = find_target_audience(filtered_users, policy_text, 'Has_4_Wheeler')

    # Save results
    save_results(target_audience, output_file)


def process_personal_loan(user_data, policy_pdf, output_file):
    """Filters users and identifies target audience for personal loans."""
    # Filter users with balance less than a threshold (e.g., 50000)
    filtered_users = user_data[user_data['balance'] < 50000]

    # Process policy text
    policy_text = extract_text_from_pdf(policy_pdf)
    policy_text = clean_text(policy_text)

    # Find target audience
    target_audience = find_target_audience(filtered_users, policy_text, 'balance')

    # Save results
    save_results(target_audience, output_file)


def process_health_insurance(user_data, policy_pdf, output_file):
    """Filters users and identifies target audience for health insurance."""
    # Filter users based on age (e.g., age > 40)
    filtered_users = user_data[user_data['age'] > 40]

    # Process policy text
    policy_text = extract_text_from_pdf(policy_pdf)
    policy_text = clean_text(policy_text)

    # Find target audience
    target_audience = find_target_audience(filtered_users, policy_text, 'age')

    # Save results
    save_results(target_audience, output_file)


# Main Function
def main():
    # File paths
    user_data_csv = '/content/train.csv'
    home_loan_pdf = '/content/home-loan-policy.pdf'
    car_loan_pdf = '/content/car-loan-policy.pdf'
    personal_loan_pdf = '/content/personal-loan-policy.pdf'
    health_insurance_pdf = '/content/health-insurance-policy.pdf'

    try:
        # Load user data
        user_data = load_user_data(user_data_csv)
        print("User data loaded successfully!")

        # Process each policy
        process_home_loan(user_data, home_loan_pdf, '/content/target_home_loan.csv')
        process_car_loan(user_data, car_loan_pdf, '/content/target_car_loan.csv')
        process_personal_loan(user_data, personal_loan_pdf, '/content/target_personal_loan.csv')
        process_health_insurance(user_data, health_insurance_pdf, '/content/target_health_insurance.csv')

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
