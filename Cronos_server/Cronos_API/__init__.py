# minutes
# =============================================================================

MINUTES_RANGE = [str(i) for i in range(0, 60)]
EVERY_MINUTES_RANGE = [f'*/{i}' for i in range(5, 60, 5)]
MINUTES_ALLOWED_MSG = "Only numbers from 0 to 59 or intervals of 5 (*/5 to */55) are allowed."

# hours
# =============================================================================

HOURS_RANGE = [str(i) for i in range(0, 24)]
EVERY_HOURS_RANGE = [f'*/{i}' for i in range(1, 24)]
HOURS_ALLOWED_MSG = "Only numbers from 0 to 23 or */1 to */23 are allowed."

# day of month
# =============================================================================

DAY_OF_MONTH_RANGE = [str(i) for i in range(1, 32)]
EVERY_DAY_OF_MONTH_RANGE = [f'*/{i}' for i in range(1, 32)]
DAY_OF_MONTH_ALLOWED_MSG = "Only numbers from 1 to 31 or */1 to */31 are allowed."
DAY_OF_MONTH_ERROR_MSG = "You set '{day_of_month}' to 'day_of_month', then 'day_of_week' must be set to '*'"


# months
# =============================================================================

MONTHS_RANGE = [str(i) for i in range(1, 13)]
EVERY_MONTHS_RANGE = [f'*/{i}' for i in range(1, 13)]
MONTHS_ALLOWED_MSG = "Only numbers from 1 to 12 or */1 to */12 are allowed."

# day od week
# =============================================================================

DAY_OF_WEEK_RANGE = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
EVERY_DAY_OF_WEEK_RANGE = [f'*/{i}' for i in range(1, 8)]
DAY_OF_WEEK_ALLOWED_MSG = "Only mon, tue, wed, thu, fri, sat, sun or */1 to */7 are allowed."
DAY_OF_WEEK_ERROR_MSG = "You set '{day_of_week}' to 'day_of_week', then 'months' and 'day_of_month' must be set to '*'"


# command
# =============================================================================

ALLOWED_COMMANDS = ['open', 'ls']
COMMANDS_ALLOWED_MSG = f"Command allowed : {' - '.join(ALLOWED_COMMANDS)}"