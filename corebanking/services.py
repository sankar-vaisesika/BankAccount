def calculate_interest(account):
    if account.account_type=="SAVINGS":
        rate=0.04
    else:
        rate=1

    interest=account.balance*rate

    return rate