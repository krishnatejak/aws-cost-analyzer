from flask import Flask, jsonify
from cost_analyzer import AWSCostAnalyzer
from recommendation_engine import RecommendationEngine

app = Flask(__name__)

@app.route('/api/cost-data')
def get_cost_data():
    analyzer = AWSCostAnalyzer()
    data = analyzer.get_cost_and_usage()
    return jsonify(data)

@app.route('/api/recommendations')
def get_recommendations():
    engine = RecommendationEngine()
    recommendations = engine.generate_recommendations()
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
