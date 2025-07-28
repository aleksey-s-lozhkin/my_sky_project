def mask_account_card():


    pass


def get_date(date_str: str) -> str:


    from datetime import datetime

    dt = datetime.fromisoformat(date_str)
    return dt.strftime('%D.%m.%y')