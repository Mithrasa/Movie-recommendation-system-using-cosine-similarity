// Get the form element
const form = document.querySelector('#recommendation-form');

// Add event listener to form submission
form.addEventListener('submit', (event) => {
  event.preventDefault();

  // Get the user's input
  const movieNameInput = document.querySelector('#movie-name');
  const movieName = movieNameInput.value.trim();

  // Perform validation or further processing if needed
  // ...

  // Make an AJAX request to the server
  fetch('/recommend', {
    method: 'POST',
    body: new URLSearchParams(`movie_name=${encodeURIComponent(movieName)}`)
  })
  .then(response => response.json())
  .then(data => {
    // Handle the response data and update the UI
    // ...

    // Example: Update a <div> element with the movie recommendations
    const recommendationsDiv = document.querySelector('#recommendations');
    recommendationsDiv.innerHTML = '';

    data.movies.forEach((movie, index) => {
      const movieElement = document.createElement('p');
      movieElement.textContent = `${index + 1}. ${movie.title}`;
      recommendationsDiv.appendChild(movieElement);
    });
  })
  .catch(error => {
    console.error('Error:', error);
  });
});
