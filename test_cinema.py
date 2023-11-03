from datetime import datetime
from Screening import Screening
from Seat import Seat
from User import Customer
from Booking import Booking
from Hall import Hall
from Movie import Movie
from CinemaController import Cinema

# Test creating a customer and getting all customers
def test_create_customer_and_get_all_customers():
    cinema = Cinema("Lincoln Cinemas")
    cinema.create_customer("Dora Wang", "dora", "password")
    customers = cinema.get_all_customers()
    assert len(customers) == 1
    assert customers[0].name == "Dora Wang"

# Test creating a seat
def test_create_seat():
    seat = Seat(1, 'A', False, 10.0)
    assert seat.seatNumber == 1
    assert seat.seatColumn == 'A'
    assert not seat.isReserved
    assert seat.seatPrice == 10.0    

# Test creating a hall
def test_create_hall():
    seats = [Seat(1, 'A', False, 10.0), Seat(2, 'A', False, 10.0)]
    hall = Hall("Hall 1", 2, seats)
    assert hall.name == "Hall 1"
    assert hall.totalSeats == 2

# Test viewing a movie
def test_view_movie():
    cinema = Cinema("Lincoln Cinemas")
    cinema.add_movie("Movie 1", "Description 1", 120, "English", "2023-11-01", "USA", "Action")
    cinema.add_movie("Movie 2", "Description 2", 110, "Spanish", "2023-11-02", "Spain", "Drama")

    # Test viewing an existing movie
    movie1 = cinema.view_movie("Movie 1")
    assert movie1 is not None
    assert movie1.title == "Movie 1"

    # Test viewing a non-existing movie
    movie3 = cinema.view_movie("Movie 3")
    assert movie3 is None

# Test creating a booking
def test_create_booking():
    cinema = Cinema("Lincoln Cinemas")
    customer = Customer("Dora", "dora", "123")
    hall = Hall("Hall 1", 2, [])
    screening = Screening(datetime(2023, 11, 15), datetime(2023, 11, 15, 18, 0), datetime(2023, 11, 15, 21, 0), hall)
    seats = [Seat(1, 'A', False, 10.0), Seat(2, 'A', False, 10.0)]
    booking = cinema.create_booking(customer, screening, seats, 20.0, "Credit Card")
    assert booking is not None
    assert booking.customer == customer
    assert booking.screening == screening

# Test canceling a booking
def test_cancel_booking():
    cinema = Cinema("Lincoln Cinemas")
    customer = Customer("Dora", "dora", "123")
    hall = Hall("Hall 1", 2, [])
    screening = Screening(datetime(2023, 11, 15), datetime(2023, 11, 15, 18, 0), datetime(2023, 11, 15, 21, 0), hall)
    seats = [Seat(1, 'A', False, 10.0), Seat(2, 'A', False, 10.0)]
    booking = cinema.create_booking(customer, screening, seats, 20.0, "Credit Card")
    
    # Check if the booking was created successfully
    assert booking is not None
    assert booking.customer == customer
    assert booking.screening == screening
    
    # Attempt to cancel the booking
    result = cinema.cancel_booking(booking)
    
    # Check if the booking was canceled successfully
    assert result is True
    assert booking not in cinema.bookingList  # Ensure the booking is removed from the booking list
    assert booking not in cinema.customer_bookings.get(customer, [])  # Ensure the booking is removed from the customer's bookings

    # Check if the booked seats are now available
    for seat in seats:
        assert not seat.isReserved

# Test the getAvailableSeats function in Screening
def test_get_available_seats():
    # Create seats and Hall
    seats = [Seat(1, 'A', False, 10.0), Seat(2, 'A', False, 10.0), Seat(3, 'A', True, 10.0)]
    hall = Hall("Hall 1", 5, seats)

    # Create a screening for the hall
    screening = Screening(datetime(2023, 11, 15), datetime(2023, 11, 15, 18, 0), datetime(2023, 11, 15, 21, 0), hall)

    # Book some seats
    booked_seats = [seats[0]]

    screening.bookSeats(booked_seats)

    # Get the available seats
    available_seats = screening.getAvailableSeats()

    # Check if the available seats match the expected result
    assert len(available_seats) == 1  # There should be 1 available seats
    assert seats[0] not in available_seats
    assert seats[1] in available_seats
    assert seats[2] not in available_seats

# Test the find_booking_by_id method in the Cinema class
def test_find_booking_by_id():
    # Create a cinema
    cinema = Cinema("Lincoln Cinemas")

    # Create a customer
    customer = Customer("Dora", "dora", "123")

    # Create a booking with a unique booking ID
    unique_booking_id = 12345
    booking = Booking(customer, None, [], 0.0, "Credit Card")
    booking.bookingNum = unique_booking_id

    # Add the booking to the cinema
    cinema.bookingList.append(booking)

    # Test finding the booking by its unique booking ID
    found_booking = cinema.find_booking_by_id(unique_booking_id)

    # Check if the found booking is the same as the original booking
    assert found_booking is not None
    assert found_booking == booking

    # Test finding a non-existing booking
    non_existing_booking_id = 54321
    non_existing_booking = cinema.find_booking_by_id(non_existing_booking_id)
    assert non_existing_booking is None

    
if __name__ == "__main__":
    import test_cinema
    test_cinema.main()

