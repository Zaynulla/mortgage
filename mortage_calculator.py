# https://vc.ru/money/716629-kak-rasschityvayutsya-dosrochnye-platezhi-po-ipoteke-vyvod-formul?ysclid=lvsap23zg1652408946
# %%
from dataclasses import dataclass, replace
from math import ceil, log

import pandas as pd
from IPython.display import display


# %%
class NotEnoughActualMonthlyPayment(Exception):
    pass


# %%
# https://pandas.pydata.org/pandas-docs/stable/user_guide/copy_on_write.html
pd.options.mode.copy_on_write = True


# %%
@dataclass
class MortageConditions:
    total_amount: int
    initial_payment: int
    annual_interest_rate: float
    amortization_period_years: int
    actual_monthly_payment: int
    occasional_payments_reducing_period: dict[int, int]

    def __str__(self) -> str:
        occasional_payments_reducing_period_str = "\n".join(
            [
                f"\t{month:3} мес: {payment:6}"
                for month, payment in self.occasional_payments_reducing_period.items()
            ]
        )
        return "\n".join(
            [
                f"Общая сумма {self.total_amount}",
                f"Первоначальный взнос {self.initial_payment}",
                f"Процентная ставка {self.annual_interest_rate}",
                f"Начальный срок ипотеки {self.amortization_period_years}",
                f"Планируемые ежемесячный платеж {self.actual_monthly_payment}",
                (
                    "Планируемые разовые платежи:\n"
                    f"{occasional_payments_reducing_period_str}"
                ),
            ]
        )


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


def generate_mortgage_schedule(data: MortageConditions):
    amortization_period_months = data.amortization_period_years * 12
    monthly_interest_rate = data.annual_interest_rate / 12

    remaining_balance = data.total_amount - data.initial_payment
    mortgage_schedule = []

    month = 0
    while remaining_balance > 1:  # пока долг больше 1 рубля
        month += 1
        interest_payment = remaining_balance * monthly_interest_rate

        principal_payment = data.actual_monthly_payment - interest_payment
        principal_payment += occasional_payments_reducing_period.get(month, 0)
        principal_payment = min(principal_payment, remaining_balance)

        remaining_balance -= principal_payment

        required_monthly_payment = calculate_monthly_payment(
            remaining_balance=remaining_balance,
            monthly_interest_rate=monthly_interest_rate,
            amortization_period_months=amortization_period_months,
        )

        if principal_payment < 0:
            msg = f"Требуемый платеж {required_monthly_payment}"
            raise NotEnoughActualMonthlyPayment(msg)

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
def calc_mortage_duration(payments_schedule_data: dict):
    df = pd.DataFrame(payments_schedule_data)

    actual_years = df.shape[0] / 12
    full_years = int(actual_years)
    months = int((actual_years - full_years) * 12)

    return actual_years, months


# %%
def print_mortage_main_info(mortage_conditions: MortageConditions):
    data = generate_mortgage_schedule(mortage_conditions)

    actual_years, months = calc_mortage_duration(data)
    print(f"Ипотека будет выплачена за {int(actual_years)} лет {months} мес.")
    print(mortage_conditions)

    df = pd.DataFrame(data)
    df_1 = df[["Month", "Required monthly payment"]]
    df_1 = df_1[df_1["Month"] % 12 == 0]
    df_1["Full years"] = df_1["Month"] // 12
    df_1["Required monthly payment"] = df_1["Required monthly payment"].astype(int)
    df_1 = df_1[["Full years", "Required monthly payment"]]
    display(df_1.style.hide(axis="index"))


# %%
print("Базовая вторичка")

occasional_payments_reducing_period = {
    # month_num: amount
    7: 520_000,
}

cheap_ugly_second_hand = MortageConditions(
    total_amount=11_000_000,
    initial_payment=5_000_000,
    annual_interest_rate=0.164,
    amortization_period_years=30,
    actual_monthly_payment=130_000,
    occasional_payments_reducing_period=occasional_payments_reducing_period,
)

print_mortage_main_info(cheap_ugly_second_hand)

# %%
print("Приличная вторичка")
luxury_price = 14_500_000
well_enough_second_hand_immediately = replace(
    cheap_ugly_second_hand, total_amount=luxury_price
)
print_mortage_main_info(well_enough_second_hand_immediately)

# %%
print("Приличная вторичка после продажи базовой вторички")
initial_payment = cheap_ugly_second_hand.total_amount
well_enough_after_ugly = replace(
    well_enough_second_hand_immediately,
    initial_payment=initial_payment,
    occasional_payments_reducing_period={},  # на втором этапе не получаем льготу
)
print_mortage_main_info(well_enough_after_ugly)

# %%
