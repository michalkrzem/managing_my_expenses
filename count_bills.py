import pandas as pd

from count_my_money import BillsCounter

runner = True
companies = {}
filename = input("Podaj nazwę pliku razem z rozszerzeniem ")

while runner:
    key = input(
        "Co chcesz sprawdzić? Będzie to opis w wynikowym pliku. "
        "Np. jeśli chcesz sprawdzić koszty tankowania na stacji, "
        "możesz podać: tankowanie: "
    )
    value = input(
        "Jaki sklep sprawdzić? Możesz podawać kilka sklepów używając znaku | "
        "np.: Orlen|shell|bp|lotos  "
    )

    companies.update({
        key: value,
    })

    what_to_do = input("Czy chcesz dodać kolejny wydatek? T/N ")
    if what_to_do.upper() == 'N':
        runner = False

sum_by_company_df = pd.DataFrame({'wydatek': [], 'kwota': []})
calculator = BillsCounter(filename=filename)


for company in companies:
    calculator.company_name = companies[company]
    calculator.create_my_bills_df()
    sum_by_company = calculator.my_bills['price'].sum()
    sum_by_company_df = pd.concat(
        [
            sum_by_company_df,
            pd.DataFrame(
                [{
                    'wydatek': company,
                    'kwota': round(sum_by_company, 2)
                }],

            )
        ],
        ignore_index=True
    )

sum_by_company_df = pd.concat(
    [
        sum_by_company_df,
        pd.DataFrame(
            [{
                'wydatek': 'PODSUMOWANIE',
                'kwota': round(sum_by_company_df['kwota'].sum(), 2)
            }]
        )
    ],
    ignore_index=True
)

sum_by_company_df.to_csv(f'sum_of_{filename}', index=False)
