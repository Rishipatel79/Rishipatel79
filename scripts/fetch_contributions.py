import json
import os
from pathlib import Path
from dotenv import load_dotenv
import requests

# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")

if not GITHUB_TOKEN:
    raise ValueError("[ERROR] GITHUB_TOKEN not found in .env")

if not USERNAME:
    raise ValueError("[ERROR] GITHUB_USERNAME not found in .env")

# ==========================================
# Output File
# ==========================================

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "contributions.json"

# ==========================================
# GitHub GraphQL Endpoint
# ==========================================

GRAPHQL_URL = "https://api.github.com/graphql"

# ==========================================
# GraphQL Query
# ==========================================

QUERY = """
query($login:String!){
  user(login:$login){
    contributionsCollection{
      contributionCalendar{
        totalContributions

        weeks{
          contributionDays{
            contributionCount
            contributionLevel
            date
            weekday
          }
        }
      }
    }
  }
}
"""

# ==========================================
# Fetch Contributions
# ==========================================

def fetch_contributions():

    print(f"Fetching contributions for {USERNAME}...")

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/json"
    }

    payload = {
        "query": QUERY,
        "variables": {
            "login": USERNAME
        }
    }

    response = requests.post(
        GRAPHQL_URL,
        json=payload,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if "errors" in data:
        raise Exception(data["errors"])

    return data

# ==========================================
# Process Contributions
# ==========================================

def process_contributions(data):
    """Extract and calculate statistics from the contributions data."""
    try:
        # Navigate to the contribution calendar
        calendar = data['data']['user']['contributionsCollection']['contributionCalendar']
        total_contributions = calendar['totalContributions']
        weeks = calendar['weeks']

        # Flatten all days into a list in chronological order (oldest to newest)
        all_days = []
        for week in weeks:
            for day in week['contributionDays']:
                all_days.append({
                    'date': day['date'],
                    'count': day['contributionCount'],
                    'level': day['contributionLevel'],
                    'weekday': day['weekday']
                })

        # Calculate longest streak
        longest_streak = 0
        current_streak = 0
        streak = 0

        # Iterate through days in chronological order to find longest streak
        for day in all_days:
            if day['count'] > 0:
                streak += 1
                if streak > longest_streak:
                    longest_streak = streak
            else:
                streak = 0

        # Calculate current streak (from most recent day backwards)
        # Reverse the list to start from newest
        for day in reversed(all_days):
            if day['count'] > 0:
                current_streak += 1
            else:
                break

        # Verify total contributions by summing daily counts
        calculated_total = sum(day['count'] for day in all_days)

        stats = {
            'total_contributions': total_contributions,
            'calculated_total': calculated_total,
            'longest_streak': longest_streak,
            'current_streak': current_streak,
            'total_days_tracked': len(all_days),
            'days_with_contributions': len([d for d in all_days if d['count'] > 0])
        }

        return stats

    except KeyError as e:
        print(f"Error processing data: Missing key {e}")
        return None

# ==========================================
# Main Function
# ==========================================

def main():
    """Main function to fetch, process, and save contributions data."""
    try:
        # Fetch data from GitHub
        data = fetch_contributions()

        # Process the data to get statistics
        stats = process_contributions(data)

        if stats is None:
            print("[ERROR] Failed to process contributions data")
            return

        # Save the raw data to JSON file
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"[SUCCESS] Data saved to {OUTPUT_FILE}")

        # Print statistics summary
        print("\n[STATS] Contributions Summary:")
        print(f"   Total Contributions (from API): {stats['total_contributions']}")
        print(f"   Total Contributions (calculated): {stats['calculated_total']}")
        print(f"   Longest Streak: {stats['longest_streak']} days")
        print(f"   Current Streak: {stats['current_streak']} days")
        print(f"   Days Tracked: {stats['total_days_tracked']}")
        print(f"   Days with Contributions: {stats['days_with_contributions']}")

        # Verify consistency
        if stats['total_contributions'] != stats['calculated_total']:
            print(f"[WARNING] Warning: API total ({stats['total_contributions']}) != calculated total ({stats['calculated_total']})")
        else:
            print("[SUCCESS] Totals match!")

    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")

# ==========================================
# Script Entry Point
# ==========================================

if __name__ == "__main__":
    main()