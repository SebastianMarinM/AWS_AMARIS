from datetime import datetime

def get_current_partition():
    now = datetime.now()
    return {
        "year": now.year,
        "month": f"{now.month:02}",
        "day": f"{now.day:02}"
    }

def format_date(date_str, input_format="%Y-%m-%d", output_format="%d/%m/%Y"):
    try:
        return datetime.strptime(date_str, input_format).strftime(output_format)
    except Exception as e:
        return None
