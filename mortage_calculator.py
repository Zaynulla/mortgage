# https://vc.ru/money/716629-kak-rasschityvayutsya-dosrochnye-platezhi-po-ipoteke-vyvod-formul?ysclid=lvsap23zg1652408946
# %%
from math import ceil, log

import pandas as pd


# %%
def calculate_monthly_payment(
    remaining_balance,
    monthly_interest_rate,
    amortization_period_months,
):
    remaining_balance = float(remaining_balance)
    amortization_period_months = int(amortization_period_months)
    monthly_interest_rate = float(monthly_interest_rate)

    if (monthly_interest_rate > 0) and (amortization_period_months > 0):
        payment = (
            remaining_balance
            * (
                monthly_interest_rate
                * (1 + monthly_interest_rate) ** amortization_period_months
            )
            / ((1 + monthly_interest_rate) ** amortization_period_months - 1)
        )
        return payment
    return 0


def calculate_new_amortization_period(
    monthly_interest_rate, monthly_payment, remaining_balance
) -> int:
    monthly_interest_rate = float(monthly_interest_rate)
    monthly_payment = float(monthly_payment)
    remaining_balance = float(remaining_balance)

    return ceil(
        log(
            monthly_payment
            / (monthly_payment - monthly_interest_rate * remaining_balance),
            1 + monthly_interest_rate,
        )
    )


def generate_mortgage_schedule(
    total_amount,
    initial_payment,
    annual_interest_rate,
    amortization_period_years,
    actual_monthly_payment,
    occasional_payments_reducing_period: dict,
):
    total_amount = float(total_amount)
    amortization_period_months = int(amortization_period_years) * 12
    initial_payment = float(initial_payment)
    annual_interest_rate = float(annual_interest_rate)

    monthly_interest_rate = annual_interest_rate / 12

    remaining_balance = total_amount - initial_payment
    mortgage_schedule = []

    month = 0
    while remaining_balance > 1:  # пока долг больше 1 рубля
        month += 1
        interest_payment = remaining_balance * monthly_interest_rate

        principal_payment = actual_monthly_payment - interest_payment
        principal_payment += occasional_payments_reducing_period.get(month, 0)
        principal_payment = min(principal_payment, remaining_balance)

        remaining_balance -= principal_payment

        required_monthly_payment = calculate_monthly_payment(
            remaining_balance=remaining_balance,
            monthly_interest_rate=monthly_interest_rate,
            amortization_period_months=amortization_period_months,
        )

        # Обрабатываем разовые платежи
        if month in occasional_payments_reducing_period:
            amortization_period_months = month + calculate_new_amortization_period(
                monthly_interest_rate=monthly_interest_rate,
                monthly_payment=required_monthly_payment,
                remaining_balance=remaining_balance,
            )

        mortgage_schedule.append(
            {
                "Month": month,
                "Principal payment": principal_payment,
                "Interest payment": interest_payment,
                "Total payment": principal_payment + interest_payment,
                "Required monthly payment": required_monthly_payment,
                "Remaining balance": remaining_balance,
            }
        )

    return mortgage_schedule


# %%
occasional_payments_reducing_period = {
    7: 520_000,
}
# month_num: amount

data = generate_mortgage_schedule(
    total_amount=11_000_000,
    initial_payment=5_000_000,
    annual_interest_rate=0.20,
    amortization_period_years=30,
    actual_monthly_payment=130_000,
    occasional_payments_reducing_period=occasional_payments_reducing_period,
)

df = pd.DataFrame(data)
df

# %%
actual_years = df.shape[0] / 12
full_years = int(actual_years)
months = int((actual_years - full_years) * 12)
print(f"Ипотека будет выплачена за {int(actual_years)} лет {months} мес.")

# %%
df_1 = df[["Month", "Required monthly payment"]]
df_1["Rounded required payment"] = df["Required monthly payment"] / 10_000
df_1["Rounded required payment"] = df_1["Rounded required payment"].astype(int) * 10_000
df_1["Month/Year"] = df["Month"].apply(lambda m: f"{m-int(m/12)*12:02}/{int(m/12)}")
df_1.drop(columns=["Required monthly payment", "Month"], inplace=True)
df_1.groupby("Rounded required payment").agg("min").sort_values(
    by=["Rounded required payment"], ascending=False
)
