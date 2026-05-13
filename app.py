from flask import Flask, request, jsonify

app = Flask(__name__)

def parse_odd(value):
    try:
        return float(str(value).replace(",", "."))
    except:
        return 0

def analyse_match(home, away, odd1, oddX, odd2):
    o1 = parse_odd(odd1)
    ox = parse_odd(oddX)
    o2 = parse_odd(odd2)

    favorite = "Win1" if o1 < o2 else "Win2"
    fav_odd = min(o1, o2)
    outsider_odd = max(o1, o2)
    gap = abs(o1 - o2)

    result = "Match Piège"
    score = "1-1"
    total = 2
    market = "Under 3.5"
    confidence = 60
    risk = "Moyen"
    reason = "Cotes tsy mazava loatra, mila mitandrina."

    if fav_odd <= 1.25 and outsider_odd >= 7:
        result = favorite
        score = "3-0" if favorite == "Win1" else "0-3"
        total = 3
        market = "Win favori + Over 1.5"
        confidence = 88
        risk = "Safe"
        reason = "Favori matanjaka be amin’ny cote ambany."

    elif fav_odd <= 1.55 and outsider_odd >= 4:
        result = favorite
        score = "2-0" if favorite == "Win1" else "0-2"
        total = 2
        market = "Win favori"
        confidence = 80
        risk = "Moyen"
        reason = "Favori mazava, mety handresy."

    elif ox <= 2.80 and gap <= 1:
        result = "Draw"
        score = "1-1"
        total = 2
        market = "Under 3.5"
        confidence = 70
        risk = "Moyen"
        reason = "Cote X ambany, mety hivoaka nul."

    elif fav_odd >= 2 and fav_odd <= 2.8:
        result = "BTTS"
        score = "2-2"
        total = 4
        market = "BTTS / Over 2.5"
        confidence = 68
        risk = "Moyen"
        reason = "Cotes équilibrées, mety samy mahafaty."

    return {
        "match": f"{home} vs {away}",
        "resultat": result,
        "score": score,
        "total": total,
        "over": market,
        "confiance": confidence,
        "risk": risk,
        "reason": reason
    }

@app.route("/")
def home():
    return "Predict IA Football Server Works!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    matches = data.get("matches", [])
    results = []

    for m in matches:
        results.append(
            analyse_match(
                m.get("home"),
                m.get("away"),
                m.get("odd1"),
                m.get("oddX"),
                m.get("odd2")
            )
        )

    return jsonify({
        "status": "success",
        "predictions": results
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
