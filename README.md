# Attendance Agent CLI

A command-line tool that analyzes your class attendance from a CSV file, flags subjects where attendance has fallen below a threshold, and uses the Gemini API to automatically draft a formal, ready-to-send message to the relevant professor for each flagged subject.

## Features

- Parses attendance data from a CSV file
- Calculates attendance percentage per subject
- Flags subjects below a configurable threshold
- Matches each flagged subject to a professor via a mapping file
- Drafts a polite, formal message per professor using Google's Gemini API
- Handles missing/invalid data gracefully (e.g. subjects with no classes held, or no professor mapped)

## Installation

1. Clone this repository and navigate into the project folder:

git clone <your-repo-url>
cd attendance-agent-cli


2. Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # macOS/Linux


3. Install dependencies:

pip install -r requirements.txt


## Setup

1. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com).

2. Create a `.env` file in the project root:

GEMINI_API_KEY=your_key_here


3. Prepare your `attendance.csv` with the following columns:

   | Subject | Classes_Attended | Classes_Held |
   |---------|-------------------|--------------|
   | PS      | 16                | 18           |
   | DBMS    | 26                | 28           |

4. Prepare your `professors.csv` with the following columns:

   | Subject | Professor_Name | Professor_Email        |
   |---------|-----------------|-------------------------|
   | PS      | Dr. Sharma      | sharma@university.edu  |
   | DBMS    | Dr. Patel       | patel@university.edu   |

## Usage

Run with default settings (`attendance.csv`, 75% threshold):

python cli.py


Specify a custom CSV file and/or threshold:

python cli.py --csv attendance.csv --threshold 80


View all available options:

python cli.py --help


## How It Works

1. Loads and cleans the attendance CSV
2. Calculates attendance percentage per subject
3. Filters subjects below the given threshold
4. Merges flagged subjects with their professor's contact info
5. Sends a prompt per flagged subject to Gemini, using a system instruction to keep tone formal and consistent
6. Prints (or saves) a ready-to-send draft message for each flagged subject

## Notes

- Subjects with `0` classes held are skipped with a warning, since attendance percentage can't be calculated for them.
- Subjects with no matching professor in `professors.csv` are skipped with a warning.
- Drafts include placeholders (e.g. `[Your Name]`) where personal info should be filled in before sending.

## Tech Stack

- Python
- pandas
- google-genai (Gemini API)
- argparse