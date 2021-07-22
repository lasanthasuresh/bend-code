from datetime import datetime


def to_epoch_date(date_srt):
    utc_time = datetime.strptime(date_srt, "%Y-%m-%d")
    return (utc_time - datetime(1970, 1, 1)).total_seconds()*1000
