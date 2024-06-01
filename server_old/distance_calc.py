from math import atan2
from math import cos
from math import radians
from math import sin
from math import sqrt


def distance(
    shops: dict[int, tuple[float, float]],
    localization: tuple[float, float],
    number_of_output: int = None,
    radius: float = None,
):
    if not number_of_output:
        number_of_output = len(shops)

    def dist(loc1, loc2):
        return (
            6371.0
            * 2
            * atan2(
                sqrt(
                    sin((radians(loc2[0]) - radians(loc1[0])) / 2) ** 2
                    + cos(radians(loc1[0]))
                    * cos(radians(loc2[0]))
                    * sin((radians(loc2[1]) - radians(loc1[1])) / 2) ** 2
                ),
                sqrt(
                    1
                    - (
                        sin((radians(loc2[0]) - radians(loc1[0])) / 2) ** 2
                        + cos(radians(loc1[0]))
                        * cos(radians(loc2[0]))
                        * sin((radians(loc2[1]) - radians(loc1[1])) / 2) ** 2
                    )
                ),
            )
        )

    shops_list = list(shops.items())
    shops_list.sort(key=lambda loc: dist(loc[1], localization))
    shops_list = list(
        map(lambda x: (x[0], round(dist(x[1], localization), 2)), shops_list)
    )
    if radius:
        shops_list = list(filter(lambda x: x[1] <= radius, shops_list))
    return shops_list[:number_of_output]
