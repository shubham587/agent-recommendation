import json
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class TaskAnalysis:
    task_type: str
    complexity: str
    languages: List[str]
    requirements: List[str]
    context: str
    collaboration_needed: bool
    deployment_needed: bool
    learning_focused: bool

class RecommendationEngine:
    def __init__(self, agents_db_path: str = "agents_db.json"):
        with open(agents_db_path, 'r') as f:
            self.agents_data = json.load(f)
        self.agents = self.agents_data['agents']
        
        # Task type keywords mapping
        self.task_keywords = {
            'web_development': ['web', 'website', 'frontend', 'backend', 'react', 'vue', 'angular', 'html', 'css', 'javascript', 'node', 'django', 'flask'],
            'mobile_development': ['mobile', 'android', 'ios', 'app', 'react native', 'flutter', 'swift', 'kotlin'],
            'data_science': ['data', 'machine learning', 'ml', 'ai', 'pandas', 'numpy', 'analysis', 'visualization', 'jupyter'],
            'cloud_development': ['aws', 'azure', 'gcp', 'cloud', 'serverless', 'docker', 'kubernetes'],
            'game_development': ['game', 'unity', 'unreal', 'pygame', 'godot'],
            'api_development': ['api', 'rest', 'graphql', 'microservices', 'fastapi'],
            'automation': ['automation', 'script', 'selenium', 'testing', 'ci/cd'],
            'learning': ['learn', 'tutorial', 'beginner', 'practice', 'study', 'education']
        }
        
        # Complexity indicators
        self.complexity_indicators = {
            'beginner': ['simple', 'basic', 'easy', 'beginner', 'start', 'learn', 'first time'],
            'intermediate': ['medium', 'intermediate', 'some experience', 'moderate'],
            'advanced': ['complex', 'advanced', 'enterprise', 'large scale', 'production', 'sophisticated']
        }
        
        # Programming language keywords
        self.language_keywords = {
            'Python': ['python', 'py', 'django', 'flask', 'pandas', 'numpy'],
            'JavaScript': ['javascript', 'js', 'node', 'react', 'vue', 'angular'],
            'TypeScript': ['typescript', 'ts'],
            'Java': ['java', 'spring', 'android'],
            'C++': ['c++', 'cpp'],
            'C#': ['c#', 'csharp', '.net'],
            'Go': ['go', 'golang'],
            'Rust': ['rust'],
            'PHP': ['php', 'laravel'],
            'Ruby': ['ruby', 'rails'],
            'Swift': ['swift', 'ios'],
            'Kotlin': ['kotlin', 'android']
        }
    
    def analyze_task(self, task_description: str) -> TaskAnalysis:
        """Analyze the task description to extract key information"""
        task_lower = task_description.lower()
        
        # Determine task type
        task_type = 'general_programming'
        max_matches = 0
        for task_cat, keywords in self.task_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in task_lower)
            if matches > max_matches:
                max_matches = matches
                task_type = task_cat
        
        # Determine complexity
        complexity = 'intermediate'  # default
        for comp_level, indicators in self.complexity_indicators.items():
            if any(indicator in task_lower for indicator in indicators):
                complexity = comp_level
                break
        
        # Identify programming languages
        languages = []
        for lang, keywords in self.language_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                languages.append(lang)
        
        # Check for specific requirements
        requirements = []
        if any(word in task_lower for word in ['collaborate', 'team', 'share', 'together']):
            requirements.append('collaboration')
        if any(word in task_lower for word in ['deploy', 'production', 'host', 'publish']):
            requirements.append('deployment')
        if any(word in task_lower for word in ['secure', 'security', 'enterprise', 'compliance']):
            requirements.append('security')
        if any(word in task_lower for word in ['free', 'budget', 'cost', 'cheap']):
            requirements.append('budget_conscious')
        if any(word in task_lower for word in ['fast', 'quick', 'rapid', 'prototype']):
            requirements.append('rapid_development')
        
        # Determine context
        context = 'professional'
        if any(word in task_lower for word in ['learn', 'study', 'practice', 'beginner']):
            context = 'learning'
        elif any(word in task_lower for word in ['enterprise', 'company', 'business']):
            context = 'enterprise'
        elif any(word in task_lower for word in ['personal', 'hobby', 'side project']):
            context = 'personal'
        
        return TaskAnalysis(
            task_type=task_type,
            complexity=complexity,
            languages=languages,
            requirements=requirements,
            context=context,
            collaboration_needed='collaboration' in requirements,
            deployment_needed='deployment' in requirements,
            learning_focused=context == 'learning'
        )
    
    def calculate_agent_score(self, agent: Dict, task_analysis: TaskAnalysis) -> Tuple[float, Dict[str, float]]:
        """Calculate a score for how well an agent matches the task"""
        scores = {
            'language_support': 0.0,
            'task_alignment': 0.0,
            'complexity_match': 0.0,
            'feature_match': 0.0,
            'context_fit': 0.0
        }
        
        # Language support scoring (25% weight)
        if task_analysis.languages:
            supported_langs = set(lang.lower() for lang in agent['supported_languages'])
            required_langs = set(lang.lower() for lang in task_analysis.languages)
            language_overlap = len(supported_langs.intersection(required_langs))
            scores['language_support'] = min(language_overlap / len(required_langs), 1.0) * 0.25
        else:
            scores['language_support'] = 0.15  # Default bonus for good language support
        
        # Task type alignment (25% weight)
        task_score = 0.0
        if task_analysis.task_type == 'web_development':
            if 'React' in agent['supported_languages'] or 'HTML' in agent['supported_languages']:
                task_score = 0.8
        elif task_analysis.task_type == 'cloud_development':
            if agent['id'] == 'aws_codewhisperer':
                task_score = 1.0
            elif agent['deployment']:
                task_score = 0.6
        elif task_analysis.task_type == 'learning':
            if 'educational' in [uc.lower() for uc in agent['use_cases']] or agent['learning_curve'] == 'low':
                task_score = 0.8
        elif task_analysis.task_type == 'data_science':
            if 'Python' in agent['supported_languages']:
                task_score = 0.7
        else:
            task_score = 0.5  # Default for general programming
        
        scores['task_alignment'] = task_score * 0.25
        
        # Complexity match (20% weight)
        complexity_match = 0.5  # default
        if task_analysis.complexity == 'beginner':
            if agent['learning_curve'] == 'low' or 'beginners' in agent['ideal_for']:
                complexity_match = 1.0
        elif task_analysis.complexity == 'advanced':
            if 'enterprise' in agent['ideal_for'] or 'experienced_developers' in agent['ideal_for']:
                complexity_match = 1.0
        
        scores['complexity_match'] = complexity_match * 0.20
        
        # Feature requirements match (20% weight)
        feature_score = 0.0
        total_requirements = len(task_analysis.requirements) or 1
        
        for req in task_analysis.requirements:
            if req == 'collaboration' and agent['collaboration']:
                feature_score += 1.0
            elif req == 'deployment' and agent['deployment']:
                feature_score += 1.0
            elif req == 'budget_conscious' and agent['price_tier'] == 'free':
                feature_score += 1.0
            elif req == 'security' and 'security' in agent['strengths'][0].lower():
                feature_score += 1.0
            elif req == 'rapid_development' and ('prototyping' in agent['ideal_for'] or 'zero setup' in agent['strengths'][0].lower()):
                feature_score += 1.0
        
        scores['feature_match'] = min(feature_score / total_requirements, 1.0) * 0.20
        
        # Context fit (10% weight)
        context_score = 0.5  # default
        if task_analysis.learning_focused and 'students' in agent['ideal_for']:
            context_score = 1.0
        elif task_analysis.context == 'enterprise' and 'enterprise' in agent['ideal_for']:
            context_score = 1.0
        elif task_analysis.context == 'personal' and agent['price_tier'] in ['free', 'freemium']:
            context_score = 0.8
        
        scores['context_fit'] = context_score * 0.10
        
        total_score = sum(scores.values())
        return total_score, scores
    
    def generate_explanation(self, agent: Dict, task_analysis: TaskAnalysis, scores: Dict[str, float]) -> str:
        """Generate explanation for why this agent was recommended"""
        explanations = []
        
        # Language support
        if task_analysis.languages:
            supported = [lang for lang in task_analysis.languages if lang in agent['supported_languages']]
            if supported:
                explanations.append(f"Excellent support for {', '.join(supported)}")
        
        # Key strengths
        top_strengths = agent['strengths'][:2]
        explanations.append(f"Key strengths: {', '.join(top_strengths)}")
        
        # Special features
        if 'collaboration' in task_analysis.requirements and agent['collaboration']:
            explanations.append("Supports real-time collaboration")
        if 'deployment' in task_analysis.requirements and agent['deployment']:
            explanations.append("Includes deployment capabilities")
        if agent['price_tier'] == 'free':
            explanations.append("Completely free to use")
        
        # Context-specific reasons
        if task_analysis.learning_focused and 'students' in agent['ideal_for']:
            explanations.append("Great for learning and educational use")
        if task_analysis.complexity == 'advanced' and 'enterprise' in agent['ideal_for']:
            explanations.append("Suitable for complex enterprise projects")
        
        return ". ".join(explanations) + "."
    
    def get_recommendations(self, task_description: str, top_n: int = 3) -> Dict:
        """Get top N agent recommendations for a given task"""
        # Analyze the task
        task_analysis = self.analyze_task(task_description)
        
        # Score all agents
        agent_scores = []
        for agent in self.agents:
            total_score, score_breakdown = self.calculate_agent_score(agent, task_analysis)
            explanation = self.generate_explanation(agent, task_analysis, score_breakdown)
            
            agent_scores.append({
                'agent': agent,
                'score': total_score,
                'score_breakdown': score_breakdown,
                'explanation': explanation,
                'confidence': min(total_score * 100, 95)  # Convert to percentage, cap at 95%
            })
        
        # Sort by score and get top N
        agent_scores.sort(key=lambda x: x['score'], reverse=True)
        top_recommendations = agent_scores[:top_n]
        
        return {
            'task_analysis': {
                'task_type': task_analysis.task_type,
                'complexity': task_analysis.complexity,
                'languages': task_analysis.languages,
                'requirements': task_analysis.requirements,
                'context': task_analysis.context
            },
            'recommendations': [
                {
                    'rank': i + 1,
                    'agent_id': rec['agent']['id'],
                    'agent_name': rec['agent']['name'],
                    'description': rec['agent']['description'],
                    'score': round(rec['score'], 3),
                    'confidence': round(rec['confidence'], 1),
                    'explanation': rec['explanation'],
                    'strengths': rec['agent']['strengths'],
                    'capabilities': rec['agent']['capabilities'],
                    'supported_languages': rec['agent']['supported_languages'],
                    'price_tier': rec['agent']['price_tier'],
                    'learning_curve': rec['agent']['learning_curve'],
                    'score_breakdown': {k: round(v, 3) for k, v in rec['score_breakdown'].items()}
                }
                for i, rec in enumerate(top_recommendations)
            ]
        } 