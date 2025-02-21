from datetime import datetime

raw_date_1 = "August 15 - 18, 2024"
raw_date_2 = "May 30 - June 2, 2024"
raw_date_3 = "Jun 29 - July 2, 2023"
def convert_dates(raw_date):
    # Break down the raw date to the individual parts
    raw_date_parts = raw_date.split(" - ")
    first_raw_date_part = raw_date_parts[0].split(" ")
    second_raw_date_part = raw_date_parts[1].split(",")

    # determine which type of date it is
    if (len(second_raw_date_part[0]) > 2):
        end_date_part = second_raw_date_part[0].split(" ")
        
        start_month = first_raw_date_part[0]
        start_day = first_raw_date_part[1]
        end_month = end_date_part[0]
        end_day = end_date_part[1]
        year = second_raw_date_part[1].strip()
    else:
        start_month = first_raw_date_part[0]
        end_month = start_month
        start_day = first_raw_date_part[1]
        end_day = second_raw_date_part[0]
        year = second_raw_date_part[1].strip()

    # Build both the start and end date objects based on format
    start_date = start_month + " " + start_day + ", " + year
    if len(start_month) > 3:
        start_original_format = "%B %d, %Y"
    else:
        start_original_format = "%b %d, %Y"
    start_date_obj = datetime.strptime(start_date, start_original_format)

    end_date = end_month + " " + end_day + ", " + year
    if len(end_month) > 3:
        end_original_format = "%B %d, %Y"
    else:
        end_original_format = "%b %d, %Y"
    end_date_obj = datetime.strptime(end_date, end_original_format)

    # Convert start and end dates to new format
    new_format = "%Y-%m-%d"
    start_date = start_date_obj.strftime(new_format)
    end_date = end_date_obj.strftime(new_format)

    return start_date, end_date

if __name__ == "__main__":
    raw_date = raw_date_3

    print(f"raw_date: {raw_date}")
    start_date, end_date = convert_dates(raw_date)

    print(f"start_date: {start_date}, end_date: {end_date}")

