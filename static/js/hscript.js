// script.js
const carousel = document.querySelector('.carousel');
const images = document.querySelectorAll('.carousel-image');
const leftArrow = document.querySelector('.left-arrow');
const rightArrow = document.querySelector('.right-arrow');

let currentIndex = 0;
const totalImages = images.length;

// Function to update carousel position
function updateCarousel() {
  const offset = -currentIndex * 100; // Move carousel by 100% per image
  carousel.style.transform = `translateX(${offset}%)`;
}

// Move to the next image
function nextImage() {
  currentIndex = (currentIndex + 1) % totalImages; // Loop back to the start
  updateCarousel();
}

// Move to the previous image
function prevImage() {
  currentIndex = (currentIndex - 1 + totalImages) % totalImages; // Loop back to the end
  updateCarousel();
}

// Add event listeners for arrows
rightArrow.addEventListener('click', nextImage);
leftArrow.addEventListener('click', prevImage);

// Auto-slide functionality
setInterval(nextImage, 3000); // Move to the next image every 3 seconds


document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".movie-button");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");
    });
  });
});

document.querySelectorAll('.movie-buttons a').forEach(button => {
  button.addEventListener('click', function() {
    // Remove active class from all buttons
    document.querySelectorAll('.movie-buttons a').forEach(btn => {
      btn.classList.remove('active');
    });
    
    // Add active class to the clicked button
    this.classList.add('active');
  });
});

window.onload = function() {
  const mainContent = document.querySelector('main');
  setTimeout(() => {
    mainContent.classList.add('animated');
  }, 100); // Delay of 100 milliseconds
};

