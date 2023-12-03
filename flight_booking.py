import re

class FlightBooking:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = 1
        self.departure_city = None
        self.arrival_city = None
        self.departure_date = None
        self.return_date = None

    def respond(self, message):
        if self.state == 1:
            match = re.search('flight from (\w+) to (\w+)', message)
            if match:
                self.departure_city = match.group(1)
                self.arrival_city = match.group(2)
                self.state = 2
                return 'What is your departure date?'
            else:
                return 'I did not understand. Can you please specify your departure and arrival cities?'

        elif self.state == 2:
            self.departure_date = message
            self.state = 3
            return 'Do you want a return flight?'

        elif self.state == 3:
            if 'yes' in message:
                self.state = 4
                return 'What is your return date?'
            else:
                return self.book_flight()

        elif self.state == 4:
            self.return_date = message
            return self.book_flight()

    def book_flight(self):
        sql_query = f"SELECT * FROM flights WHERE departure_city='{self.departure_city}' AND arrival_city='{self.arrival_city}' AND departure_date='{self.departure_date}'"
        if self.return_date:
            sql_query += f" AND return_date='{self.return_date}'"
        self.reset()
        return f'Your flight is being booked. Please click [HERE](http://example.com/book?query={sql_query}) to confirm.'

booking = FlightBooking()

while True:
    message = input('You: ')
    response = booking.respond(message)
    print('Bot:', response)