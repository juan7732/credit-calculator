import math
import sys


def parse_args(parse_arguments):
    args = {}
    if len(parse_arguments) != 4:
        abort_incorrect_params()
    for arg in parse_arguments:
        values = arg.split('=')
        values[0] = values[0].replace('-', '')
        args[values[0]] = values[1]

    if 'type' not in args.keys() or 'interest' not in args.keys():
        abort_incorrect_params()
    if args['type'] == 'diff' and 'payment' in args.keys():
        abort_incorrect_params()
    if args['type'] != 'diff' and args['type'] != 'annuity':
        abort_incorrect_params()
    if 'principal' not in args.keys():
        args['principal'] = None
    if 'periods' not in args.keys():
        args['periods'] = None
    if 'payment' not in args.keys():
        args['payment'] = None

    return args


def abort_incorrect_params():
    print('Incorrect parameters')
    exit()


arguments = sys.argv
arguments.pop(0)
parsed_arguments = parse_args(arguments)


class CreditCalculator:
    def __init__(self, passed_args):
        self.type = passed_args['type']
        self.credit_principal = float(passed_args['principal']) if passed_args['principal'] is not None else None
        self.monthly_payment = float(passed_args['payment']) if passed_args['payment'] is not None else None
        self.count_periods = float(passed_args['periods']) if passed_args['periods'] is not None else None
        self.credit_interest = float(passed_args['interest']) / 100
        self.nominal_interest = self.credit_interest / 12

    def calculate_count(self):
        count = math.ceil(math.log(self.monthly_payment / (self.monthly_payment - self.nominal_interest * self.credit_principal), 1 + self.nominal_interest))
        print(f'You need {self.convert_months_to_years(count)} to repay this credit')
        print(f'Overpayment = {math.ceil(self.monthly_payment * count - self.credit_principal)}')

    def calculate_payment(self):
        midcalc = self.nominal_interest * (1 + self.nominal_interest) ** self.count_periods
        midcalc2 = (1 + self.nominal_interest) ** self.count_periods - 1
        annuity_payment = math.ceil(self.credit_principal * (midcalc/midcalc2))
        print(f'Your annuity payment = {annuity_payment}!')
        print(f'Overpayment = {math.ceil(annuity_payment * self.count_periods - self.credit_principal)}')

    def calculate_principal(self):
        midcalc = self.nominal_interest * (1 + self.nominal_interest) ** self.count_periods
        midcalc2 = midcalc2 = (1 + self.nominal_interest) ** self.count_periods - 1
        credit_principal = self.monthly_payment / (midcalc/midcalc2)
        print(f'Your credit principal = {math.ceil(credit_principal)}!')
        print(f'Overpayment = {math.ceil(self.monthly_payment * self.count_periods - credit_principal)}')

    def calculate_differentiated_payments(self):
        total_overpaid = 0
        for i in range(1, int(self.count_periods + 1)):
            midcalc = self.credit_principal - (self.credit_principal * (i - 1))/self.count_periods
            paid = math.ceil((self.credit_principal/self.count_periods) + self.nominal_interest * midcalc)
            total_overpaid += paid
            print(f'Month {i}: paid out {paid}')
        print(f'Overpayment = {total_overpaid - self.credit_principal}')

    def convert_months_to_years(self, months):
        years = months // 12
        months_left = months % 12
        if months_left == 0 and years == 0:
            return ''
        elif years == 0:
            return f'{str(months_left) + " month" + ("" if months_left == 1 else "s")}'
        elif months_left == 0:
            return f'{years} year{"" if years == 1 else "s"}'
        else:
            return f'{years} year{"" if years == 1 else "s"} ' \
               f'{"and " + str(months_left) + " month" + ("" if months_left == 1 else "s")}'

    def calculate_result(self):
        if self.type == 'diff':
            user_input = 'diff'
        elif self.type == 'annuity' and self.monthly_payment is None:
            user_input = 'a'
        elif self.type == 'annuity' and self.count_periods is None:
            user_input = 'n'
        elif self.type == 'annuity' and self.credit_principal is None:
            user_input = 'p'

        results = {
            'n': self.calculate_count,
            'a': self.calculate_payment,
            'p': self.calculate_principal,
            'diff': self.calculate_differentiated_payments
        }
        results[user_input]()


myCalc = CreditCalculator(parsed_arguments)
myCalc.calculate_result()
