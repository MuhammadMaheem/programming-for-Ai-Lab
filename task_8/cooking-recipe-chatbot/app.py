"""
Cooking/Recipe Finder Application
Uses the TheMealDB API to search for recipes and display cooking information
Free API - No authentication required
"""

from flask import Flask, render_template, request, jsonify
import requests
import logging
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TheMealDB API endpoints
MEAL_SEARCH_API = "https://www.themealdb.com/api/json/v1/1/search.php"
MEAL_CATEGORIES_API = "https://www.themealdb.com/api/json/v1/1/categories.php"
MEAL_INGREDIENTS_API = "https://www.themealdb.com/api/json/v1/1/list.php"
MEAL_BY_ID_API = "https://www.themealdb.com/api/json/v1/1/lookup.php"
MEAL_RANDOM_API = "https://www.themealdb.com/api/json/v1/1/random.php"

def search_recipes(query):
    """
    Search for recipes by name using TheMealDB API
    
    Args:
        query (str): Recipe/meal name to search
    
    Returns:
        dict: Search results with recipes and metadata
    """
    try:
        params = {'s': query}
        response = requests.get(MEAL_SEARCH_API, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        processed_meals = []
        if data['meals']:
            for meal in data['meals']:
                processed_meal = {
                    'id': meal['idMeal'],
                    'name': meal['strMeal'],
                    'image': meal['strMealThumb'],
                    'category': meal['strCategory'],
                    'cuisine': meal['strArea'],
                    'tags': meal['strTags'].split(',') if meal.get('strTags') else [],
                    'instructions': meal['strInstructions'],
                    'youtube': meal.get('strYoutube', ''),
                    'ingredients': []
                }
                
                # Extract ingredients and measurements
                for i in range(1, 21):
                    ingredient_key = f'strIngredient{i}'
                    measure_key = f'strMeasure{i}'
                    
                    ingredient = meal.get(ingredient_key, '').strip()
                    measure = meal.get(measure_key, '').strip()
                    
                    if ingredient:
                        processed_meal['ingredients'].append({
                            'ingredient': ingredient,
                            'measure': measure
                        })
                
                processed_meals.append(processed_meal)
        
        return {
            'success': True,
            'results': processed_meals,
            'count': len(processed_meals),
            'query': query,
            'timestamp': datetime.now().isoformat()
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {str(e)}")
        return {
            'success': False,
            'results': [],
            'error': f"Failed to fetch recipes: {str(e)}",
            'timestamp': datetime.now().isoformat()
        }

def get_random_recipe():
    """
    Get a random recipe from TheMealDB API
    
    Returns:
        dict: Random recipe details
    """
    try:
        response = requests.get(MEAL_RANDOM_API, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['meals']:
            meal = data['meals'][0]
            processed_meal = {
                'id': meal['idMeal'],
                'name': meal['strMeal'],
                'image': meal['strMealThumb'],
                'category': meal['strCategory'],
                'cuisine': meal['strArea'],
                'tags': meal['strTags'].split(',') if meal.get('strTags') else [],
                'instructions': meal['strInstructions'],
                'youtube': meal.get('strYoutube', ''),
                'ingredients': []
            }
            
            # Extract ingredients and measurements
            for i in range(1, 21):
                ingredient_key = f'strIngredient{i}'
                measure_key = f'strMeasure{i}'
                
                ingredient = meal.get(ingredient_key, '').strip()
                measure = meal.get(measure_key, '').strip()
                
                if ingredient:
                    processed_meal['ingredients'].append({
                        'ingredient': ingredient,
                        'measure': measure
                    })
            
            return {
                'success': True,
                'meal': processed_meal,
                'timestamp': datetime.now().isoformat()
            }
        
        return {
            'success': False,
            'error': 'No recipe found',
            'timestamp': datetime.now().isoformat()
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {str(e)}")
        return {
            'success': False,
            'error': f"Failed to fetch random recipe: {str(e)}",
            'timestamp': datetime.now().isoformat()
        }

def get_categories():
    """
    Get all meal categories from TheMealDB API
    
    Returns:
        list: List of meal categories
    """
    try:
        response = requests.get(MEAL_CATEGORIES_API, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        categories = []
        
        if data['categories']:
            for category in data['categories']:
                categories.append({
                    'id': category['idCategory'],
                    'name': category['strCategory'],
                    'image': category['strCategoryThumb'],
                    'description': category['strCategoryDescription']
                })
        
        return {
            'success': True,
            'categories': categories,
            'count': len(categories)
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {str(e)}")
        return {
            'success': False,
            'categories': [],
            'error': str(e)
        }

def search_by_category(category):
    """
    Search for recipes by category
    
    Args:
        category (str): Meal category
    
    Returns:
        dict: Meals in the category
    """
    try:
        params = {'c': category}
        response = requests.get("https://www.themealdb.com/api/json/v1/1/filter.php", 
                              params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        processed_meals = []
        if data['meals']:
            for meal in data['meals']:
                processed_meals.append({
                    'id': meal['idMeal'],
                    'name': meal['strMeal'],
                    'image': meal['strMealThumb']
                })
        
        return {
            'success': True,
            'results': processed_meals,
            'count': len(processed_meals),
            'category': category,
            'timestamp': datetime.now().isoformat()
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {str(e)}")
        return {
            'success': False,
            'results': [],
            'error': f"Failed to fetch recipes: {str(e)}",
            'timestamp': datetime.now().isoformat()
        }

# Routes

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """API endpoint for searching recipes"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Search query is required'
        }), 400
    
    logger.info(f"Searching for recipes: {query}")
    results = search_recipes(query)
    return jsonify(results)

@app.route('/api/random', methods=['GET'])
def random_recipe():
    """API endpoint for getting a random recipe"""
    logger.info("Fetching random recipe")
    result = get_random_recipe()
    return jsonify(result)

@app.route('/api/categories', methods=['GET'])
def categories():
    """API endpoint for getting all categories"""
    logger.info("Fetching categories")
    result = get_categories()
    return jsonify(result)

@app.route('/api/category/<category>', methods=['GET'])
def by_category(category):
    """API endpoint for searching by category"""
    logger.info(f"Fetching recipes from category: {category}")
    result = search_by_category(category)
    return jsonify(result)

@app.route('/api/recipe/<recipe_id>', methods=['GET'])
def get_recipe_details(recipe_id):
    """API endpoint for getting detailed recipe information"""
    try:
        params = {'i': recipe_id}
        response = requests.get(MEAL_BY_ID_API, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['meals']:
            meal = data['meals'][0]
            processed_meal = {
                'id': meal['idMeal'],
                'name': meal['strMeal'],
                'image': meal['strMealThumb'],
                'category': meal['strCategory'],
                'cuisine': meal['strArea'],
                'tags': meal['strTags'].split(',') if meal.get('strTags') else [],
                'instructions': meal['strInstructions'],
                'youtube': meal.get('strYoutube', ''),
                'ingredients': []
            }
            
            # Extract ingredients
            for i in range(1, 21):
                ingredient_key = f'strIngredient{i}'
                measure_key = f'strMeasure{i}'
                
                ingredient = meal.get(ingredient_key, '').strip()
                measure = meal.get(measure_key, '').strip()
                
                if ingredient:
                    processed_meal['ingredients'].append({
                        'ingredient': ingredient,
                        'measure': measure
                    })
            
            return jsonify({
                'success': True,
                'meal': processed_meal
            })
        
        return jsonify({
            'success': False,
            'error': 'Recipe not found'
        }), 404
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
