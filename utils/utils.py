from django.core.mail import send_mail


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






































# def get_total_cart(instance):
#     from carts.models import CartItem
#     total = 0
#     print(instance.shipping_fee)
#     items = CartItem.objects.filter(cart_id=instance.id)
#     for i in items:
#         total += i.quantity * i.item.price
#
#     if total > 100:
#         instance.shipping_fee = 0
#     else:
#         instance.shipping_fee = 20
#
#     instance.grand_total = total + instance.shipping_fee
#     print(instance.grand_total)

# return total
