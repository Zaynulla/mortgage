# %%
from dataclasses import replace

import pandas as pd

from mortgage import Mortgage

# %%
# https://pandas.pydata.org/pandas-docs/stable/user_guide/copy_on_write.html
pd.options.mode.copy_on_write = True


# %%
print("Базовая вторичка")
cheap_ugly_second_hand = Mortgage(
    property_cost=10_000_000,
    initial_payment=5_000_000,
    annual_interest_rate_percent=15.0,
    amortization_period_years=30,
    actual_monthly_payment=100_000,
    payments_reducing_payment={7: 520_000},
    # payments_reducing_duration={7: 520_000},
)
cheap_ugly_second_hand.print_mortgage_main_info()


# %%
print("Приличная вторичка")
well_enough_second_hand = replace(
    cheap_ugly_second_hand,
    property_cost=13_000_000,
)
well_enough_second_hand.print_mortgage_main_info()


# %%
print("Приличная вторичка после продажи базовой вторички")
well_enough_after_ugly = replace(
    well_enough_second_hand,
    initial_payment=cheap_ugly_second_hand.property_cost,
    payments_reducing_payment={},  # на втором этапе не получаем льготу
)
well_enough_after_ugly.print_mortgage_main_info()


# %%
print("IT-ипотека")
it_mortgage_slavery = replace(
    cheap_ugly_second_hand,
    property_cost=20_000_000,
    annual_interest_rate_percent=4.6,
)
it_mortgage_slavery.print_mortgage_main_info()


# %%
