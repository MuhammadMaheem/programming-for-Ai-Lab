// DOM Elements
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const randomBtn = document.getElementById('randomBtn');
const recipesGrid = document.getElementById('recipesGrid');
const resultsSection = document.getElementById('resultsSection');
const categoriesGrid = document.getElementById('categoriesGrid');
const emptyState = document.getElementById('emptyState');
const recipeModal = document.getElementById('recipeModal');
const searchQuery = document.getElementById('searchQuery');
const resultCount = document.getElementById('resultCount');

// State
let currentSearchQuery = '';
let allCategories = [];

// Event Listeners
searchBtn.addEventListener('click', performSearch);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') performSearch();
});
randomBtn.addEventListener('click', getRandomRecipe);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadCategories();
});

/**
 * Search for recipes
 */
function performSearch() {
    const query = searchInput.value.trim();
    if (!query) {
        alert('Please enter a search term');
        return;
    }
    searchRecipe(query);
}

/**
 * Search recipe wrapper
 */
function searchRecipe(query) {
    currentSearchQuery = query;
    searchInput.value = query;
    searchQuery.textContent = query;
    recipesGrid.innerHTML = '<div class="spinner"></div>';
    resultsSection.style.display = 'block';
    emptyState.style.display = 'none';
    categoriesGrid.style.display = 'none';

    fetch('/api/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.results.length > 0) {
            resultCount.textContent = data.count;
            displayRecipes(data.results);
        } else {
            resultCount.textContent = '0';
            recipesGrid.innerHTML = '';
            emptyState.style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        recipesGrid.innerHTML = '<p style="text-align: center; color: red;">Error loading recipes. Please try again.</p>';
    });
}

/**
 * Display recipes in grid
 */
function displayRecipes(recipes) {
    recipesGrid.innerHTML = '';
    recipes.forEach(recipe => {
        const card = createRecipeCard(recipe);
        recipesGrid.appendChild(card);
    });
}

/**
 * Create recipe card element
 */
function createRecipeCard(recipe) {
    const card = document.createElement('div');
    card.className = 'recipe-card';
    card.innerHTML = `
        <img src="${recipe.image}" alt="${recipe.name}" class="recipe-image" onerror="this.src='https://via.placeholder.com/300x200?text=No+Image'">
        <div class="recipe-content">
            <h3 class="recipe-name">${recipe.name}</h3>
            <div class="recipe-details">
                <div class="detail-item">
                    <span>🍽️</span>
                    <span>${recipe.category}</span>
                </div>
                <div class="detail-item">
                    <span>🌍</span>
                    <span>${recipe.cuisine}</span>
                </div>
            </div>
            <button class="btn-view" onclick="openRecipeModal('${recipe.id}')">View Recipe</button>
        </div>
    `;
    return card;
}

/**
 * Load categories
 */
function loadCategories() {
    fetch('/api/categories')
    .then(response => response.json())
    .then(data => {
        if (data.success && data.categories.length > 0) {
            allCategories = data.categories;
            displayCategories(data.categories);
        }
    })
    .catch(error => console.error('Error loading categories:', error));
}

/**
 * Display categories
 */
function displayCategories(categories) {
    categoriesGrid.innerHTML = '';
    categories.forEach(category => {
        const categoryCard = document.createElement('div');
        categoryCard.className = 'category-card';
        categoryCard.onclick = () => searchByCategory(category.name);
        categoryCard.innerHTML = `
            <div class="category-icon">🍴</div>
            <div class="category-name">${category.name}</div>
        `;
        categoriesGrid.appendChild(categoryCard);
    });
}

/**
 * Search by category
 */
