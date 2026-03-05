# 🍳 Recipe Finder - Flask Web Application

A modern, dynamic Flask-based web application for discovering and exploring recipes from around the world. The app uses the **TheMealDB API** (free, no authentication required) to fetch real recipe data with ingredients, instructions, and more.

## 📋 Features

### Frontend Features
- **Dynamic Search**: Real-time recipe search with instant results
- **Category Browsing**: Browse recipes by popular meal categories
- **Random Recipe Generator**: Discover new recipes with a single click
- **Detailed Recipe Modal**: View complete recipe information including:
  - Full ingredients list with measurements
  - Step-by-step cooking instructions
  - Meal category and cuisine type
  - Tags and dietary information
  - YouTube video links (when available)
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Interactive UI**: Smooth animations and transitions for better user experience
- **Popular Search Tags**: Quick access to common searches (Pasta, Pizza, Chicken, etc.)

### Backend Features
- **RESTful API Endpoints**: Clean, well-documented API endpoints
- **Multiple Search Methods**:
  - Search by recipe name
  - Browse by category
  - Get a random recipe
  - Detailed recipe lookup
- **Error Handling**: Comprehensive error handling and logging
- **Caching-Friendly**: Works efficiently with API rate limits
- **Detailed Logging**: Tracks all requests and issues for debugging

## 🍳 API Endpoints

### Available Routes

#### Search Recipes
```
POST /api/search
Content-Type: application/json

Body: { "query": "pasta" }
Returns: List of recipes matching the search term
```

#### Get Random Recipe
```
GET /api/random
Returns: A random recipe with full details
```

#### Get All Categories
```
GET /api/categories
Returns: List of all available meal categories
```

#### Search by Category
```
GET /api/category/<category_name>
Returns: List of recipes in the specified category
```

#### Get Recipe Details
```
GET /api/recipe/<recipe_id>
Returns: Complete details for a specific recipe
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Step 1: Clone and Navigate
```bash
cd "task_8"
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 5: Open in Browser
Open your web browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
task_8/
├── app.py                 # Flask application with all API routes
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template with interactive UI
└── static/
    ├── style.css         # Modern styling with gradients and animations
    └── script.js         # Dynamic frontend functionality
```

## 🛠️ Technologies Used

### Backend
- **Flask 2.3.3**: Lightweight Python web framework
- **Requests 2.31.0**: HTTP library for API calls
- **Werkzeug 2.3.7**: WSGI utility library (included with Flask)

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with flexbox and grid layouts
- **Vanilla JavaScript**: Dynamic interactivity without jQuery

### External API
- **TheMealDB API**: Free recipe database
  - Base URL: `https://www.themealdb.com/api/json/v1/1/`
  - No authentication required
  - Rate limit: Generous for personal use

## 💡 How to Use

### Basic Search
1. Enter a recipe name in the search box (e.g., "Pasta", "Pizza", "Chicken")
2. Click the "Search" button or press Enter
3. Browse through the results
4. Click "View Recipe" on any recipe card to see full details

### Browse by Category
1. Scroll down to the "Browse by Category" section
2. Click on any category (e.g., Seafood, Vegetarian, Dessert)
3. View all recipes in that category

### Get Random Recipe
1. Click the "🎲 Random Recipe" button in the top navigation
2. A random recipe modal will open with full details

### View Recipe Details
1. Click "View Recipe" on any recipe card
2. A modal opens showing:
   - High-quality recipe image
   - Complete ingredients list with measurements
   - Detailed cooking instructions
   - Meal category and cuisine type
   - Any tags or dietary information
   - YouTube video link (if available)

## 🎨 User Interface Highlights

### Color Scheme
- **Primary Orange**: `#FF6B35` - Main actions and highlights
- **Secondary Orange**: `#F7931E` - Accent color
- **Tertiary Yellow**: `#FDB913` - Supporting elements
- Clean, modern design with smooth animations

### Responsive Breakpoints
- **Desktop**: 1200px+ (full grid view)
- **Tablet**: 768px - 1199px (adjusted grid)
- **Mobile**: Below 768px (single column or 2-column layout)

## 🔒 Security Notes

- No sensitive data is stored
- External API calls are made directly from the backend
- No user authentication required
- CORS headers are not explicitly set (requests from same origin only)
- Debug mode should be disabled in production (`debug=False`)

## 🐛 Troubleshooting

### "Recipe not found" for specific searches
- The TheMealDB API has a limited dataset. Try different search terms
- Common searches: "Pasta", "Pizza", "Chicken", "Fish", "Vegetable"

### API Timeout Issues
- The free API has rate limits
- Wait a few moments and try again
- Reduce the number of simultaneous requests

### Images Not Loading
- Some recipes may have broken image links
- The app shows a placeholder image automatically

### Port Already in Use
- If port 5000 is already in use, modify the last line in `app.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)  # Change port to 5001
  ```

## 🚀 Future Enhancements

- Add user accounts and recipe favorites
- Implement recipe ratings and reviews
- Add nutritional information
- Search filters (prep time, difficulty, allergies)
- Recipe sharing on social media
- Add shopping list feature
- Meal planning calendar
- Dark mode theme

## 📄 License

This project is free to use and modify for educational purposes.

## 🙏 Credits

- **TheMealDB API**: https://www.themealdb.com/
- **Flask**: https://flask.palletsprojects.com/
- Icons and design inspiration from modern web applications

## 📞 Support

For issues or questions about this project, please refer to the following:
- Check the required Python version matches (3.7+)
- Verify all packages in `requirements.txt` are installed
- Ensure you're using a compatible Flask version (2.3.3)

---

Happy Cooking! 🍽️👨‍🍳
