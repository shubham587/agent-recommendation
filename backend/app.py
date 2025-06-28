from flask import Flask, request, jsonify
from flask_cors import CORS
from recommendation_engine import RecommendationEngine
import json
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize recommendation engine
try:
    engine = RecommendationEngine()
    logger.info("Recommendation engine initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize recommendation engine: {e}")
    engine = None

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Coding Agent Recommendation System API',
        'version': '1.0.0'
    })

@app.route('/api/agents', methods=['GET'])
def get_all_agents():
    """Get all available agents"""
    try:
        if engine is None:
            return jsonify({'error': 'Recommendation engine not initialized'}), 500
        
        agents = engine.agents
        return jsonify({
            'success': True,
            'agents': agents,
            'total_count': len(agents)
        })
    except Exception as e:
        logger.error(f"Error getting agents: {e}")
        return jsonify({'error': 'Failed to retrieve agents'}), 500

@app.route('/api/agents/<agent_id>', methods=['GET'])
def get_agent_details(agent_id):
    """Get details for a specific agent"""
    try:
        if engine is None:
            return jsonify({'error': 'Recommendation engine not initialized'}), 500
        
        agent = next((a for a in engine.agents if a['id'] == agent_id), None)
        if not agent:
            return jsonify({'error': 'Agent not found'}), 404
        
        return jsonify({
            'success': True,
            'agent': agent
        })
    except Exception as e:
        logger.error(f"Error getting agent details: {e}")
        return jsonify({'error': 'Failed to retrieve agent details'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_task():
    """Analyze a task description without providing recommendations"""
    try:
        if engine is None:
            return jsonify({'error': 'Recommendation engine not initialized'}), 500
        
        data = request.get_json()
        if not data or 'task_description' not in data:
            return jsonify({'error': 'Task description is required'}), 400
        
        task_description = data['task_description'].strip()
        if not task_description:
            return jsonify({'error': 'Task description cannot be empty'}), 400
        
        # Analyze the task
        task_analysis = engine.analyze_task(task_description)
        
        return jsonify({
            'success': True,
            'task_analysis': {
                'task_type': task_analysis.task_type,
                'complexity': task_analysis.complexity,
                'languages': task_analysis.languages,
                'requirements': task_analysis.requirements,
                'context': task_analysis.context,
                'collaboration_needed': task_analysis.collaboration_needed,
                'deployment_needed': task_analysis.deployment_needed,
                'learning_focused': task_analysis.learning_focused
            }
        })
    except Exception as e:
        logger.error(f"Error analyzing task: {e}")
        return jsonify({'error': 'Failed to analyze task'}), 500

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """Get agent recommendations for a task"""
    try:
        if engine is None:
            return jsonify({'error': 'Recommendation engine not initialized'}), 500
        
        data = request.get_json()
        if not data or 'task_description' not in data:
            return jsonify({'error': 'Task description is required'}), 400
        
        task_description = data['task_description'].strip()
        if not task_description:
            return jsonify({'error': 'Task description cannot be empty'}), 400
        
        # Get optional parameters
        top_n = data.get('top_n', 3)
        if not isinstance(top_n, int) or top_n < 1:
            top_n = 3
        
        # Get recommendations
        recommendations = engine.get_recommendations(task_description, top_n)
        
        return jsonify({
            'success': True,
            'task_description': task_description,
            **recommendations
        })
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return jsonify({'error': 'Failed to get recommendations'}), 500

@app.route('/api/compare', methods=['POST'])
def compare_agents():
    """Compare specific agents for a task"""
    try:
        if engine is None:
            return jsonify({'error': 'Recommendation engine not initialized'}), 500
        
        data = request.get_json()
        if not data or 'task_description' not in data or 'agent_ids' not in data:
            return jsonify({'error': 'Task description and agent IDs are required'}), 400
        
        task_description = data['task_description'].strip()
        agent_ids = data['agent_ids']
        
        if not task_description:
            return jsonify({'error': 'Task description cannot be empty'}), 400
        if not isinstance(agent_ids, list) or len(agent_ids) == 0:
            return jsonify({'error': 'At least one agent ID is required'}), 400
        
        # Find the specified agents
        selected_agents = [a for a in engine.agents if a['id'] in agent_ids]
        if len(selected_agents) != len(agent_ids):
            return jsonify({'error': 'One or more agent IDs not found'}), 404
        
        # Analyze the task
        task_analysis = engine.analyze_task(task_description)
        
        # Score the selected agents
        comparisons = []
        for agent in selected_agents:
            total_score, score_breakdown = engine.calculate_agent_score(agent, task_analysis)
            explanation = engine.generate_explanation(agent, task_analysis, score_breakdown)
            
            comparisons.append({
                'agent_id': agent['id'],
                'agent_name': agent['name'],
                'description': agent['description'],
                'score': round(total_score, 3),
                'confidence': round(min(total_score * 100, 95), 1),
                'explanation': explanation,
                'score_breakdown': {k: round(v, 3) for k, v in score_breakdown.items()},
                'strengths': agent['strengths'],
                'capabilities': agent['capabilities']
            })
        
        # Sort by score
        comparisons.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'success': True,
            'task_description': task_description,
            'task_analysis': {
                'task_type': task_analysis.task_type,
                'complexity': task_analysis.complexity,
                'languages': task_analysis.languages,
                'requirements': task_analysis.requirements,
                'context': task_analysis.context
            },
            'comparisons': comparisons
        })
    except Exception as e:
        logger.error(f"Error comparing agents: {e}")
        return jsonify({'error': 'Failed to compare agents'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Coding Agent Recommendation System API")
    print("📋 Available endpoints:")
    print("   GET  /                    - Health check")
    print("   GET  /api/agents          - Get all agents")
    print("   GET  /api/agents/<id>     - Get agent details")
    print("   POST /api/analyze         - Analyze task")
    print("   POST /api/recommend       - Get recommendations")
    print("   POST /api/compare         - Compare specific agents")
    print("\n🌐 API will be available at: http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 