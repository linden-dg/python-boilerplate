from datetime import datetime, timedelta

UNITS = {
    "s": 1,
    "milli": 1e3,
    "micro": 1e6,
    "nano": 1e9,
}


def convert_timestamp_to_datetime(timestamp: float, unit="s"):
    return datetime.fromtimestamp(float(timestamp) / UNITS[unit])


def convert_nanoseconds_to_datetime(timestamp: float):
    return convert_timestamp_to_datetime(timestamp, "nano")


def days_diff(start_datetime: datetime, end_datetime: datetime):
    return (end_datetime - start_datetime).days


def date_diff(start_datetime: datetime, end_datetime: datetime):
    return (end_datetime.date() - start_datetime.date()).days


def hours_diff(start_datetime: datetime, end_datetime: datetime):
    delta = end_datetime - start_datetime
    total_seconds = delta.days * 24 * 60 * 60 + delta.seconds
    return total_seconds / 3600


def working_hours_difference(
    start_date: datetime, end_date: datetime, working_hour_start=9, working_hour_end=17
) -> float:
    """
    Calculate the difference between two dates in working hours.

    :param start_date: Start date
    :param end_date: End date
    :param working_hour_start: Starting hour of the normal working day (e.g. 9am -> 9)
    :param working_hour_end: Ending hour of the normal working day (e.g. 5pm -> 17)
    :return: Difference in working hours
    """

    # Define working hours
    work_start_time = datetime.time(
        datetime(2000, 1, 1, working_hour_start)
    )  # Arbitrary date just to get the time
    work_end_time = datetime.time(
        datetime(2000, 1, 1, working_hour_end)
    )  # Arbitrary date just to get the time
    work_hours_per_day = abs(working_hour_end - working_hour_start)

    # Calculate the total working hours between the two dates
    total_hours = 0

    # Increment the start date until it reaches the end date
    current_date = start_date

    while current_date.date() <= end_date.date():
        # If the current date is a weekday
        if current_date.weekday() < 5:
            # If the current date is the start date
            if current_date.date() == start_date.date():
                # Calculate working hours for the start day
                work_end_today = datetime(
                    current_date.year,
                    current_date.month,
                    current_date.day,
                    work_end_time.hour,
                )
                if current_date.time() > work_end_time:
                    pass  # start time is after working hours
                elif current_date.time() <= work_start_time:
                    total_hours += work_hours_per_day
                else:
                    total_hours += (work_end_today - current_date).seconds / 3600
            # If the current date is the end date
            elif current_date.date() == end_date.date():
                # Calculate working hours for the end day
                work_start_today = datetime(
                    current_date.year,
                    current_date.month,
                    current_date.day,
                    work_start_time.hour,
                )
                if end_date.time() < work_start_time:
                    pass  # end time is before working hours
                elif end_date.time() >= work_end_time:
                    total_hours += work_hours_per_day
                else:
                    total_hours += (end_date - work_start_today).seconds / 3600.0
            # If the current date is a day between the start and end dates
            else:
                total_hours += work_hours_per_day
        # Move to the next day
        current_date += timedelta(days=1)

    return total_hours
