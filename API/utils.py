
def format_change(amount):
    denominations = [100, 50, 20, 10, 5]
    change = {}

    for denom in denominations:
        count = amount // denom
        if count > 0:
            change[str(denom)] = count
            amount -= count * denom

    return change