"""
BookFinder API Application
Uses the Open Library API to search for books and display bibliographic information
No API key required - free and stable API maintained by Internet Archive
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

# Open Library API endpoint
OPEN_LIBRARY_API = "https://openlibrary.org/search.json"

def search_books(query, limit=20, offset=0):
    """
    Search for books using the Open Library API
    
    Args:
        query (str): Search query (title, author, ISBN, etc.)
        limit (int): Number of results to return (default: 20)
        offset (int): Pagination offset (default: 0)
    
    Returns:
        dict: Search results with books and metadata
    """
    try:
        params = {
            'q': query,
            'limit': min(limit, 100),  # API has a max limit of 100
            'offset': offset
        }
        
        response = requests.get(OPEN_LIBRARY_API, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Process and enhance the results
        processed_books = []
        if 'docs' in data:
            for book in data['docs']:
                processed_book = {
                    'title': book.get('title', 'Unknown Title'),
                    'author': ', '.join(book.get('author_name', ['Unknown Author'])[:3]),
                    'first_publish_year': book.get('first_publish_year'),
                    'isbn': book.get('isbn', ['N/A'])[0] if book.get('isbn') else 'N/A',
                    'edition_count': book.get('edition_count'),
                    'cover_id': book.get('cover_i'),
                    'key': book.get('key'),
                    'subtitle': book.get('subtitle'),
                    'publisher': ', '.join(book.get('publisher', ['N/A'])[:2]),
                    'language': ', '.join(book.get('language', ['en'])[:2]),
                }
                processed_books.append(processed_book)
        
        return {
            'success': True,
            'query': query,
            'books': processed_books,
            'total_results': data.get('numFound', 0),
            'returned_count': len(processed_books),
            'timestamp': datetime.now().isoformat()
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return {
            'success': False,
            'error': f'Failed to fetch data from Open Library API: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'success': False,
            'error': f'An unexpected error occurred: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

def get_book_details(book_key):
    """
    Get detailed information about a specific book
    
    Args:
        book_key (str): The Open Library book key (e.g., '/works/OL12345W')
    
    Returns:
        dict: Detailed book information
    """
    try:
        url = f"https://openlibrary.org{book_key}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        details = {
            'success': True,
            'title': data.get('title'),
            'description': data.get('description'),
            'first_published': data.get('first_published'),
            'author_key': data.get('author_key'),
            'covers': data.get('covers'),
            'editions': data.get('editions_count'),
            'key': data.get('key'),
            'timestamp': datetime.now().isoformat()
        }
        
        return details
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get book details: {str(e)}")
        return {
            'success': False,
            'error': f'Failed to fetch book details: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

@app.route('/')
def index():
    """Render the main search interface"""
    return render_template('index.html')

@app.route('/api/search', methods=['GET', 'POST'])
def api_search():
    """
    Search endpoint - accepts both GET and POST requests
    Query parameters: q (query), limit (int), offset (int)
    """
    # Handle both GET and POST
    if request.method == 'POST':
        data = request.get_json()
        query = data.get('q', '').strip()
        limit = data.get('limit', 20)
        offset = data.get('offset', 0)
    else:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Search query is required',
            'timestamp': datetime.now().isoformat()
        }), 400
    
    if len(query) < 2:
        return jsonify({
            'success': False,
            'error': 'Search query must be at least 2 characters',
            'timestamp': datetime.now().isoformat()
        }), 400
    
    results = search_books(query, limit, offset)
    return jsonify(results)

@app.route('/api/book/<path:book_key>', methods=['GET'])
def api_book_details(book_key):
    """
    Get detailed information about a specific book
    book_key should be URL-encoded (e.g., 'OL12345W' or 'works/OL12345W')
    """
    if not book_key:
        return jsonify({
            'success': False,
            'error': 'Book key is required',
            'timestamp': datetime.now().isoformat()
        }), 400
    
    # Ensure the key is properly formatted
    if not book_key.startswith('/works/') and not book_key.startswith('/books/'):
        book_key = '/works/' + book_key
    
    details = get_book_details(book_key)
    return jsonify(details)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API status and connectivity"""
    try:
        response = requests.head(OPEN_LIBRARY_API, timeout=5)
        api_status = 'online' if response.status_code == 200 else 'degraded'
    except:
        api_status = 'offline'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'open_library_api': api_status,
        'version': '1.0'
    })

@app.route('/api/trending', methods=['GET'])
def api_trending():
    """
    Get trending/popular books (based on edition count)
    """
    try:
        # Search for common terms to get popular books
        popular_queries = ['the ', 'a ', 'harry potter']
        
        # Use a simple query that returns many results sorted by relevance
        params = {
            'q': 'book',
            'limit': 20,
            'sort': 'key'
        }
        
        response = requests.get(OPEN_LIBRARY_API, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        processed_books = []
        
        if 'docs' in data:
            # Sort by edition count (proxy for popularity)
            sorted_books = sorted(
                data['docs'],
                key=lambda x: x.get('edition_count', 0),
                reverse=True
            )[:20]
            
            for book in sorted_books:
                processed_book = {
                    'title': book.get('title', 'Unknown Title'),
                    'author': ', '.join(book.get('author_name', ['Unknown Author'])[:3]),
                    'first_publish_year': book.get('first_publish_year'),
                    'isbn': book.get('isbn', ['N/A'])[0] if book.get('isbn') else 'N/A',
                    'edition_count': book.get('edition_count'),
                    'cover_id': book.get('cover_i'),
                    'key': book.get('key'),
                }
                processed_books.append(processed_book)
        
        return jsonify({
            'success': True,
            'books': processed_books,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Trending books error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to fetch trending books: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'timestamp': datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
