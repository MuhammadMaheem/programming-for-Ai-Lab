/**
 * BookFinder API - Frontend JavaScript
 * Handles search, pagination, and UI interactions
 */

const COVER_URL_BASE = 'https://covers.openlibrary.org/b/id';
let currentResults = [];
let currentPage = 0;
const RESULTS_PER_PAGE = 20;
let totalResults = 0;

// DOM Elements
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultsContainer = document.getElementById('resultsContainer');
const resultsList = document.getElementById('resultsList');
const loadingContainer = document.getElementById('loadingContainer');
const errorContainer = document.getElementById('errorContainer');
const emptyContainer = document.getElementById('emptyContainer');
const errorText = document.getElementById('errorText');
const resultCount = document.getElementById('resultCount');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const pageInfo = document.getElementById('pageInfo');
const statusIndicator = document.getElementById('status-indicator');
const statusText = document.getElementById('status-text');
const filterBtns = document.querySelectorAll('.filter-btn');
const bookModal = document.getElementById('bookModal');

// Initialize event listeners
document.addEventListener('DOMContentLoaded', () => {
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });

    prevBtn.addEventListener('click', () => {
        if (currentPage > 0) {
            currentPage--;
            displayResults();
        }
    });

    nextBtn.addEventListener('click', () => {
        const maxPages = Math.ceil(totalResults / RESULTS_PER_PAGE);
        if (currentPage < maxPages - 1) {
            currentPage++;
            displayResults();
        }
    });

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            searchInput.value = btn.dataset.query;
            performSearch();
        });
    });

    // Check API health
    checkAPIHealth();
    setInterval(checkAPIHealth, 30000); // Check every 30 seconds
});

/**
 * Check if the Open Library API is accessible
 */
function checkAPIHealth() {
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            const apiStatus = data.open_library_api;
            updateStatusIndicator(apiStatus);
        })
        .catch(error => {
            updateStatusIndicator('offline');
        });
}

/**
 * Update the API status indicator
 */
function updateStatusIndicator(status) {
    const statusMap = {
        'online': { class: 'online', text: 'Open Library API Online' },
        'degraded': { class: 'offline', text: 'Open Library API Degraded' },
        'offline': { class: 'offline', text: 'Open Library API Offline' }
    };

    const info = statusMap[status] || statusMap['offline'];
    statusIndicator.className = 'status-dot ' + info.class;
    statusText.textContent = info.text;
}

/**
 * Perform the book search
 */
function performSearch() {
    const query = searchInput.value.trim();

    if (!query) {
        showError('Please enter a search query');
        return;
    }

    if (query.length < 2) {
        showError('Search query must be at least 2 characters');
        return;
    }

    currentPage = 0;
    searchBooks(query);
}

/**
 * Search for books using the backend API
 */
