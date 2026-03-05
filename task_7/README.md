# BookFinder API - Open Library Search Application

## Project Overview

BookFinder is a full-stack web application that leverages the **Open Library API** to search for books and display bibliographic information. Unlike weather, stocks, news, or NASA imagery APIs, this application uniquely focuses on literary data and bibliographic information from the Internet Archive's stable, free API.

### Why Open Library API?

- **No API Key Required**: Free access without authentication
- **Stable & Maintained**: Long-term stability guaranteed by the Internet Archive
- **Rich Data**: Access to millions of books with comprehensive metadata
- **Unique Domain**: Literary/bibliographic data (not weather, stocks, or news)
- **Reliable**: Has maintained consistent uptime and API structure

## API Details

**API Endpoint**: `https://openlibrary.org/search.json`

**Authentication**: None required (free access)

**Notable Features**:
- Search books by title, author, ISBN, or keywords
- Get detailed book information including publication year, ISBN, covers, edition counts
- Comprehensive metadata for millions of publications
- Stable API structure maintained over years

## Features

### 1. **Book Search**
- Search by title, author, ISBN, or keywords
- Real-time suggestions with quick filters for popular books
- Pagination support for browsing through results

### 2. **Book Details**
- Comprehensive book information including:
  - Title and subtitle
  - Author(s)
  - First publication year
  - Publisher information
  - ISBN number
  - Edition count
  - Available language
  - Book cover images

### 3. **API Health Check**
- Real-time status monitoring of the Open Library API
- Visual indicators showing API availability

### 4. **Responsive UI**
- Modern, gradient-based design
- Mobile-friendly interface
- Smooth animations and transitions
- Modal popup for detailed book information

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **HTTP Client**: Requests library
- **Server**: Flask development server

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **Vanilla JavaScript**: No framework dependencies
- **Responsive Design**: Mobile-first approach

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 3: Open in Browser

Navigate to `http://localhost:5000` in your web browser

## Usage

### Search for Books

1. **Using the Search Bar**
   - Type a book title, author name, or ISBN in the search field
   - Click "Search" or press Enter
   - Browse through results

2. **Using Quick Filters**
   - Click on predefined quick filter buttons (e.g., "Harry Potter", "Science Fiction")
   - Instant search with popular queries

3. **Browse Results**
   - Results are displayed in a card grid layout
   - Each card shows:
     - Book cover image (if available)
     - Title and author
     - Publication year
     - Number of editions
     - ISBN and language

### View Book Details

- Click on any book card to open detailed information
- Link to full Open Library page for more information

### Navigate Results

- Use pagination buttons to browse through pages
- Page info shows current position and total results

## API Endpoints

### 1. Search Books
```
GET /api/search?q=<query>&limit=<limit>&offset=<offset>
POST /api/search
```

**Parameters**:
- `q` (string): Search query (required)
- `limit` (int): Number of results (default: 20, max: 100)
- `offset` (int): Pagination offset (default: 0)

**Example**:
```bash
curl "http://localhost:5000/api/search?q=Harry%20Potter&limit=10"
```

### 2. Get Book Details
```
GET /api/book/<book_key>
```

**Example**:
```bash
curl "http://localhost:5000/api/book/OL12345W"
```

### 3. Health Check
```
GET /api/health
```

**Response**:
```json
{
    "status": "healthy",
    "timestamp": "2026-03-03T10:30:00",
    "open_library_api": "online",
    "version": "1.0"
}
```

### 4. Trending Books
```
GET /api/trending
```

## Project Structure

```
task_7/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── style.css         # CSS styling
    └── script.js         # Frontend JavaScript
```

## Code Features

### Backend Highlights
- **Error Handling**: Comprehensive error handling for API failures
- **Logging**: Built-in logging for debugging
- **Request Timeout**: 10-second timeout to prevent hanging
- **Response Processing**: Data enrichment and normalization
- **CORS Ready**: Can be extended for cross-origin requests

### Frontend Highlights
- **Vanilla JavaScript**: No external dependencies for core functionality
- **Error Recovery**: User-friendly error messages
- **Loading States**: Visual feedback during API calls
- **Responsive Grid**: Adaptive layout for all screen sizes
- **Modal System**: Clean modal popup for detailed views
- **Pagination**: Smooth pagination with disabled states

## Error Handling

The application gracefully handles various error scenarios:

1. **Empty Search Query**: Validation at both client and server
2. **API Timeout**: 10-second timeout with error messages
3. **network Errors**: Detailed error reporting
4. **No Results Found**: User-friendly empty state message
5. **API Downtime**: Health check system with fallback handling

## Configuration

### Search Limits
- Default result limit: 20 books per page
- Maximum API limit: 100 results
- Pagination offset increments by RESULTS_PER_PAGE

### Timeouts
- API request timeout: 10 seconds
- Health check interval: 30 seconds

## Performance Considerations

1. **Pagination**: Results are paginated to reduce initial load
2. **Lazy Loading**: Book covers loaded on demand
3. **Caching**: Can be extended with caching layer (Redis, etc.)
4. **Rate Limiting**: Open Library API has generous rate limits
5. **CDN Images**: Cover images served from Open Library's CDN

## Future Enhancements

1. **Advanced Filtering**: Filter by publication year, language, publisher
2. **User Ratings**: Integration with Goodreads API for ratings
3. **Favorites List**: Save favorite books for later
4. **Reading Lists**: Create and manage reading lists
5. **Database Integration**: Store search history and user preferences
6. **Export Options**: Download search results as CSV/PDF
7. **Social Sharing**: Share book discoveries on social media

## Known Limitations

1. **No Authentication**: Application is publicly accessible
2. **No Persistence**: No database storage (stateless)
3. **Rate Limiting**: Subject to Open Library's rate limits
4. **Cover Availability**: Not all books have cover images available
5. **Limited Book Details**: Some book metadata may be incomplete

## Troubleshooting

### Application won't start
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Search doesn't work
- Check internet connection
- Verify Open Library API is accessible: `curl https://openlibrary.org/search.json?q=test`
- Check application logs for error messages

### No book covers displayed
- This is normal for older or obscure books
- Open Library maintains covers for popular titles
- Fallback emoji (📚) is displayed when covers unavailable

## API Reliability Statement

As of March 2026, the Open Library API (`openlibrary.org`) remains:
- **Active**: Fully operational with no announced deprecation plans
- **Free**: No API keys or subscriptions required
- **Stable**: Consistent API structure maintained over multiple years
- **Well-Maintained**: Regular updates and improvements by Internet Archive

## License

This project is created for educational purposes as part of the "Programming for Artificial Intelligence" course.

## References

- **Open Library API**: https://openlibrary.org/developers/api
- **Internet Archive**: https://archive.org/
- **Open Library**: https://openlibrary.org/

## Support

For issues or questions, refer to:
- Open Library API documentation: https://openlibrary.org/developers/api
- Open Library GitHub: https://github.com/internetarchive/openlibrary

---

**Version**: 1.0  
**Last Updated**: March 3, 2026  
**Status**: Active and Maintained
