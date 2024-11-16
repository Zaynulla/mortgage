# https://vc.ru/money/716629-kak-rasschityvayutsya-dosrochnye-platezhi-po-ipoteke-vyvod-formul?ysclid=lvsap23zg1652408946
# %%
from dataclasses import replace

import pandas as pd

from utils import MortageConditions, print_mortage_main_info

# %%
# https://pandas.pydata.org/pandas-docs/stable/user_guide/copy_on_write.html
pd.options.mode.copy_on_write = True


# %%
print("Базовая вторичка")

cheap_ugly_second_hand = MortageConditions(
    total_amount=11_000_000,
    initial_payment=5_000_000,
    annual_interest_rate=0.164,
    amortization_period_years=30,
    actual_monthly_payment=130_000,
    occasional_payments_reducing_period={7: 520_000},
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
print("IT-ипотека")
it_mortgage_slavery = replace(
    cheap_ugly_second_hand,
    total_amount=20_000_000,
    annual_interest_rate=0.046,
    actual_monthly_payment=130_000,
)
print_mortage_main_info(it_mortgage_slavery)


# %%
