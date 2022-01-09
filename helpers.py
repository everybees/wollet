import requests
from api.models import Transaction


FIXER_URL = "http://data.fixer.io/api"
FIXER_API_KEY = "4ddf00f196cb9a97bd79e2dcea385547"

# rates = {'AED': 4.169884, 'AFN': 118.644008, 'ALL': 121.412235, 'AMD': 546.499965, 'ANG': 2.035996, 'AOA': 625.464621, 'ARS': 116.694564, 'AUD': 1.582482, 'AWG': 2.044095, 'AZN': 1.926301, 'BAM': 1.954578, 'BBD': 2.281039, 'BDT': 97.082218, 'BGN': 1.958017, 'BHD': 0.428026, 'BIF': 2253.72648, 'BMD': 1.135293, 'BND': 1.535417, 'BOB': 7.778118, 'BRL': 6.398282, 'BSD': 1.129676, 'BTC': 2.6745495e-05, 'BTN': 83.946232, 'BWP': 13.174562, 'BYN': 2.924527, 'BYR': 22251.739678, 'BZD': 2.277141, 'CAD': 1.436185, 'CDF': 2278.53233, 'CHF': 1.044299, 'CLF': 0.034197, 'CLP': 943.595623, 'CNY': 7.240558, 'COP': 4557.88066, 'CRC': 725.47533, 'CUC': 1.135293, 'CUP': 30.08526, 'CVE': 110.19442, 'CZK': 24.422418, 'DJF': 201.121181, 'DKK': 7.434709, 'DOP': 64.811488, 'DZD': 158.376559, 'EGP': 17.853887, 'ERN': 17.029481, 'ETB': 56.045303, 'EUR': 1, 'FJD': 2.42283, 'FKP': 0.856441, 'GBP': 0.836312, 'GEL': 3.513751, 'GGP': 0.856441, 'GHS': 6.986725, 'GIP': 0.856441, 'GMD': 59.947729, 'GNF': 10314.293656, 'GTQ': 8.721414, 'GYD': 236.358611, 'HKD': 8.852599, 'HNL': 27.738234, 'HRK': 7.515178, 'HTG': 112.946657, 'HUF': 359.131155, 'IDR': 16255.974363, 'ILS': 3.536232, 'IMP': 0.856441, 'INR': 84.326712, 'IQD': 1648.853903, 'IRR': 47966.122611, 'ISK': 146.055368, 'JEP': 0.856441, 'JMD': 174.468252, 'JOD': 0.804948, 'JPY': 131.263665, 'KES': 127.996917, 'KGS': 96.270221, 'KHR': 4603.551408, 'KMF': 492.137156, 'KPW': 1021.763469, 'KRW': 1359.575649, 'KWD': 0.343596, 'KYD': 0.941397, 'KZT': 491.934914, 'LAK': 12709.359608, 'LBP': 1708.40576, 'LKR': 229.191202, 'LRD': 167.029952, 'LSL': 17.756261, 'LTL': 3.352224, 'LVL': 0.686727, 'LYD': 5.195972, 'MAD': 10.488982, 'MDL': 20.204959, 'MGA': 4493.451927, 'MKD': 61.575561, 'MMK': 2008.636061, 'MNT': 3245.103633, 'MOP': 9.076087, 'MRO': 405.299349, 'MUR': 49.618219, 'MVR': 17.540094, 'MWK': 922.300263, 'MXN': 23.142939, 'MYR': 4.778489, 'MZN': 72.466084, 'NAD': 17.750328, 'NGN': 469.114658, 'NIO': 39.997382, 'NOK': 10.039956, 'NPR': 134.313971, 'NZD': 1.675499, 'OMR': 0.4371, 'PAB': 1.129676, 'PEN': 4.484927, 'PGK': 3.967459, 'PHP': 58.278672, 'PKR': 199.507914, 'PLN': 4.545201, 'PYG': 7856.268031, 'QAR': 4.133613, 'RON': 4.947035, 'RSD': 117.505737, 'RUB': 85.682651, 'RWF': 1172.24917, 'SAR': 4.261432, 'SBD': 9.18154, 'SCR': 17.011174, 'SDG': 496.687673, 'SEK': 10.281144, 'SGD': 1.539233, 'SHP': 1.56375, 'SLL': 12868.544361, 'SOS': 663.010771, 'SRD': 24.145351, 'STD': 23498.269655, 'SVC': 9.884669, 'SYP': 2852.415069, 'SZL': 17.646198, 'THB': 38.208248, 'TJS': 12.760127, 'TMT': 3.973525, 'TND': 3.270768, 'TOP': 2.593578, 'TRY': 15.661461, 'TTD': 7.668188, 'TWD': 31.394227, 'TZS': 2607.389957, 'UAH': 31.061905, 'UGX': 4004.834888, 'USD': 1.135293, 'UYU': 50.549623, 'UZS': 12221.332191, 'VEF': 242759920546.93082, 'VND': 25759.794556, 'VUV': 128.574926, 'WST': 2.951956, 'XAF': 655.537126, 'XAG': 0.050751, 'XAU': 0.000632, 'XCD': 3.068186, 'XDR': 0.807883, 'XOF': 655.537126, 'XPF': 119.801743, 'YER': 284.106813, 'ZAR': 17.738924, 'ZMK': 10218.997508, 'ZMW': 19.041404, 'ZWL': 365.563832}


def perform_funding(amount, currnecy, wallet):
    ...


def perfrom_withdrawal(amount, currency, wallet_id):
    ...


def convert_to_main_currency(amount, currency, wallet, transaction_type):
    try:
        response = requests.post(f"{FIXER_URL}/latest?access_key={FIXER_API_KEY}")
        data = response.json().get('rates')
        euro_to_currency = data[currency]
        euro_to_wallet_currency = data[wallet.currency]
        amount_conversion = round((euro_to_wallet_currency / euro_to_currency) * amount, 2)
        return Transaction.objects.create(
            wallet=wallet,
            amount=amount_conversion,
            transaction_type=transaction_type,
        )

    except Exception as e:
        return str(e)


def convert_balance(currency, main_currency, balance):
    try:
        response = requests.post(f"{FIXER_URL}/latest?access_key={FIXER_API_KEY}")
        data = response.json().get('rates')
        euro_to_currency = data[currency]
        euro_to_wallet_currency = data[main_currency]
        return round((euro_to_currency / euro_to_wallet_currency) * balance, 2)
    except Exception as e:
        return str(e)