function searchBooks(query) {
    hideError();
    hideResults();
    showLoading();

    const params = new URLSearchParams({
        q: query,
        limit: RESULTS_PER_PAGE,
        offset: currentPage * RESULTS_PER_PAGE
    });

    fetch(`/api/search?${params}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            hideLoading();

            if (!data.success) {
                showError(data.error || 'Failed to search books');
                return;
            }

            if (data.books.length === 0) {
                showEmpty();
                return;
            }

            currentResults = data.books;
            totalResults = data.total_results;
            displayResults();
        })
        .catch(error => {
            hideLoading();
            showError(`Error: ${error.message}`);
            console.error('Search error:', error);
        });
}

/**
 * Display the current page of results
 */
function displayResults() {
    resultsList.innerHTML = '';

    currentResults.forEach(book => {
        const bookCard = createBookCard(book);
        resultsList.appendChild(bookCard);
    });

    // Update pagination info
    const maxPages = Math.ceil(totalResults / RESULTS_PER_PAGE);
    resultCount.textContent = `${totalResults} books found`;
    pageInfo.textContent = `Page ${currentPage + 1} of ${maxPages}`;

    // Update pagination buttons
    prevBtn.disabled = currentPage === 0;
    nextBtn.disabled = currentPage >= maxPages - 1;

    showResults();
    window.scrollTo({ top: resultsContainer.offsetTop - 100, behavior: 'smooth' });
}

/**
 * Create a book card element
 */
function createBookCard(book) {
    const card = document.createElement('div');
    card.className = 'book-card';
    card.style.cursor = 'pointer';

    const coverHTML = book.cover_id
        ? `<img src="${COVER_URL_BASE}/${book.cover_id}-M.jpg" alt="${book.title}">`
        : `<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-size: 3rem; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%;">📚</div>`;

    card.innerHTML = `
        <div class="book-cover">
            ${coverHTML}
        </div>
        <div class="book-info">
            <div class="book-title">${escapeHtml(book.title)}</div>
            <div class="book-author">${escapeHtml(book.author || 'Unknown Author')}</div>
            <div class="book-meta">
                ${book.first_publish_year ? `<div class="book-meta-item"><strong>Year:</strong> ${book.first_publish_year}</div>` : ''}
                ${book.edition_count ? `<div class="book-meta-item"><strong>Editions:</strong> ${book.edition_count}</div>` : ''}
                ${book.isbn !== 'N/A' ? `<div class="book-meta-item"><strong>ISBN:</strong> ${book.isbn}</div>` : ''}
                ${book.language ? `<div class="book-meta-item"><strong>Language:</strong> ${book.language}</div>` : ''}
            </div>
        </div>
    `;

    card.addEventListener('click', () => showBookDetails(book));
    return card;
}

/**
 * Show detailed book information in a modal
 */
function showBookDetails(book) {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
            <div style="flex: 0 0 200px;">
                ${book.cover_id 
                    ? `<img src="${COVER_URL_BASE}/${book.cover_id}-M.jpg" alt="${book.title}" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">`
                    : `<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-size: 5rem; display: flex; align-items: center; justify-content: center; width: 100%; height: 300px; border-radius: 8px;">📚</div>`}
            </div>
            <div style="flex: 1; min-width: 250px;">
                <h2 style="margin-bottom: 15px; color: #1f2937;">${escapeHtml(book.title)}</h2>
                ${book.subtitle ? `<p style="color: #6b7280; font-style: italic; margin-bottom: 15px;">${escapeHtml(book.subtitle)}</p>` : ''}
                
                <div style="margin-bottom: 20px;">
                    <h3 style="color: #374151; margin-bottom: 8px;">Author</h3>
                    <p style="color: #6b7280;">${escapeHtml(book.author || 'Unknown Author')}</p>
                </div>

                ${book.first_publish_year ? `
                    <div style="margin-bottom: 15px;">
                        <h3 style="color: #374151; margin-bottom: 8px;">First Published</h3>
                        <p style="color: #6b7280;">${book.first_publish_year}</p>
                    </div>
                ` : ''}

                ${book.publisher ? `
                    <div style="margin-bottom: 15px;">
                        <h3 style="color: #374151; margin-bottom: 8px;">Publisher</h3>
                        <p style="color: #6b7280;">${escapeHtml(book.publisher)}</p>
                    </div>
                ` : ''}

                ${book.isbn !== 'N/A' ? `
                    <div style="margin-bottom: 15px;">
                        <h3 style="color: #374151; margin-bottom: 8px;">ISBN</h3>
                        <p style="color: #6b7280; font-family: monospace;">${book.isbn}</p>
                    </div>
                ` : ''}

                ${book.edition_count ? `
                    <div style="margin-bottom: 15px;">
                        <h3 style="color: #374151; margin-bottom: 8px;">Total Editions</h3>
                        <p style="color: #6b7280;">${book.edition_count}</p>
                    </div>
                ` : ''}

                ${book.language ? `
                    <div style="margin-bottom: 15px;">
                        <h3 style="color: #374151; margin-bottom: 8px;">Language</h3>
                        <p style="color: #6b7280;">${escapeHtml(book.language)}</p>
                    </div>
                ` : ''}

                ${book.key ? `
                    <a href="https://openlibrary.org${book.key}" target="_blank" style="display: inline-block; margin-top: 15px; padding: 10px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">
                        View on Open Library →
                    </a>
                ` : ''}
            </div>
        </div>
    `;
    bookModal.classList.remove('hidden');
}

/**
 * Close the book details modal
 */
function closeBookModal() {
    bookModal.classList.add('hidden');
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * UI Helper functions
 */
function showResults() {
    resultsContainer.classList.remove('hidden');
    emptyContainer.classList.add('hidden');
}

function hideResults() {
    resultsContainer.classList.add('hidden');
}

function showLoading() {
    loadingContainer.classList.remove('hidden');
}

function hideLoading() {
    loadingContainer.classList.add('hidden');
}

function showError(message) {
    errorText.textContent = message;
    errorContainer.classList.remove('hidden');
}

function hideError() {
    errorContainer.classList.add('hidden');
}

function showEmpty() {
    emptyContainer.classList.remove('hidden');
    resultsContainer.classList.add('hidden');
}

// Close modal when clicking outside it
bookModal.addEventListener('click', (e) => {
    if (e.target === bookModal) {
        closeBookModal();
    }
});
