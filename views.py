import os
from datetime import datetime
from flask import render_template, request, redirect, url_for, make_response, session
from models import User, Movie, Seat, Ticket, Booking, SessionLocal

# Home page
def home():
    return render_template('home.html')

# About page
def about():
    return render_template('about.html')

# Contact page
def contact():
    return render_template('contact.html')

def admin():
    db = SessionLocal()
    if request.method == 'POST':
        changes_made = False

        # Get a list of all submitted movie keys
        movie_keys = request.form.getlist('movie_key')

        # Build a dictionary of existing movies using their movie_id as string keys.
        existing_movies = {str(m.movie_id): m for m in db.query(Movie).all()}

        # Track which existing movies were processed.
        processed_keys = set()

        for key in movie_keys:
            # Use the key in all our form field names.
            # For existing movies, a hidden movie_id will be submitted.
            movie_id_field = request.form.get(f"movies[{key}][movie_id]")
            movie_title = request.form.get(f"movies[{key}][movie_title]")
            genres = request.form.getlist(f"movies[{key}][genre][]")
            time_slots = request.form.getlist(f"movies[{key}][time_slots][]")
            screens = request.form.getlist(f"movies[{key}][screen][]")

            genre_str = ','.join(genres)
            time_slots_str = ','.join(time_slots)  # keep order as is
            screen_str = ','.join(screens)         # keep order as is

            poster_file = request.files.get(f"movies[{key}][poster]")

            if movie_id_field:
                # Existing movie – update record.
                movie = existing_movies.get(movie_id_field)
                if movie:
                    if (movie.name != movie_title or movie.genre != genre_str or
                        movie.time_slots.strip() != time_slots_str or
                        movie.screen.strip() != screen_str or
                        (poster_file and poster_file.filename)):
                        
                        movie.name = movie_title
                        movie.genre = genre_str
                        movie.time_slots = time_slots_str
                        movie.screen = screen_str

                        if poster_file and poster_file.filename:
                            poster_path = os.path.join('static', 'img', f"{movie.movie_id}.jpg")
                            poster_file.save(poster_path)
                        
                        db.commit()
                        changes_made = True
                    processed_keys.add(movie_id_field)
            else:
                # New movie – create record.
                new_movie = Movie(
                    name=movie_title,
                    genre=genre_str,
                    time_slots=time_slots_str,
                    screen=screen_str
                )
                db.add(new_movie)
                db.commit()  # commit to generate movie_id
                db.refresh(new_movie)

                if poster_file and poster_file.filename:
                    poster_path = os.path.join('static', 'img', f"{new_movie.movie_id}.jpg")
                    poster_file.save(poster_path)
                db.commit()
                changes_made = True

        # Delete movies that were not present in the submitted form.
        for movie_id, movie in existing_movies.items():
            if movie_id not in processed_keys:
                poster_path = os.path.join('static', 'img', f"{movie.movie_id}.jpg")
                if os.path.exists(poster_path):
                    os.remove(poster_path)
                db.delete(movie)
        db.commit()
        db.close()
        return redirect(url_for('admin'))

    else:  # GET request
        movies = db.query(Movie).all()
        movies_list = []
        for m in movies:
            time_slots = m.time_slots.split(',') if m.time_slots else []
            screens = m.screen.split(',') if m.screen else []
            zipped_slots = list(zip(time_slots, screens)) if time_slots and screens else []
            movies_list.append({
                'movie_id': m.movie_id,
                'movie_title': m.name,
                'genres': m.genre.split(',') if m.genre else [],
                'time_slots': zipped_slots
            })
        db.close()
        return render_template('admin.html', movies=movies_list)

# Book Now page (movie selection)
def book_now():
    db = SessionLocal()
    movies = db.query(Movie).all()  # Fetch all movies from DB
    db.close()
    return render_template('booknow.html', movies=movies)  # Pass movies to template

