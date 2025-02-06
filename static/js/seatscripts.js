document.addEventListener("DOMContentLoaded", () => {
  const seats = document.querySelectorAll(".seat:not([disabled])"); // Ignore disabled seats
  const selectedSeatsElement = document.getElementById("selected-seats");
  const totalPriceElement = document.getElementById("total-price");
  const summaryBar = document.querySelector(".summary-bar");
  const confirmBookingButton = document.getElementById("confirm-booking");
  const bookingForm = document.getElementById("booking-form");
  const selectedSeatsInput = document.getElementById("selected-seats-input"); // Hidden input

  let selectedSeats = [];
  let totalPrice = 0;

  seats.forEach((seat) => {
    seat.addEventListener("click", () => {
      const isSelected = seat.classList.contains("selected");
      const category = parseInt(seat.parentElement.dataset.category);
      const seatNumber = seat.textContent.trim(); // Trim whitespace
      const rowLabel = seat.parentElement.previousElementSibling.textContent.trim(); // Trim whitespace

      if (!seat.disabled) {
        if (isSelected) {
          // Deselect the seat
          seat.classList.remove("selected");
          selectedSeats = selectedSeats.filter(
            (s) => !(s.seatNumber === seatNumber && s.rowLabel === rowLabel)
          );
          totalPrice -= category;
        } else {
          // Select the seat
          seat.classList.add("selected");
          selectedSeats.push({ seatNumber, rowLabel });
          totalPrice += category;
        }

        // Update the summary
        selectedSeatsElement.textContent = selectedSeats.length
          ? selectedSeats.map((s) => `${s.rowLabel}${s.seatNumber}`).join(", ")
          : "None";
        totalPriceElement.textContent = `₹${totalPrice}`;

        // Show or hide the summary bar
        summaryBar.classList.toggle("active", selectedSeats.length > 0);
      }
    });
  });

  // Submit form on "Confirm Booking"
  confirmBookingButton.addEventListener("click", (event) => {
    if (selectedSeats.length === 0) {
      alert("No seats selected!");
      event.preventDefault(); // Prevent form submission if no seats are selected
      return;
    }

    // Convert selected seats to a comma-separated string and store in hidden input
    selectedSeatsInput.value = selectedSeats.map((s) => `${s.rowLabel}${s.seatNumber}`).join(",");

    // Submit the form
    bookingForm.submit();
  });
});
