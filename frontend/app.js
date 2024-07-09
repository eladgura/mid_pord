// app.js

// Function to fetch user profile data
function fetchProfile() {
    const token = localStorage.getItem('access_token');
    axios.get('http://localhost:5000/api/users/me', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        const user = response.data;
        document.getElementById('username').textContent = user.username;
        document.getElementById('email').textContent = user.email;
        document.getElementById('is_admin').textContent = user.is_admin ? 'Yes' : 'No';
        document.getElementById('new-username').value = user.username;
        document.getElementById('new-email').value = user.email;
    })
    .catch(error => console.error('Error fetching profile:', error));
}

// Axios GET request to fetch all books
axios.get('http://localhost:5000/api/books')
.then(response => {
    const books = response.data;
    const booksList = document.getElementById('books-list');
    books.forEach(book => {
        const bookDiv = document.createElement('div');
        bookDiv.classList.add('book');
        bookDiv.innerHTML = `
            <img src="http://localhost:5000/api/image/${book.image_filename}" alt="${book.title}">
            <div class="book-details">
                <h2>${book.title}</h2>
                <p>Author: ${book.author}</p>
                <p>Type: ${book.genre}</p>
                <p>In Stock: ${book.in_stock ? 'Yes' : 'No'}</p>
                <button class="loan-btn btn btn-primary" data-book-id="${book.id}">Loan Book</button>
            </div>
        `;
        booksList.appendChild(bookDiv);
    });

    // Function to check if user is authenticated
    const checkLoggedIn = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/auth/check'); // Replace with actual check endpoint
            return response.data.authenticated; // Assuming backend returns authenticated boolean
        } catch (error) {
            console.error('Error checking authentication status:', error);
            return false;
        }
    };

    // Add event listener to loan buttons
    const loanButtons = document.querySelectorAll('.loan-btn');
    loanButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const loggedIn = await checkLoggedIn();
            if (loggedIn) {
                const bookId = button.getAttribute('data-book-id');
                // Send POST request to loan the book
                axios.post(`http://localhost:5000/api/loans`, {
                    user_id: 1, // Replace with actual logged-in user ID
                    book_id: bookId,
                    due_date: new Date().toISOString() // Replace with actual due date logic
                })
                .then(response => {
                    alert(`Book ID ${bookId} successfully loaned!`);
                    // Update UI to reflect loaned status
                    button.disabled = true; // Disable the loan button after successful loan
                })
                .catch(error => {
                    console.error('Error loaning book:', error);
                    alert('Failed to loan the book. Please try again later.');
                });
            } else {
                // Redirect to Login page
                window.location.href = '/login.html'; // Change to appropriate URL
            }
        });
    });

    // Fetch profile on page load (for profile.html)
    if (window.location.pathname === '/profile.html') {
        fetchProfile();
    }
})
.catch(error => console.error('Error fetching books:', error));

// Add other functions as needed for form submissions, etc.
