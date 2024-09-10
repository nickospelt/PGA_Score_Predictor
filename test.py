from datetime import datetime

raw_date = "August 15 - 18, 2024"
def convert_dates(raw_date):
    # Break down the raw date to the individual parts
    raw_date_parts = raw_date.split(" - ")
    first_raw_date_part = raw_date_parts[0].split(" ")
    second_raw_date_part = raw_date_parts[1].split(",")
    month = first_raw_date_part[0]
    start_day = first_raw_date_part[1]
    end_day = second_raw_date_part[0]
    year = second_raw_date_part[1].strip()

    # Build both the start and end date
    start_date = month + " " + start_day + ", " + year
    end_date = month + " " + end_day + ", " + year

    # Convert start and end dates to new format
    original_format = "%B %d, %Y"
    start_date_obj = datetime.strptime(start_date, original_format)
    end_date_obj = datetime.strptime(end_date, original_format)

    new_format = "%Y-%m-%d"
    start_date = start_date_obj.strftime(new_format)
    end_date = end_date_obj.strftime(new_format)

    return start_date, end_date

if __name__ == "__main__":
    raw_date = "August 15 - 18, 2024"

    print(f"raw_date: {raw_date}")
    start_date, end_date = convert_dates(raw_date)

    print(f"start_date: {start_date}, end_date: {end_date}")

