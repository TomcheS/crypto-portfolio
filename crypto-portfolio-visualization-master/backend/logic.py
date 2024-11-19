
from datetime import datetime
from dataclasses import dataclass
import datetime

# * Transaction Types
BOUGHT = 1
SOLD = 0


@dataclass(frozen=True)
class Transaction:
    id: int
    name: str
    symbol: str
    type: int
    amount: int
    time_transacted: datetime
    time_created: datetime
    price_purchased_at: float
    no_of_coins: float


def format_db_row_to_transaction(row):
    return Transaction(
        id=row[0],
        name=row[1],
        symbol=row[2],
        type=row[3],
        amount=row[4]/100,
        time_transacted=row[5].strftime("%Y/%m/%d"),
        time_created=row[6].strftime("%Y/%m/%d"),
        price_purchased_at=float(row[7]),
        no_of_coins=float(row[8])
    )
