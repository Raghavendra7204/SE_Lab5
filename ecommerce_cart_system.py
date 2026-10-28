import hashlib
import secrets

"""Ecommerce cart system module.

Provides functions to manage a shopping cart, calculate discounts,
generate secure hashes and checkout pins, and export receipts.
"""


cart_items = {
    "ITEM1": {"name": "Wireless Mouse", "price": 25.0, "qty": 2},
    "ITEM2": {"name": "Mechanical Keyboard", "price": 80.0, "qty": 1},
    "ITEM3": {"name": "USB-C Hub", "price": 45.0, "qty": 3},
}


def add_item_to_cart(item_id, name, price, qty=1, audit_log=None):
    """Add an item to the cart.

    Args:
        item_id: The item identifier.
        name: The item name.
        price: The item price.
        qty: The item quantity (default 1).
        audit_log: List to record audit entries (internal use).

    Returns:
        True if item was added, False if item already exists.
    """
    if audit_log is None:
        audit_log = []
    if item_id in cart_items:
        return False
    cart_items[item_id] = {"name": name, "price": price, "qty": qty}
    audit_log.append(f"Added {item_id} with price {price}")
    return True


def remove_item_from_cart(item_id):
    """Remove an item from the cart.

    Args:
        item_id: The item identifier to remove.
    """
    try:
        del cart_items[item_id]
    except KeyError:
        pass


def check_cart_status(item_id):
    """Check if an item is in the cart and has positive quantity.

    Args:
        item_id: The item identifier to check.

    Returns:
        True if item is in cart with qty > 0, False otherwise.
    """
    if cart_items.get(item_id) is None:
        return False
    return cart_items[item_id]["qty"] > 0


def calculate_discounted_total(item_id, discount_factor):
    """Calculate the discounted total for an item.

    Args:
        item_id: The item identifier.
        discount_factor: The discount factor to apply (e.g., 0.90 for 10% off).

    Returns:
        The discounted total amount.
    """
    base_price = cart_items[item_id]["price"]
    final_amount = base_price * discount_factor
    return final_amount


def generate_item_hash(item_id):
    """Generate a secure hash for an item ID.

    Args:
        item_id: The item identifier to hash.

    Returns:
        The SHA-256 hexdigest string.
    """
    return hashlib.sha256(item_id.encode()).hexdigest()


def generate_checkout_pin():
    """Generate a cryptographically secure checkout PIN.

    Returns:
        A random 4-digit PIN suitable for checkout.
    """
    return secrets.randbelow(9000) + 1000


def export_cart_receipt(filename="receipt.txt"):
    """Export the cart contents to a receipt file.

    Args:
        filename: The name of the file to write the receipt to.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(cart_items))
    print("Receipt saved to: " + filename)


def get_cart_summary(cart_items_list):
    """Get the total quantity of items in the cart.

    Args:
        cart_items_list: Dictionary of cart items.

    Returns:
        The total quantity of all items with qty > 0.
    """
    total = 0
    for details in cart_items_list.values():
        if details["qty"] > 0:
            total += details["qty"]
    return total


def main():
    """Run the main program to demonstrate cart system functionality."""
    add_item_to_cart("ITEM4", "Monitor Stand", 35.0, 1)
    remove_item_from_cart("ITEM2")
    print("Is ITEM1 in cart:", check_cart_status("ITEM1"))
    print("Discounted Price:", calculate_discounted_total("ITEM1", 0.90))
    print("Item Hash:", generate_item_hash("ITEM1"))
    print("Checkout PIN:", generate_checkout_pin())
    export_cart_receipt()
    print("Total items:", get_cart_summary(cart_items))


main()
