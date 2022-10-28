import assets


def count_money():
    pennies = int(input("Input pennies:"))
    nickles = int(input("Input nickles:"))
    dimes = int(input("Input dimes:"))
    quarters = int(input("Input quarters:"))

    return 0.01 * pennies + 0.05 * nickles + 0.1 * dimes + 0.25 * quarters


def refund(money):
    print(f"\nApologies, not enough money to buy the selected product. ${round(money, 2)} has been refunded.")


def refund_ingredients_shortage(money):
    print(f"\n${round(money, 2)} has been refunded.")


def return_change(beverage_name, money, product_cost, ):
    change = money - product_cost
    print(f"\nThank you for your purchase, your {beverage_name} will be ready momentarily. \nPlease take your change. "
          f"Change amount: ${round(change, 2)}")
    return product_cost


def no_change(beverage_name, product_cost):
    print(f"Thank you for your purchase, your {beverage_name} will be ready momentarily.")
    return product_cost


def deduct_ingredients_add_profit(beverage_name, resources_list, money, product):
    tmp_resource = resources_list
    if money > product["cost"]:
        tmp_resource["money"] += return_change(beverage_name, money, product["cost"])
    else:
        tmp_resource["money"] += no_change(beverage_name, product["cost"])
    if "milk" in product["ingredients"]:
        tmp_resource["milk"] -= product["ingredients"]["milk"]
    if "water" in product["ingredients"]:
        tmp_resource["water"] -= product["ingredients"]["water"]
    if "coffee" in product["ingredients"]:
        tmp_resource["coffee"] -= product["ingredients"]["coffee"]

    return tmp_resource


def enough_resources(beverage_name, resource_list, money, product):
    sufficient_resources = True
    missing = []
    if "milk" in product["ingredients"]:
        if resource_list["milk"] < product["ingredients"]["milk"]:
            sufficient_resources = False
            missing.append("milk")
    if "water" in product["ingredients"]:
        if resource_list["water"] < product["ingredients"]["water"]:
            sufficient_resources = False
            missing.append("water")
    if "coffee" in product["ingredients"]:
        if resource_list["coffee"] < product["ingredients"]["coffee"]:
            sufficient_resources = False
            missing.append("coffee")
    if not sufficient_resources:
        print(f"Unfortunately, your {beverage_name} could not be made since the following ingredients are missing: ", end="")
        for ingredient in missing:
            print(f"[{ingredient}] ", end="")

        refund_ingredients_shortage(money)
    return sufficient_resources


def buy_product(beverage_name, product, resources_list):
    money = count_money()
    tmp_resource = resources_list
    if money < product["cost"]:
        refund(money)
        return tmp_resource
    else:
        if enough_resources(beverage_name, resources_list, money, product):
            tmp_resource = deduct_ingredients_add_profit(beverage_name, resources_list, money, product)
        return tmp_resource


def print_report(resources_list):
    print(f"Water: {resources_list['water']}")
    print(f"Milk: {resources_list['milk']}")
    print(f"Coffee: {resources_list['coffee']}")
    print(f"Money: {resources_list['money']}")


if __name__ == '__main__':

    resources = assets.resources
    menu = assets.MENU
    beverages = []
    run = True
    for menu_item in menu:
        beverages.append(menu_item)
    while run:

        beverage_number = 0
        while beverage_number not in range(1, len(beverages)+1):
            print("Select one of the drinks by number:")
            for item in beverages:
                print(f"{beverages.index(item) + 1}. {item}")
            beverage_input = input("Your choice: ")
            if beverage_input == "report":
                print_report(resources)
            elif beverage_input == "shutdown":
                run = False
                print("Shutting down...")
                break
            else:
                try:
                    beverage_number = int(beverage_input)
                    if beverage_number not in range(1, len(beverages)+1):
                        print("Unrecognized option, try again.")
                except ValueError:
                    print("Unrecognized option, try again.")
        if run:
            beverage = beverages[beverage_number-1]
            resources = buy_product(beverage, menu[beverage], resources)
