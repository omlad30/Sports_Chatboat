import requests
from datetime import datetime
import time

def get_live_scores():
    # Fetch real-time soccer matches for today using TheSportsDB free tier
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today}&s=Soccer"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if not data.get("events"):
            return []
            
        matches = []
        for event in data["events"]:
            # Optionally filter for World Cup or Top leagues to keep the UI clean
            league = event.get("strLeague", "")
            
            # Format the score
            home_score = event.get("intHomeScore")
            away_score = event.get("intAwayScore")
            if home_score is not None and away_score is not None:
                score = f"{home_score} - {away_score}"
            else:
                score = "vs"
                
            status = event.get("strStatus", "Upcoming")
            if status == "NS": status = "Not Started"
            elif status == "FT": status = "Finished"
            
            matches.append({
                "league": league,
                "home": event.get("strHomeTeam", "Home"),
                "away": event.get("strAwayTeam", "Away"),
                "score": score,
                "status": status
            })
            
        # Sort so FIFA World Cup matches appear at the very top!
        matches.sort(key=lambda x: 0 if "World Cup" in x["league"] else 1)
        
        return matches

    except Exception as e:
        print(f"API Error: {e}")
        # Fallback to mock data if the API fails
        return [
            {"league": "FIFA World Cup", "home": "Canada", "away": "Qatar", "score": "vs", "status": "Not Started"}
        ]

def get_team_stats(team_name):
    # Mock data for analytics page - since TheSportsDB doesn't have an easy "team season stats" free endpoint
    return {
        "wins": 15,
        "draws": 4,
        "losses": 2,
        "goals_for": 45,
        "goals_against": 12
    }
