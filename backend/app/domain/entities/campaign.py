from datetime import date


class Campaign:
    def __init__(
        self,
        name: str,
        description: str,
        start_date: date,
        end_date: date,
        budget: float,
        is_active: bool,
    ):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.is_active = is_active
