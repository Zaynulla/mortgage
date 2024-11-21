month = int
payment = int | float


def format_thousands(num: int | float) -> str:
    return f"{num:_}".replace("_", " ")


def format_payments(one_time_payments: dict[month, payment]):
    return "\n".join(
        [
            f"\t{month:3} мес: {format_thousands(payment)}"
            for month, payment in one_time_payments.items()
        ]
    )
