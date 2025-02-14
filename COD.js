const searchButton = document.querySelector('button');
const searchInput = document.querySelector('input');

function handleSearch() {
    const query = searchInput.value.trim().toLowerCase();
    if (query === 'butter chicken') {
      window.location.href = 'recipes.html';
    } else {
      alert('Recipe not found. Please try another recipe.');
    }
    searchInput.value = ''; 
  }


searchInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  });

const butterChickenCard = document.getElementById('4');


butterChickenCard.addEventListener('click', () => {
  window.location.href = 'recipes.html';
});
