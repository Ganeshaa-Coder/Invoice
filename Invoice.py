def generate_invoice():
    print("🧾 Invoice Generator\n")
    items = []

    while True:
        name = input("Enter item name (or 'done' to finish): ")
        if name.lower() == "done":
            break
        try:
            quantity = int(input("Quantity: "))
            price = float(input("Price per item: ₹ "))
            items.append({"name": name, "quantity": quantity, "price": price})
        except ValueError:
            print("Invalid quantity or price. Please enter again.\n")

    print("\n------ Invoice ------")
    subtotal = 0
    for item in items:
        total = item["quantity"] * item["price"]
        subtotal += total
        print(f"{item['name']} (x{item['quantity']}): ₹{total:.2f}")

    tax = subtotal * 0.18  # 18% tax
    grand_total = subtotal + tax
    print(f"\nSubtotal: ₹{subtotal:.2f}")
    print(f"Tax (18%): ₹{tax:.2f}")
    print(f"Total: ₹{grand_total:.2f}")
    print("---------------------")

if __name__ == "__main__":
    generate_invoice()



