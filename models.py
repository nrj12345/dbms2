from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

# Database connection details
DATABASE_URL = f"postgresql://root:12345678@localhost:5432/test1"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), nullable=True)
    password = Column(String(256), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    genre = Column(String(100), nullable=False)  # Store as comma-separated values
    time_slots = Column(String(255), nullable=False)  # Store as comma-separated values
    screen = Column(String(50), nullable=False)  # Screen number


class Seat(Base):
    __tablename__ = 'seats'

    screen = Column(Integer, primary_key=True, nullable=False)
    luxe_price = Column(Integer, nullable=False)
    luxe_prime_price = Column(Integer, nullable=False)

class Ticket(Base):
    __tablename__ = 'tickets'

    ticket_id = Column(Integer, primary_key=True)
    screen = Column(String(50), nullable=False)
    time_slot = Column(String(20), nullable=False)
    seat = Column(String(10), nullable=False)
    movie_id = Column(Integer, nullable=False)

class Booking(Base):
    __tablename__ = 'booking'

    booking_id = Column(Integer, primary_key=True)
    cost = Column(Numeric(10, 2), nullable=False)
    user_id = Column(Integer, nullable=False)
    ticket_id = Column(String, nullable=False)  # Stores ticket IDs as a comma-separated string

# Create tables in the database
Base.metadata.create_all(bind=engine)

