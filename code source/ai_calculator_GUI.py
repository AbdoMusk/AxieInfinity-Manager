import requests
from tkinter import *
from tkinter import ttk


class AxieInfinityCalculator2:
    def __init__(self):
        self.root = Tk(className=' All Clients Viewer')
        self.root.geometry("1400x800+300+100")
        self.root.configure(background='#282828')

        # - Currency Exchanger #
        self.currency_api_key = 'YOUR_API_KEY'
        link = f'https://v6.exchangerate-api.com/v6/{self.currency_api_key}/pair'
        self.conversion_rate = {
            'USD': requests.get(f'{link}/USD/MAD').json()['conversion_rate'],
            'MAD': requests.get(f'{link}/MAD/USD').json()['conversion_rate']
        }
        self.current_pair = 'USD MAD'
        self.currency_result = Label(self.root, text='0.00', width=20)
        self.search_btn = Button(self.root, text='convert', command=self.convert_currency)
        self.exchange_widgets = self.currency_exchange()
        self.currency_result.pack(padx=10, pady=2)
        self.search_btn.pack(padx=10, pady=2)

        # - Crypto Exchanger #
        """self.currency_api_key = 'YOUR_API_KEY'
        requests.get(f'https://coincodex.com/api/coincodex/get_coin/SLP').json()['last_price_usd']

        self.conversion_rate = {
            'SLP': requests.get(f'{link}/USD/MAD').json()['conversion_rate'],
            'USD': requests.get(f'{link}/MAD/USD').json()['conversion_rate']
        }
        self.current_pair = 'USD MAD'
        self.currency_result = Label(self.root, text='0.00', width=20)
        self.search_btn = Button(self.root, text='convert', command=self.convert_currency)
        self.exchange_widgets = self.currency_exchange()
        self.currency_result.pack(padx=10, pady=2)
        self.search_btn.pack(padx=10, pady=2)"""

        self.root.mainloop()

    def convert_currency(self):
        c_pairs = self.current_pair.split(" ")
        c_rate = self.conversion_rate[c_pairs[0]]
        self.currency_result['text'] = str(c_rate * float(self.exchange_widgets[c_pairs[0]][1].get() or 0)) + f'\n Rate: {c_rate}'

    def swape_currency_pairs(self):
        if self.current_pair == 'USD MAD':
            self.current_pair = 'MAD USD'
        else:
            self.current_pair = 'USD MAD'
        self.delete_pairs()
        self.exchange_widgets = self.currency_exchange()

    def delete_pairs(self):
        for label, entry in self.exchange_widgets.values():
            if label:
                label.destroy()
            if entry:
                entry.destroy()
        self.currency_result.pack_forget()
        self.search_btn.pack_forget()

    def currency_exchange(self):
        txtlabel_pair_1, pair_1 = self.textbox_with_label(self.current_pair.split(" ")[0])
        swap_btn = Button(self.root, text='>>', command=self.swape_currency_pairs)
        swap_btn.pack(padx=10, pady=10)
        txtlabel_pair_2 = Label(self.root, text=self.current_pair.split(" ")[1])
        txtlabel_pair_2.pack(padx=10, pady=2)

        self.currency_result.pack(padx=10, pady=2)
        self.search_btn.pack(padx=10, pady=2)
        return {
            self.current_pair.split(' ')[0]: (txtlabel_pair_1, pair_1),
            'swap_btn': (swap_btn, 0),
            self.current_pair.split(' ')[1]: (txtlabel_pair_2, 0)
        }

    # ---------------------------------
    def crypto_exchange(self):
        txtlabel_pair_1, pair_1 = self.textbox_with_label(self.current_pair.split(" ")[0])
        swap_btn = Button(self.root, text='>>', command=self.swape_pairs)
        swap_btn.pack(padx=10, pady=10)
        txtlabel_pair_2 = Label(self.root, text=self.current_pair.split(" ")[1])
        txtlabel_pair_2.pack(padx=10, pady=2)

        self.currency_result.pack(padx=10, pady=2)
        self.search_btn.pack(padx=10, pady=2)
        return {
            self.current_pair.split(' ')[0]: (txtlabel_pair_1, pair_1),
            'swap_btn': (swap_btn, 0),
            self.current_pair.split(' ')[1]: (txtlabel_pair_2, 0)
        }

    def convert_crypto(self):
        c_pairs = self.current_pair.split(" ")
        c_rate = self.conversion_rate[c_pairs[0]]
        self.currency_result['text'] = str(c_rate * float(self.exchange_widgets[c_pairs[0]][1].get() or 0)) + f'\n Rate: {c_rate}'

    def swape_crypto_pairs(self):
        if self.current_pair == 'USD MAD':
            self.current_pair = 'MAD USD'
        else:
            self.current_pair = 'USD MAD'
        self.delete_pairs()
        self.exchange_widgets = self.currency_exchange()

    def delete_crypto_pairs(self):
        for label, entry in self.exchange_widgets.values():
            if label:
                label.destroy()
            if entry:
                entry.destroy()
        self.currency_result.pack_forget()
        self.search_btn.pack_forget()

    def textbox_with_label(self, text):
        txtbox_label = Label(self.root, text=text + ': ')
        txtbox_label.pack(padx=10, pady=2)
        txtbox = Entry(self.root, width=50)
        txtbox.pack(padx=10, pady=5)
        return txtbox_label, txtbox


AxieInfinityCalculator2()
exit()


