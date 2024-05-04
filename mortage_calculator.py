# %%
import pandas as pd


# %%
def calculate_monthly_payment(
    total_amount, down_payment, interest_rate, amortization_period
):
    total_amount = float(total_amount)
    amortization_period = int(amortization_period)
    down_payment = float(down_payment)
    interest_rate = float(interest_rate)
    total_amount -= down_payment
    if (interest_rate > 0) and (amortization_period > 0):
        monthly_interest_rate = interest_rate / 12
        payment = (
            total_amount
            * (
                monthly_interest_rate
                * (1 + monthly_interest_rate) ** amortization_period
            )
            / ((1 + monthly_interest_rate) ** amortization_period - 1)
        )
        return payment
    return 0


def generate_mortgage_schedule(
    total_amount, down_payment, interest_rate, amortization_period
):
    total_amount = float(total_amount)
    amortization_period = int(amortization_period) * 12
    down_payment = float(down_payment)
    interest_rate = float(interest_rate)

    monthly_payment = calculate_monthly_payment(
        total_amount, down_payment, interest_rate, amortization_period
    )
    remaining_balance = total_amount - down_payment
    mortgage_schedule = []

    for month in range(1, amortization_period + 1):
        interest_payment = remaining_balance * (interest_rate / 12)
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment

        mortgage_schedule.append(
            {
                "Month": month,
                "Principal Payment": principal_payment,
                "Interest Payment": interest_payment,
                "Total Payment": monthly_payment,
                "Remaining Balance": remaining_balance,
            }
        )

    return mortgage_schedule


# %%
data = generate_mortgage_schedule(
    total_amount=11_000_000,
    down_payment=5_000_000,
    interest_rate=0.183,
    amortization_period=7,
)

df = pd.DataFrame(data)
df

# %%
