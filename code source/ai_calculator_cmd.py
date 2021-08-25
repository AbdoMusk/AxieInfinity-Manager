import requests
import json
from time import time
import pyperclip


class CurrencyExchanger:
    def __init__(self, force_update=False):
        """
        :param force_update: (for development only) force 'currency_conversion_rate' file to update, without waiting it to expire.
        """
        self.expiration_time = 2  # hours
        self.force_update = force_update
        try:
            with open('currency_conversion_rate.json', 'r+') as currency_file:
                self.conversion_rate = json.load(currency_file)
            if time() - self.conversion_rate['last_updated'] >= self.expiration_time*60*60 or self.force_update:
                self.update_conversion_rate()
        except:
            print('Currency Conversion Rate File Not Found')
            self.update_conversion_rate()

    @property
    def get_currency_rate(self):
        return self.conversion_rate

    def update_conversion_rate(self):
        print(f'({self.expiration_time} Hours) conversion_rate_file life time is expired, Updating conversion rate ... | Force Update {self.force_update}.')
        # It is recommended to get your own API key from website 'exchangerate-api.com', because of request limit.
        currency_api_key = 'YOUR_API_KEY'
        link = f'https://v6.exchangerate-api.com/v6/{currency_api_key}/pair'

        crypto_api_link = f'https://coincodex.com/api/coincodex/get_coin/SLP'
        crypto_result = requests.get(crypto_api_link).json()['last_price_usd']
        self.conversion_rate = {
            'USD': requests.get(f'{link}/USD/MAD').json()['conversion_rate'],
            'MAD': requests.get(f'{link}/MAD/USD').json()['conversion_rate'],
            'SLP': crypto_result,
            'USDT': 1 / crypto_result,
            'last_updated': time()
        }

        with open('currency_conversion_rate.json', 'w+') as currency_file:
            json.dump(self.conversion_rate, currency_file)

        print('[+] Done.')


class Inventory:
    def __init__(self):
        self.inventory = {}
        try:
            with open('inventory.json', 'r+') as inventory_file:
                self.inventory = json.load(inventory_file)

        except:
            print('\nCreating and Setting up Inventory...')
            self.set_inventory(field='Edit capital', value=0)
            self.set_inventory(field='Edit earning', value=0)
            self.set_inventory(field='Edit SLP', value=0)

    @property
    def get_inventory(self):
        capital, earning, slp_earned = self.inventory.values()
        return f"\n [Capital]   : {round(capital, 2)} \n [Earning]   : {round(earning, 2)} \n ([SLP Earned]   : {int(slp_earned)})\n ========\n [Remaining] : {round(capital - earning, 2)}"

    def set_inventory(self, **kwargs):
        operation, field = kwargs['field'].split(' ')
        if operation == 'Edit':
            self.inventory[field] = kwargs['value']
        elif operation == 'Add':
            self.inventory[field] += kwargs['value']
        print(f'\nUpdating {field} with value {kwargs["value"]} | Your new {field} is : {self.inventory[field]}')
        self.update_inventory_file(self.inventory)

    def update_inventory_file(self, data):
        with open('inventory.json', 'w+') as inventory_file:
            json.dump(data, inventory_file)


class AxieInfinityCalculator:
    def __init__(self):
        # (description, command)
        self.MAIN_COMMANDS = {
            1: ('Open Currency Converter calculator', lambda: self.change_page('currency')),
            2: ('Show/Edit your inventory', lambda: self.change_page('inventory')),
            0: ('Exit', lambda: exit())
        }

        self.CURRENCY_COMMANDS = {
            1: ('Convert from USD to MAD', lambda: self.convert_usd_mad('USD MAD')),
            2: ('Convert from MAD to USD', lambda: self.convert_usd_mad('MAD USD')),
            3: ('Convert from SLP to USDT', lambda: self.convert_usd_mad('SLP USDT')),
            4: ('Convert from USDT to SLP', lambda: self.convert_usd_mad('USDT SLP')),
            0: ('Return Main Menu', lambda: self.change_page('main'))
        }

        self.INVENTORY_COMMANDS = {
            1: ('Show inventory summary', lambda: print(Inventory().get_inventory)),
            2: ('Edit your capital investment', lambda: self.edit_inventory('Edit capital')),
            3: ('Add earning', lambda: self.edit_inventory('Add earning')),
            4: ('Add SLP', lambda: self.edit_inventory('Add SLP')),
            0: ('Return Main Menu', lambda: self.change_page('main'))
        }

        self.pages = {
            'main': self.MAIN_COMMANDS, 'currency': self.CURRENCY_COMMANDS, 'inventory': self.INVENTORY_COMMANDS
        }
        self.current_page = 'main'

        # - Currency Exchanger #
        self.conversion_rate = CurrencyExchanger(force_update=False).get_currency_rate
        self.current_pair = 'USD MAD'

    def print_command(self, command):
        print('\nCommand List :')
        for number, values in command.items():
            if values[0] == 'Exit' or 'Return' in values[0]:
                print('')
            print(
                f'[{number}]   {values[0]} '
            )

    def run(self):
        current_command = self.pages[self.current_page]
        self.print_command(current_command)
        user_choice = input('\nYour choice : ')
        if self.check_input(user_choice):
            result = self.trigger_command(current_command, int(user_choice))
        else:
            print('\n[!] You have to input a numeric number from command list. \n\n')
            self.run()
        self.run()

    def trigger_command(self, command, user_choice):
        try:
            return command[user_choice][1]()
        except KeyError:
            print('Please choose a number from command list.')

    def check_input(self, user_input):
        def string_float():
            try:
                float(user_input)
                return True
            except ValueError:
                return False
        if user_input and (user_input.isnumeric() or string_float()) :
            return True
        return False

    # --- command's command --- #
    def change_page(self, page):
        self.current_page = page

    def convert_usd_mad(self, c_pairs):
        first_pair, second_pair = c_pairs.split(" ")
        c_rate = self.conversion_rate[first_pair]

        print(f'\nConverting {first_pair} To {second_pair} \n-----')
        usd_amount = input(f'{first_pair} Amount : ')
        if self.check_input(usd_amount):
            total = round(c_rate * float(usd_amount or 0), 2)

            print(f'\n{total} {second_pair} | Rate: {c_rate}')
            pyperclip.copy(total)
            print('This value is copied to your clipboard.')
        else:
            print('\n[!] You have to input a numeric amount (eg: 70.50 or 100). \n\n')

    # -- inventory -- #
    def edit_inventory(self, field=''):
        user_input = input(f' {field} : ')
        if self.check_input(user_input):
            Inventory().set_inventory(field=field, value=round(float(user_input), 2))


AxieInfinityCalculator().run()