# Screen page (seat selection)
def screen():
    movie_id = request.args.get("movie_id")  # Get movie ID from query parameter
    time_slot = request.args.get("time")     # Get time slot from query parameter
    screen_number = request.args.get("screen")  # Get screen number from query parameter

    # Validate inputs
    if not movie_id or not time_slot or not screen_number:
        return "Invalid inputs", 400

    try:
        movie_id = int(movie_id)
        screen_number = int(screen_number)
    except ValueError:
        return "Invalid inputs", 400

    db = SessionLocal()

    # Fetch movie details from the Movie table
    movie = db.query(Movie).filter_by(movie_id=movie_id).first()
    if not movie:
        return "Movie not found", 404

    # Fetch seat details for the given screen number from the Seat table
    seat_details = db.query(Seat).filter_by(screen=screen_number).first()
    if not seat_details:
        return "No seat details found for this screen", 404

    # Fetch booked seats from the Ticket table
    booked_seats = db.query(Ticket).filter_by(movie_id=movie_id, time_slot=time_slot, screen=screen_number).all()
    booked_seat_numbers = [ticket.seat for ticket in booked_seats]

    db.close()

    # Render the screen template with required details
    return render_template(
        "screen.html",
        movie=movie,  # Pass the movie object to the template
        time_slot=time_slot,
        booked_seat_numbers=booked_seat_numbers,
        seat_details=seat_details  # Pass the seat details object to the template
    )


# Profile page
def profile():
    return render_template('profile.html')

# Sign Up page
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    if password != confirm_password:
        error = 'Passwords do not match'
        return render_template('signup.html', error=error)

    user = User(email=email, name=name)
    user.set_password(password)

    db = SessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    response = make_response(redirect(url_for('home')))
    response.set_cookie('user_data', f"{user.user_id}|{email}", max_age=600)  # Cookie valid for 5 minutes

    return response

# Login page
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    db = SessionLocal()
    user = db.query(User).filter_by(email=email).first()
    db.close()

    if not user or not user.check_password(password):
        error = 'Invalid email or password'
        return render_template('login.html', error=error)

    response = make_response(redirect(url_for('home')))
    response.set_cookie('user_data', f"{user.user_id}|{email}", max_age=600)  # 5 minutes

    return response

# Handle the booking action when the user selects seats
# Handle the booking action when the user selects seats

def book_seats():
    selected_seats = request.form.get("selected_seats", "").split(",")
    movie_id = request.form.get("movie_id", "").strip()  # Strip extra spaces
    time_slot = request.form.get("time_slot", "").strip()
    screen_number = request.form.get("screen_number", "").strip()
    user_data = request.cookies.get("user_data")

    if not user_data:
        return redirect(url_for("login"))

    user_id, email = user_data.split("|")
    user_id = int(user_id)

    # Validate movie_id (ensure it's not empty and is a valid integer)
    if not movie_id or not movie_id.isdigit():
        return "Invalid movie ID", 400  # Ensure movie_id is a valid integer

    movie_id = int(movie_id)  # Convert movie_id to an integer

    if not selected_seats or selected_seats == [""]:
        return "No seats selected", 400

    db = SessionLocal()

    try:
        # Fetch seat details
        seat_details = db.query(Seat).filter_by(screen=screen_number).first()
        if not seat_details:
            return "Invalid screen number", 400

        total_price = 0
        ticket_ids = []

        for seat in selected_seats:
            existing_ticket = db.query(Ticket).filter_by(
                seat=seat, movie_id=movie_id, time_slot=time_slot, screen=screen_number
            ).first()
            if existing_ticket:
                return f"Seat {seat} is already booked", 400

            ticket = Ticket(
                screen=screen_number,
                time_slot=time_slot,
                seat=seat,
                movie_id=movie_id
            )
            db.add(ticket)
            db.commit()

            ticket_ids.append(str(ticket.ticket_id))

            if seat.startswith(("A", "B", "C", "D", "E", "F", "G", "H")):
                total_price += seat_details.luxe_price if seat[0] in ["A", "B", "C", "D"] else seat_details.luxe_prime_price


        # Create booking
        booking = Booking(
            cost=total_price,
            user_id=user_id,
            ticket_id=",".join(ticket_ids)
        )
        db.add(booking)
        db.commit()

    except Exception as e:
        db.rollback()
        return f"An error occurred: {str(e)}", 500

    finally:
        db.close()

    return redirect(url_for("home"))


