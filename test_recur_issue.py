from datetime import datetime, date
from pathlib import Path
from zoneinfo import ZoneInfo

import icalendar
import recurring_ical_events
import vobject

TEST_FILES = Path(__file__).parent.resolve() / 'files'


def test_recurring_ical_events():
    ical_file = TEST_FILES / 'event_recurrent_allday.ics'
    utc = ZoneInfo('UTC')

    cal: icalendar.Calendar = icalendar.Calendar.from_ical(ical_file.read_text())

    start = datetime(2024, 4, 1, tzinfo=utc)
    end = datetime(2024, 4, 17, tzinfo=utc)

    events: list[icalendar.Event] = recurring_ical_events.of(
        cal,
        keep_recurrence_attributes=False,
        components=['VJOURNAL', 'VTODO', 'VEVENT'],
    ).between(start, end)

    assert len(events) == 2

    assert events[0]['DTSTART'].dt == date(2024, 4, 8)
    assert events[0]['DTEND'].dt == date(2024, 4, 9)

    assert events[1]['DTSTART'].dt == date(2024, 4, 15)
    assert events[1]['DTEND'].dt == date(2024, 4, 16)


def test_dateutil_rrule():
    ical_file = TEST_FILES / 'event_recurrent_allday.ics'
    utc = ZoneInfo('UTC')

    cal = vobject.readOne(ical_file.read_text())
    rruleset = cal.vevent.getrruleset()

    # TypeError: can't compare offset-naive and offset-aware datetimes
    start = datetime(2024, 4, 1, tzinfo=utc)
    end = datetime(2025, 4, 17, tzinfo=utc)

    # TypeError: can't compare datetime.datetime to datetime.date
    # start = date(2024, 4, 1)
    # end = date(2025, 4, 27)

    # OK
    # start = datetime(2024, 4, 1)
    # end = datetime(2024, 4, 17)

    recurrences = rruleset.between(start, end)

    assert len(recurrences) == 2
    assert recurrences[0] == datetime(2024, 4, 8)
    assert recurrences[1] == datetime(2024, 4, 15)

