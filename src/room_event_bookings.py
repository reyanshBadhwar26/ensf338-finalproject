from bisect import bisect_left
from datetime import datetime, date, time, timedelta
from typing import Dict, List, Optional, Tuple

#Bonus Part
from booking_avl import BookingAVLTree
import room

class Booking:
    def __init__(self, room: str, event_date: date, start_time: time, end_time: time, event_name: str):
        self.room = room
        self.event_date = event_date
        self.start_time = start_time
        self.end_time = end_time
        self.event_name = event_name

    def __repr__(self):
        return (
            f"Booking(room='{self.room}', date={self.event_date}, "
            f"{self.start_time}-{self.end_time}, '{self.event_name}')"
        )

    def overlaps(self, other: 'Booking') -> bool:
        if self.event_date != other.event_date or self.room != other.room:
            return False
        return not (self.end_time <= other.start_time or other.end_time <= self.start_time)


class RoomEventBookings:
    def __init__(self):
        # All bookings for a day, kept sorted by time.
        self.bookings_by_day: Dict[date, List[Booking]] = {}
        # Bookings for each room on each day, also kept sorted by time.
        self.bookings_by_room_day: Dict[date, Dict[str, List[Booking]]] = {}
        # Exact lookup by room, date, and start time.
        self.booking_index: Dict[Tuple[str, date, time], Booking] = {}
        # Dates are kept sorted so we can jump to the next upcoming day efficiently.
        self.sorted_dates: List[date] = []

        # Bonus 2.7 balanced index
        self.avl_index = BookingAVLTree()

    def _booking_sort_key(self, booking: Booking) -> Tuple[time, str, time, str]:
        return (booking.start_time, booking.room, booking.end_time, booking.event_name)

    def _insert_sorted(self, items: List[Booking], booking: Booking) -> None:
        keys = [self._booking_sort_key(item) for item in items]
        index = bisect_left(keys, self._booking_sort_key(booking))
        items.insert(index, booking)

    def _remove_from_list(self, items: List[Booking], booking: Booking) -> bool:
        for i, item in enumerate(items):
            if (
                item.room == booking.room
                and item.event_date == booking.event_date
                and item.start_time == booking.start_time
                and item.end_time == booking.end_time
                and item.event_name == booking.event_name
            ):
                del items[i]
                return True
        return False

    def add_booking(self, booking: Booking) -> bool:
        exact_key = (booking.room, booking.event_date, booking.start_time)
        if exact_key in self.booking_index:
            return False

        day_rooms = self.bookings_by_room_day.setdefault(booking.event_date, {})
        room_bookings = day_rooms.setdefault(booking.room, [])

        insert_pos = bisect_left(
            [self._booking_sort_key(item) for item in room_bookings],
            self._booking_sort_key(booking),
        )

        if insert_pos > 0 and room_bookings[insert_pos - 1].overlaps(booking):
            return False
        if insert_pos < len(room_bookings) and room_bookings[insert_pos].overlaps(booking):
            return False

        self._insert_sorted(room_bookings, booking)
        day_bookings = self.bookings_by_day.setdefault(booking.event_date, [])
        self._insert_sorted(day_bookings, booking)
        self.booking_index[exact_key] = booking

        if booking.event_date not in self.sorted_dates:
            date_index = bisect_left(self.sorted_dates, booking.event_date)
            self.sorted_dates.insert(date_index, booking.event_date)

        # Bonus 2.7
        self.avl_index.insert(booking)

        return True

    def remove_booking(self, room: str, event_date: date, start_time: time) -> bool:
        exact_key = (room, event_date, start_time)
        booking = self.booking_index.get(exact_key)
        if booking is None:
            return False

        day_rooms = self.bookings_by_room_day.get(event_date)
        if day_rooms is not None:
            room_bookings = day_rooms.get(room)
            if room_bookings is not None:
                self._remove_from_list(room_bookings, booking)
                if not room_bookings:
                    del day_rooms[room]
            if not day_rooms:
                del self.bookings_by_room_day[event_date]

        day_bookings = self.bookings_by_day.get(event_date)
        if day_bookings is not None:
            self._remove_from_list(day_bookings, booking)
            if not day_bookings:
                del self.bookings_by_day[event_date]
                date_index = bisect_left(self.sorted_dates, event_date)
                if date_index < len(self.sorted_dates) and self.sorted_dates[date_index] == event_date:
                    del self.sorted_dates[date_index]

        del self.booking_index[exact_key]

        # Bonus 2.7
        self.avl_index.delete(event_date, start_time, room)

        return True

    def get_booking(self, room: str, event_date: date, start_time: time) -> Optional[Booking]:
        return self.booking_index.get((room, event_date, start_time))

    #Bonus 2.7
    def get_booking_avl(self, room: str, event_date: date, start_time: time):
        return self.avl_index.search(event_date, start_time, room)

    def get_events_in_time_range(self, event_date: date, start_time: time, end_time: time) -> List[Booking]:
        if event_date not in self.bookings_by_day:
            return []

        events = []
        for booking in self.bookings_by_day[event_date]:
            if not (booking.end_time <= start_time or booking.start_time >= end_time):
                events.append(booking)
        return events

    def get_events_on_day(self, event_date: date) -> List[Booking]:
        return list(self.bookings_by_day.get(event_date, []))

    def get_next_upcoming_event(self, current_datetime: datetime) -> Optional[Booking]:
        if not self.sorted_dates:
            return None

        current_date = current_datetime.date()
        current_time = current_datetime.time()

        date_index = bisect_left(self.sorted_dates, current_date)
        while date_index < len(self.sorted_dates):
            event_date = self.sorted_dates[date_index]
            day_bookings = self.bookings_by_day[event_date]

            if event_date > current_date:
                return day_bookings[0] if day_bookings else None

            times = [booking.start_time for booking in day_bookings]
            booking_index = bisect_left(times, current_time)
            if booking_index < len(day_bookings):
                return day_bookings[booking_index]

            date_index += 1

        return None


if __name__ == "__main__":
    system = RoomEventBookings()

    rooms = ["Room101", "Room102", "Room103", "Auditorium", "Lab1"]
    base_date = date.today()
    created = 0

    for day_offset in range(20):
        event_date = base_date + timedelta(days=day_offset)
        for room_index, room in enumerate(rooms):
            start_hour = 8 + room_index * 2
            start_time = time(start_hour, 0)
            end_time = time(start_hour + 1, 0)
            event_name = f"Event {created + 1}"
            booking = Booking(room, event_date, start_time, end_time, event_name)
            if system.add_booking(booking):
                created += 1

    print(f"Added {created} bookings.")

    today = date.today()
    events_today = system.get_events_on_day(today)
    print(f"Events today: {len(events_today)}")

    sample_booking = system.get_booking("Room101", today, time(8, 0))
    print(f"Retrieved booking: {sample_booking}")

    removed = system.remove_booking("Room101", today, time(8, 0))
    print(f"Removed booking: {removed}")

    now = datetime.now()
    next_event = system.get_next_upcoming_event(now)
    print(f"Next event: {next_event}")

    range_events = system.get_events_in_time_range(today, time(10, 0), time(14, 0))
    print(f"Events between 10AM-2PM today: {len(range_events)}")
