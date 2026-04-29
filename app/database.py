import json

shipments = {}

with open("shipments.json") as json_file:
    orders = json.load(json_file)

    for order in orders:
        shipments[order["id"]] = order

    print(shipments)


def save():
    with open("shipments.json", "w") as json_file:
        json.dump(list(shipments.values()), json_file)