def profile():
    # Read the cookie that stores "user_id|email"
    user_data = request.cookies.get('user_data')
    if not user_data:
        # If not logged in, redirect to login page.
        return redirect(url_for('login'))
    
    try:
        user_id_str, cookie_email = user_data.split('|')
        user_id = int(user_id_str)
    except Exception as e:
        print("Error parsing user_data cookie:", e)
        return redirect(url_for('login'))
    
    db = SessionLocal()
    
    # 1. Get the user details for display in the profile
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        db.close()
        return redirect(url_for('login'))
    
    # 2. Query all bookings for this user.
    bookings = db.query(Booking).filter(Booking.user_id == user_id).all()

    active_bookings = []  # Will contain bookings with show time in the future
    expired_bookings = []  # Bookings with shows already started (or passed)
    
    now = datetime.now()
    
    for booking in bookings:
        print(f"Processing booking {booking.booking_id}")
        # Get the list of ticket IDs (stored as a comma-separated string)
        ticket_ids = booking.ticket_id.split(',')
        tickets = []
        for tid in ticket_ids:
            try:
                ticket = db.query(Ticket).filter(Ticket.ticket_id == int(tid.strip())).first()
                if ticket:
                    tickets.append(ticket)
            except Exception as e:
                print(f"Error processing ticket id {tid} for booking {booking.booking_id}:", e)
                continue
        
        if not tickets:
            print(f"No tickets found for booking {booking.booking_id}")
            continue

        # We assume all tickets in a booking belong to the same show.
        first_ticket = tickets[0]

        # Get the corresponding movie details.
        movie = db.query(Movie).filter(Movie.movie_id == first_ticket.movie_id).first()
        if not movie:
            print(f"Movie not found for ticket with movie_id {first_ticket.movie_id} in booking {booking.booking_id}")
            continue


        # Parse the time slot (e.g. "10:00 AM" or "01:01") into a datetime object for today.
        try:
            time_str = first_ticket.time_slot.strip()
            if "AM" in time_str or "PM" in time_str:
                show_time = datetime.strptime(time_str, '%I:%M %p')
            else:
                show_time = datetime.strptime(time_str, '%H:%M')
            show_time = show_time.replace(year=now.year, month=now.month, day=now.day)
        except Exception as e:
            print(f"Error parsing time '{first_ticket.time_slot}' for booking {booking.booking_id}:", e)
            continue

        # Debug: print parsed show time and current time
        print(f"Booking {booking.booking_id}: Show time is {show_time}, current time is {now}")

        # Check if the show is still active (i.e. its start time is later than now)
        is_active = show_time > now
        time_remaining = show_time - now if is_active else None

        # Combine all seat numbers for this booking.
        seat_numbers = [ticket.seat for ticket in tickets]
        seats_str = ', '.join(seat_numbers)
        
        # Package the booking information in a dictionary.
        booking_info = {
            'booking_id': booking.booking_id,
            'cost': float(booking.cost),
            'movie_name': movie.name,
            'movie_id': movie.movie_id,  # for displaying the poster image
            'screen': first_ticket.screen,
            'time_slot': first_ticket.time_slot,
            'seats': seats_str,
            'time_remaining': time_remaining  # a timedelta object if active, otherwise None
        }
        
        if is_active:
            active_bookings.append(booking_info)
            print(f"Booking {booking.booking_id} is active.")
        else:
            expired_bookings.append(booking_info)
            print(f"Booking {booking.booking_id} has expired.")
    
    db.close()
    
    # Pass the user info and the two booking lists to the template.
    return render_template('profile.html',
                           user=user,
                           active_bookings=active_bookings,
                           expired_bookings=expired_bookings)


