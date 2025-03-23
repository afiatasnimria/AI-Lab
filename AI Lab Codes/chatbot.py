import random
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Sample tournament data
tournament_data = {
    "teams": [],
    "matches": [],
    "scores": {},
    "team_stats": {}  # Historical performance data: {"team_name": [features]}
}

# Register a team
def register_team(team_name, stats):
    if team_name in tournament_data["teams"]:
        return f"Team '{team_name}' is already registered."
    tournament_data["teams"].append(team_name)
    tournament_data["team_stats"][team_name] = stats
    return f"Team '{team_name}' has been successfully registered with stats {stats}!"

# Schedule a match
def schedule_match(team1, team2):
    if team1 not in tournament_data["teams"] or team2 not in tournament_data["teams"]:
        return "Both teams must be registered before scheduling a match."
    match = {
        "team1": team1,
        "team2": team2
    }
    tournament_data["matches"].append(match)
    return f"Match scheduled between '{team1}' and '{team2}'."

# Update scores
def update_score(match_id, team1_score, team2_score):
    if match_id < 0 or match_id >= len(tournament_data["matches"]):
        return "Invalid match ID."
    match = tournament_data["matches"][match_id]
    tournament_data["scores"][match_id] = {
        match["team1"]: team1_score,
        match["team2"]: team2_score
    }
    return f"Scores updated for match {match_id}: {match['team1']} ({team1_score}) - {match['team2']} ({team2_score})"

# Predict match outcome using kNN
def predict_match(team1, team2):
    if team1 not in tournament_data["team_stats"] or team2 not in tournament_data["team_stats"]:
        return "Both teams must have historical data for prediction."

    # Create training data
    X = []
    y = []
    for match_id, scores in tournament_data["scores"].items():
        match = tournament_data["matches"][match_id]
        team1_stats = tournament_data["team_stats"][match["team1"]]
        team2_stats = tournament_data["team_stats"][match["team2"]]
        features = team1_stats + team2_stats
        X.append(features)
        winner = match["team1"] if scores[match["team1"]] > scores[match["team2"]] else match["team2"]
        y.append(winner)

    if len(X) < 3:  # Minimum samples required for kNN
        return "Not enough data for prediction. Play more matches to build data."

    # Train kNN model
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)

    # Predict outcome
    team1_stats = tournament_data["team_stats"][team1]
    team2_stats = tournament_data["team_stats"][team2]
    prediction = knn.predict([team1_stats + team2_stats])[0]
    return f"Prediction: The winner will likely be '{prediction}'."

# View matches
def view_matches():
    if not tournament_data["matches"]:
        return "No matches have been scheduled yet."
    response = "Scheduled Matches:\n"
    for idx, match in enumerate(tournament_data["matches"]):
        response += f"{idx}: {match['team1']} vs {match['team2']}\n"
    return response.strip()

def chatbot_response(user_input):
    """
    Processes user commands and responds appropriately.
    """
    if user_input.startswith("register team"):
        try:
            _, team_name, *stats = user_input.split(",")
            stats = list(map(float, stats))
            return register_team(team_name.strip(), stats)
        except ValueError:
            return "Invalid input. Use: register team, team_name, stat1, stat2, ..."
    elif user_input.startswith("schedule match"):
        try:
            _, team1, team2 = user_input.split(",")
            return schedule_match(team1.strip(), team2.strip())
        except ValueError:
            return "Invalid input. Use: schedule match, team1, team2"
    elif user_input.startswith("update score"):
        try:
            _, match_id, team1_score, team2_score = user_input.split(",")
            return update_score(int(match_id.strip()), int(team1_score.strip()), int(team2_score.strip()))
        except ValueError:
            return "Invalid input. Use: update score, match_id, team1_score, team2_score"
    elif user_input.startswith("predict match"):
        try:
            _, team1, team2 = user_input.split(",")
            return predict_match(team1.strip(), team2.strip())
        except ValueError:
            return "Invalid input. Use: predict match, team1, team2"
    elif user_input.startswith("view matches"):
        return view_matches()
    elif user_input.lower() in ["bye", "exit", "quit"]:
        return "Goodbye! Let me know if you need further assistance."
    else:
        return "I'm sorry, I didn't understand that. Try commands like 'register team', 'schedule match', or 'predict match'."

def main():
    print("Tournament Management Chatbot with AI: How can I assist you?")
    print("Commands: \n- register team, team_name, stat1, stat2, ...\n- schedule match, team1, team2")
    print("- update score, match_id, team1_score, team2_score\n- predict match, team1, team2\n- view matches\n- exit")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["bye", "exit", "quit"]:
            print("ChatBot: Goodbye! Have a great day!")
            break
        response = chatbot_response(user_input)
        print(f"ChatBot: {response}")

if __name__ == "__main__":
    main()
