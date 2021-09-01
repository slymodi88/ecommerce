from django.core.mail import send_mail


"""
send email to the user after order is created 
"""
# email data
subject = 'your order is ready'
body = 'thank you'
sender_mail = 'slymodi88@gmail.com'


def send_order_email(email):
    send_mail(
        subject,
        body,
        sender_mail,
        [email],
    )


def calculate_price(branch_items):
    """
    calculate price according to available items if not return min price of items
    :param branch_items: branch_items is a queryset that each items in it must contains is_available attribute
    :return: Decimal price
    """
    available_prices = [branch_item.price for branch_item in branch_items if branch_item.is_available]
    if available_prices:
        return min(available_prices)
    return min([branch_item.price for branch_item in branch_items])












