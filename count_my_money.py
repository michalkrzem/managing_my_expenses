import pandas as pd

pd.set_option('display.max_columns', None)


class BillsCounter:
    """
    Class to read, modify and create dataframe with important information
    """
    COLUMN_TO_CHECK = [
        'Unnamed: 7',
        'Unnamed: 8',
        'Unnamed: 9',
        'Unnamed: 10'
    ]
    COLUMNS_TO_DROP = [
        'Data waluty',
        'Waluta',
        'Saldo po transakcji'
    ]

    def __init__(self, filename):
        self.my_bills = None
        self.filename = filename
        self.company_name = None
        self.df = self.read_csv()
        self.drop_non_important_columns()
        self.drop_cash_inflows()

    def read_csv(self):
        self.df = pd.read_csv(self.filename, encoding='windows-1250')

        return self.df

    def drop_non_important_columns(self):
        self.df.drop(
            columns=self.COLUMNS_TO_DROP,
            inplace=True
        )

    def drop_cash_inflows(self):
        self.df.drop(self.df[self.df['Kwota'] > 0].index, inplace=True)

    def create_bills_by_company(self):
        df_by_company_name = self.df[
            self.COLUMN_TO_CHECK
        ].apply(
            lambda x: x.str.contains(self.company_name, case=False)
        )
        company_costs = self.df[df_by_company_name.any(axis=1)]

        return company_costs

    def create_my_bills_df(self):
        company_costs = self.create_bills_by_company()
        self.my_bills = pd.DataFrame(
            {
                'date': company_costs['Data operacji'],
                'category': self.company_name,
                'price': company_costs['Kwota']
            }
        )

        return self.my_bills
