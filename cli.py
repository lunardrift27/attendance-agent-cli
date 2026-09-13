import pandas as pd
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import argparse

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description='Attendance analyzer and email drafter')
parser.add_argument('--csv', default='attendance.csv', help='Path to attendance CSV')
parser.add_argument('--threshold', type=float, default=75, help='Attendance %% threshold')
args = parser.parse_args()

try:
    df = pd.read_csv(args.csv)
    df.columns = df.columns.str.strip()
except FileNotFoundError:
    print(f"Error: The file {args.csv} was not found.")
    exit(1)

if 'Subject' not in df.columns or 'Classes_Attended' not in df.columns or 'Classes_Held' not in df.columns:
    print("Error: The CSV file must contain 'Subject', 'Classes_Attended', and 'Classes_Held' columns.")
    exit(1)

df['Attendance %'] = (df['Classes_Attended'] / df['Classes_Held']) * 100
print(df)

invalid_df=df[df['Classes_Held'] == 0]
valid_df=df[df['Classes_Held'] != 0]

low_attendance = valid_df[valid_df['Attendance %'] < args.threshold]
print("Subjects with low attendance:")
print(low_attendance)

if not invalid_df.empty:
    print("\nWarning: these subjects have no recorded classes and were skipped:")
    print(invalid_df)

try:
    prof_df = pd.read_csv('professors.csv')
    prof_df.columns = prof_df.columns.str.strip()
except FileNotFoundError:
    print("Error: The file 'professors.csv' was not found.")
    exit(1)

if 'Subject' not in prof_df.columns or 'Professor_Name' not in prof_df.columns or 'Professor_Email' not in prof_df.columns:
    print("Error: The professors CSV file must contain 'Subject', 'Professor_Name', and 'Professor_Email' columns.")
    exit(1)

print("\nProfessor Data:")
print(prof_df)

merged_df = pd.merge(low_attendance, prof_df, on='Subject', how='left')
print("\nMerged Data:")
print(merged_df)

missing_professors = merged_df[merged_df['Professor_Email'].isna()]
merged_df = merged_df.dropna(subset=['Professor_Email'])

print("\nSubjects with low attendance and their professors:")
print(merged_df)

if not missing_professors.empty:
    print("\nWarning: these subjects have no professor mapped and were skipped:")
    print(missing_professors[['Subject']])

for _, row in merged_df.iterrows():
    prompt = f"Subject: {row['Subject']}, Attendance: {row['Attendance %']:.1f}%, Professor: {row['Professor_Name']}"

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="You are a student writing to your professor about low attendance. The email should be polite, concise, and respectful. It should request guidance on how to improve attendance and suggest possible solutions such as completing assignments or attending extra sessions.",
            temperature=0.3
        )
    )

    print(f"\n--- Draft for {row['Subject']} ---")
    print(response.text)