function searchByCategory(categoryName) {
    currentSearchQuery = categoryName;
    searchInput.value = categoryName;
    searchQuery.textContent = categoryName;
    recipesGrid.innerHTML = '<div class="spinner"></div>';
    resultsSection.style.display = 'block';
    emptyState.style.display = 'none';
    categoriesGrid.style.display = 'none';

    fetch(`/api/category/${categoryName}`)
    .then(response => response.json())
    .then(data => {
        if (data.success && data.results.length > 0) {
            resultCount.textContent = data.count;
            displaySimpleRecipes(data.results);
        } else {
            resultCount.textContent = '0';
            recipesGrid.innerHTML = '';
            emptyState.style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        recipesGrid.innerHTML = '<p style="text-align: center; color: red;">Error loading recipes. Please try again.</p>';
    });
}

/**
 * Display simple recipes (from category search)
 */
function displaySimpleRecipes(recipes) {
    recipesGrid.innerHTML = '';
    recipes.forEach(recipe => {
        const card = document.createElement('div');
        card.className = 'recipe-card';
        card.innerHTML = `
            <img src="${recipe.image}" alt="${recipe.name}" class="recipe-image" onerror="this.src='https://via.placeholder.com/300x200?text=No+Image'">
            <div class="recipe-content">
                <h3 class="recipe-name">${recipe.name}</h3>
                <button class="btn-view" onclick="openRecipeModal('${recipe.id}')">View Recipe</button>
            </div>
        `;
        recipesGrid.appendChild(card);
    });
}

/**
 * Get random recipe
 */
function getRandomRecipe() {
    fetch('/api/random')
    .then(response => response.json())
    .then(data => {
        if (data.success && data.meal) {
            openRecipeModalWithData(data.meal);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to fetch random recipe. Please try again.');
    });
}

/**
 * Open recipe modal with ID
 */
function openRecipeModal(recipeId) {
    fetch(`/api/recipe/${recipeId}`)
    .then(response => response.json())
    .then(data => {
        if (data.success && data.meal) {
            openRecipeModalWithData(data.meal);
        } else {
            alert('Failed to load recipe details');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error loading recipe. Please try again.');
    });
}

/**
 * Open modal with recipe data
 */
function openRecipeModalWithData(recipe) {
    document.getElementById('modalTitle').textContent = recipe.name;
    document.getElementById('modalImage').src = recipe.image;
    document.getElementById('modalCategory').textContent = `🍽️ ${recipe.category}`;
    document.getElementById('modalCuisine').textContent = `🌍 ${recipe.cuisine}`;
    
    // Display instructions
    document.getElementById('instructionsText').textContent = recipe.instructions;
    
    // Display ingredients
    const ingredientsList = document.getElementById('ingredientsList');
    ingredientsList.innerHTML = '';
    recipe.ingredients.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span class="ingredient-item">${item.ingredient}</span>
            <span class="ingredient-measure">${item.measure}</span>
        `;
        ingredientsList.appendChild(li);
    });
    
    // Display tags if available
    const tagsSection = document.getElementById('tagsSection');
    if (recipe.tags && recipe.tags.length > 0 && recipe.tags[0] !== '') {
        tagsSection.style.display = 'block';
        const tagsList = document.getElementById('tagsList');
        tagsList.innerHTML = '';
        recipe.tags.forEach(tag => {
            if (tag.trim()) {
                const span = document.createElement('span');
                span.className = 'tag';
                span.textContent = tag.trim();
                tagsList.appendChild(span);
            }
        });
    } else {
        tagsSection.style.display = 'none';
    }
    
    // Display video link if available
    const videoSection = document.getElementById('videoSection');
    const videoLink = document.getElementById('videoLink');
    if (recipe.youtube && recipe.youtube !== '') {
        videoSection.style.display = 'block';
        videoLink.href = recipe.youtube;
    } else {
        videoSection.style.display = 'none';
    }
    
    // Show modal
    recipeModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

/**
 * Close modal
 */
function closeModal(event) {
    // Only close if clicking on the modal background or close button
    if (!event || event.target === recipeModal || event.target.classList.contains('close-btn')) {
        recipeModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    if (event.target === recipeModal) {
        closeModal();
    }
});

// Close modal on Escape key
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && recipeModal.style.display === 'block') {
        closeModal();
    }
});
