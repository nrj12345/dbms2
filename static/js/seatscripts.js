document.addEventListener("DOMContentLoaded", () => {
  const seats = document.querySelectorAll(".seat");
  const selectedSeatsElement = document.getElementById("selected-seats");
  const totalPriceElement = document.getElementById("total-price");
  const summaryBar = document.querySelector(".summary-bar");
  const confirmBookingButton = document.getElementById("confirm-booking");

  let selectedSeats = [];
  let totalPrice = 0;

  seats.forEach((seat) => {
    seat.addEventListener("click", () => {
      const isSelected = seat.classList.contains("selected");
      const category = parseInt(seat.parentElement.dataset.category);
      const seatNumber = seat.textContent;
      const rowLabel = seat.parentElement.previousElementSibling.textContent; // Get the row label

      if (!seat.classList.contains("occupied")) {
        if (isSelected) {
          // Deselect the seat
          seat.classList.remove("selected");
          selectedSeats = selectedSeats.filter(
            (s) => s.seatNumber !== seatNumber || s.rowLabel !== rowLabel
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
          ? selectedSeats
              .map((s) => `${s.rowLabel}${s.seatNumber}`)
              .join(", ")
          : "None";
        totalPriceElement.textContent = totalPrice;

        // Show or hide the summary bar
        if (selectedSeats.length > 0) {
          summaryBar.classList.add("active");
        } else {
          summaryBar.classList.remove("active");
        }
      }
    });
  });

  confirmBookingButton.addEventListener("click", () => {
    const seatDetails = selectedSeats
      .map((s) => `${s.rowLabel}${s.seatNumber}`)
      .join(", ");
    alert(`Booking confirmed for seats: ${seatDetails}\nTotal Price: ₹${totalPrice}`);
    // Reset selection
    selectedSeats.forEach((s) => {
      const seat = Array.from(seats).find(
        (seat) =>
          seat.textContent === s.seatNumber &&
          seat.parentElement.previousElementSibling.textContent === s.rowLabel
      );
      seat.classList.remove("selected");
    });
    selectedSeats = [];
    totalPrice = 0;
    selectedSeatsElement.textContent = "None";
    totalPriceElement.textContent = "0";
    summaryBar.classList.remove("active");
  });
});
