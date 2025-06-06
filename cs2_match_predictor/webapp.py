from flask import Flask, request, render_template_string
from .elo import build_ratings, predict
from .data import load_matches


TEMPLATE = """
<!doctype html>
<title>CS2 Match Predictor</title>
<h1>CS2 Match Predictor</h1>
<form method="post">
  <label>Team 1:
    <select name="team1">
      {% for t in teams %}
      <option value="{{t}}" {% if t==team1 %}selected{% endif %}>{{t}}</option>
      {% endfor %}
    </select>
  </label>
  <label>Team 2:
    <select name="team2">
      {% for t in teams %}
      <option value="{{t}}" {% if t==team2 %}selected{% endif %}>{{t}}</option>
      {% endfor %}
    </select>
  </label>
  <input type="submit" value="Predict">
</form>
{% if prob is not none %}
<p>Probability that {{team1}} beats {{team2}}: {{'{:.2%}'.format(prob)}}</p>
{% endif %}
"""


def create_app(csv_path: str) -> Flask:
    matches = load_matches(csv_path)
    ratings = build_ratings(matches)
    teams = sorted({m.team1 for m in matches} | {m.team2 for m in matches})

    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        team1 = request.form.get('team1', teams[0])
        team2 = request.form.get('team2', teams[1] if len(teams) > 1 else teams[0])
        prob = None
        if request.method == 'POST':
            prob = predict(ratings, team1, team2)
        return render_template_string(TEMPLATE, teams=teams, team1=team1, team2=team2, prob=prob)

    return app


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run the CS2 Match Predictor web front end')
    parser.add_argument(
        'dataset',
        nargs='?',
        default='data/csgoresults.csv',
        help='CSV dataset file'
    )
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind')
    args = parser.parse_args()

    app = create_app(args.dataset)
    app.run(debug=True, host=args.host, port=args.port)
