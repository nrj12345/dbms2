// Counters for new movies – ensure new movies get unique keys.
let newMovieCounter = 0;

// Image selection and preview functions
function selectImage(imgElement) {
  imgElement.previousElementSibling.click();
}
function previewImage(input) {
  const file = input.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      input.nextElementSibling.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
}

function addMovie() {
  const container = document.getElementById("movies-container");
  if (container.children.length >= 5) {
    alert("You can only add up to 5 movies.");
    return;
  }
  // Generate a unique temporary key for the new movie.
  const key = 'new_' + newMovieCounter++;
  const newMovie = document.createElement("div");
  newMovie.classList.add("movie-container", "flex", "bg-gray-800", "rounded-lg", "shadow-md", "p-4", "space-x-6", "relative");
  newMovie.setAttribute("data-key", key);
  newMovie.innerHTML = `
    <input type="hidden" name="movie_key" value="${key}">
    <div class="movie-poster flex-shrink-0 w-40">
      <label class="block text-sm font-medium mb-1">Upload Poster:</label>
      <input type="file" name="movies[${key}][poster]" accept="image/*" class="hidden" onchange="previewImage(this)">
      <img src="" alt="Movie Poster" class="poster-preview w-full h-52 bg-gray-700 rounded-md object-cover cursor-pointer" onclick="selectImage(this)">
    </div>
    <div class="movie-details flex-grow">
      <label class="block text-sm font-medium mb-1">Movie Title:</label>
      <input type="text" name="movies[${key}][movie_title]" class="w-full bg-gray-700 text-white p-2 rounded-md" required>
      <div class="genres mt-4">
        <label class="block text-sm font-medium">Genres (Max: 3):</label>
        <div class="genre-container space-y-2">
          <input type="text" name="movies[${key}][genre][]" class="w-full bg-gray-700 text-white p-2 rounded-md genre-input" required>
        </div>
        <div class="flex space-x-2 mt-2">
          <button type="button" onclick="addGenre(this)" class="bg-blue-600 px-3 py-1 rounded">Add Genre</button>
          <button type="button" onclick="removeGenre(this)" class="bg-red-600 px-3 py-1 rounded">Remove Genre</button>
        </div>
      </div>
      <div class="time-slots mt-4">
        <label class="block text-sm font-medium">Time Slots:</label>
        <div class="time-slot-container space-y-2">
          <div class="flex space-x-2">
            <input type="time" name="movies[${key}][time_slots][]" class="bg-gray-700 text-white p-2 rounded-md" required>
            <select name="movies[${key}][screen][]" class="bg-gray-700 text-white p-2 rounded-md" required>
              <option value="1">Screen 1</option>
              <option value="2">Screen 2</option>
            </select>
            <button type="button" onclick="removeTimeSlot(this)" class="bg-red-600 text-white px-2 py-1 rounded text-xs">Remove</button>
          </div>
        </div>
        <button type="button" onclick="addTimeSlot(this)" class="mt-2 bg-blue-600 px-3 py-1 rounded">Add Time Slot</button>
      </div>
    </div>
    <button type="button" onclick="deleteMovie(this)" class="absolute top-2 right-2 bg-red-600 text-white px-2 py-1 rounded text-xs">Delete</button>
  `;
  container.appendChild(newMovie);
}

function deleteMovie(button) {
  const movieContainer = button.closest(".movie-container");
  const timeSlots = movieContainer.querySelectorAll("input[name*='[time_slots][]']");
  if (timeSlots.length > 1) {
    movieContainer.remove();
  } else {
    alert("A movie must have at least one time slot.");
  }
}

function addGenre(button) {
  const container = button.closest(".movie-details").querySelector(".genre-container");
  if (container && container.children.length < 3) {
    const movieContainer = button.closest(".movie-container");
    const key = movieContainer.getAttribute("data-key");
    const input = document.createElement("input");
    input.type = "text";
    input.name = `movies[${key}][genre][]`;
    input.className = "w-full bg-gray-700 text-white p-2 rounded-md genre-input";
    input.required = true;
    container.appendChild(input);
  }
}

function removeGenre(button) {
  const container = button.closest(".movie-details").querySelector(".genre-container");
  const inputs = container.querySelectorAll(".genre-input");
  if (inputs.length > 1) {
    container.removeChild(inputs[inputs.length - 1]);
  }
}

function addTimeSlot(button) {
  const container = button.parentElement.querySelector(".time-slot-container");
  const movieContainer = button.closest(".movie-container");
  const key = movieContainer.getAttribute("data-key");
  const div = document.createElement("div");
  div.classList.add("flex", "space-x-2");
  div.innerHTML = `
    <input type="time" name="movies[${key}][time_slots][]" class="bg-gray-700 text-white p-2 rounded-md" required>
    <select name="movies[${key}][screen][]" class="bg-gray-700 text-white p-2 rounded-md" required>
      <option value="1">Screen 1</option>
      <option value="2">Screen 2</option>
    </select>
    <button type="button" onclick="removeTimeSlot(this)" class="bg-red-600 text-white px-2 py-1 rounded text-xs">Remove</button>
  `;
  container.appendChild(div);
}

function removeTimeSlot(button) {
  const container = button.closest(".time-slot-container");
  const slots = container.querySelectorAll("div");
  if (slots.length > 1) {
    button.closest("div").remove();
  } else {
    alert("A movie must have at least one time slot.");
  }
}