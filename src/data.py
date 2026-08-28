# Grab data
# Include class variables for data type
# Allow for pulling data at a specific date

from datetime import datetime as dt
from schwab.auth import easy_client
from schwab.client import Client
from schwab.streaming import StreamClient

class AssetData():
    def __init__(self, ticker='AAPL', timezone='America/New_York'):
        self.ticker = ticker.upper()
        self.timezone = timezone

    @classmethod
    def auth_client(cls, api_key, app_secret, callback_url, token_path='/tmp/token.json'):
        cls.client = easy_client(
                api_key = api_key,
                app_secret = app_secret,
                callback_url = callback_url,
                token_path = token_path
        )

    
    def fetch_data(self, start_date=dt.today(), end_date=dt.today(), side='c', strike_count=20,
                  ):
        contract_type = 'CALL' if side.lower() == 'c' else 'PUT'
        return self.client.get_option_chain(
                symbol = self.ticker,
                contract_type = self.client.Options.ContractType(contract_type),
                strike_count = strike_count,
                include_underlying_quote = True,
                from_date = dt.strptime(start_date, '%Y-%m-%d'),
                to_date = dt.strptime(end_date, '%Y-%m-%d')
                ).json()
        raise ValueError(f'Invalid option {side}!')
        
