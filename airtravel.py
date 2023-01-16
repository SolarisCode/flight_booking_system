"""The module is for creating flights, adding aircraft types and inforramtion,
    adding passengers or relocate them and printing boarding passes.
"""


class Flight:
    """A flight with a particular passenger aircraft."""

    def __init__(self, number, aircarft):
        if not number[:2].isalpha():
            raise ValueError(f"No Airline code in {number}")

        if not number[:2].isupper():
            raise ValueError(f"Invalid Airline code in {number}")

        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError(f"Invalid route number {number}")

        self._number = number
        self._aircraft = aircarft
        self._registration = self._aircraft.registration()
        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + [{letter: None
                                   for letter in seats} for _ in rows]

    def number(self):
        return (self._number)

    def aircraft_model(self):
        return (self._aircraft.model())

    def airline(self):
        return (self._number[:2])

    def registration(self):
        return (self._registration)

    def allocate_seat(self, seat, passenger):
        """Allocate a seat to a passenger.
        
        Args:
            seat: A seat designator such as '12a'.
            passenger: The passenger name.
            
        Raises:
            ValueError: If the seat in unavailable.
        """
        row, letter = self._parse_seat(seat)

        if self._seating[row][letter] is not None:
            raise ValueError(f"Seat {seat} is already occupied")

        self._seating[row][letter] = passenger

    def _parse_seat(self, seat):
        rows, seat_letters = self._aircraft.seating_plan()
        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError(f"Invalid seat letter {letter}")

        row_txt = seat[:-1]
        try:
            row = int(row_txt)
        except ValueError:
            raise ValueError(f"Invalid seat row {row_txt}")

        if row not in rows:
            raise ValueError(f"Invalid row number {row}")

        return (row, letter)

    def relocate_passenger(self, from_seat, to_seat):
        """Realocate a passenger to a different seat.
        
        Args:
            from_seat: The current occupied seat.
            to_seat: The new seat to move to.
        """
        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError(f"Seat {to_seat} is already occupied")

        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError(f"No passenger to relocate in seat {from_seat}")

        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def num_availabe_seats(self):
        return (sum(
            sum(1 for x in row.values() if x is None) for row in self._seating
            if row is not None))

    def make_boarding_card(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(), self.aircraft_model())

    def _passenger_seats(self):
        number_rows, seat_letters = self._aircraft.seating_plan()
        for row in number_rows:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield (passenger, f"{row}{letter}")

class Aircraft:
    
    def __init__(self, registration):
        self._registration = registration

    def registration(self):
        return (self._registration)
    
    def num_seats(self):
        rows, row_seats = self.seating_plan()
        return (len(rows) * len(row_seats))


class Airbus319(Aircraft):
    
    def model(self):
        return ("Airbus A319")

    def seating_plan(self):
        return (range(1, 23), "ABCDEF")


class Boeing777(Aircraft):
    # For simplicity's sake, we ignore complex
    # seating arrangement for first_class

    def model(self):
        return ("Boeing 777")

    def seating_plan(self):
        return (range(1, 56), "ABCDEGHJK")
    
    
class AircraftGeneral:

    def __init__(self, registration, model, num_rows, num_seats_per_row):
        self._registration = registration
        self._model = model
        if num_rows < 0:
            raise ValueError(f"Invalid row number {num_rows}")
        self._num_rows = num_rows
        self._num_seats_per_row = num_seats_per_row

    def registration(self):
        return (self._registration)

    def model(self):
        return (self._model)

    def seating_plan(self):
        return ((range(1, self._num_rows + 1),
                 "ABCDEFGHJK"[:self._num_seats_per_row]))


def boarding_card_printer(passenger, seat, flight_number, aircraft):
    output = f"| Name: {passenger}"        \
            f" Flight: {flight_number}"    \
            f" Seat: {seat}"                \
            f" Aircraft: {aircraft} |"
    banner = "+" + "-" * (len(output) - 2) + "+"
    border = "|" + " " * (len(output) - 2) + "|"
    line = [banner, border, output, border, banner]
    card = "\n".join(line)
    print(card)
    print()

def make_flight():
    f = Flight("EK973", AircraftGeneral("EK-ARE", "Airbus A380", \
                                 num_rows=22, num_seats_per_row=6))
    f.allocate_seat("1A", "Mohammed Elkholy")
    f.allocate_seat("1B", "Leen Hito")
    f.allocate_seat("2A", "Ahmed Maher")
    f.allocate_seat("22A", "Guido Van Rossum")
    f.allocate_seat("22B", "Andres Heljsberg")
    f.allocate_seat("11A", "John McCarthy")
    return (f)

def generate_flights():
    a = Flight("EK231", Airbus319("EK-YGH"))
    a.allocate_seat("1A", "Mohammed Elkholy")
    a.allocate_seat("1B", "Leen Hito")
    a.allocate_seat("2A", "Ahmed Maher")
    a.allocate_seat("22A", "Guido Van Rossum")
    a.allocate_seat("22B", "Andres Heljsberg")
    a.allocate_seat("11A", "John McCarthy")

    b = Flight("EK973", Boeing777("EK-EDO"))
    b.allocate_seat("1A", "Mohammed Elkholy")
    b.allocate_seat("1B", "Leen Hito")
    b.allocate_seat("2A", "Ahmed Maher")
    b.allocate_seat("22A", "Guido Van Rossum")
    b.allocate_seat("22B", "Andres Heljsberg")
    b.allocate_seat("11A", "John McCarthy")
    return (a, b)