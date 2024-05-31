from bson import ObjectId
from config.database import init_db
from distance_calc import distance
from models.shop import Shop

# longitude: str # x coordinate
#     latitude: str # y coordinate
#     user_id: str # id of the seller
#     flavors: str # enum variants separated by semicolons
#     payment_methods: str = 0 # 0 - cash, 1 - card, 2 - cash and card


class Repository:
    def __init__(self) -> None:
        self.shops, self.users = init_db()

    # def invidual_serial(shop) -> dict:
    #     return {
    #         "id": str(shop["_id"]),
    #         "name": shop["name"],
    #         "longitude": float(shop["longitude"]),
    #         "latitude": float(shop["latitude"]),
    #         "card_payment": shop["card_payment"],
    #         "flavors": shop["flavors"],
    #         "time": shop["time"],
    #         "startTime": shop["startTime"],
    #         "endTime": shop["endTime"]
    #     }
    def mapToShop(self, shop: dict) -> dict:
        # shop["id"] = str(shop["_id"])
        # del shop["_id"]
        return shop

    def get_all_shops(self) -> list[dict]:
        shops_coursor = self.shops.find()
        print(shops_coursor[0])
        shops = list(map(self.mapToShop, shops_coursor))
        return shops

    def get_shop_by_id(self, id) -> dict:
        return self.mapToShop(self.shops.find_one({"_id": ObjectId(id)}))

    def insert_shop(self, shop: Shop):
        self.shops.insert_one(shop.dict())

    def list_serial(self, shops: list[dict]) -> list:
        serialized = {}
        for shop in shops:
            serialized[shop["id"]] = (shop["latitude"], shop["longitude"])
        return serialized

    def filter_by_distance(self, shops, localization, radius=5):
        return self.get_shops_data(
            distance(self.list_serial(shops), localization, radius=radius)
        )

    def filter_n_nearest(self, shops, localization, n):
        return self.get_shops_data(
            distance(self.list_serial(shops), localization, number_of_output=n)
        )

    def get_shops_data(self, filtered_shops):
        list_of_shops = []
        for id, distance in filtered_shops:
            shop = self.get_shop_by_id(id)
            shop["distance"] = distance
            list_of_shops.append(shop)
        return list_of_shops
