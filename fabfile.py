from models import CartItem, Product


def calculate_cart_total(cart_items):
    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity
    return total

# Test the calculate_cart_total function
def test_calculate_cart_total():
    cart_items = [
        CartItem(product=Product(price=10), quantity=2),
        CartItem(product=Product(price=15), quantity=3),
        CartItem(product=Product(price=8), quantity=1),
    ]
    assert calculate_cart_total(cart_items) == 10*2 + 15*3 + 8*1