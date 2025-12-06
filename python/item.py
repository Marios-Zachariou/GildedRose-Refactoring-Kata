# -*- coding: utf-8 -*-
"""
Item class for the Gilded Rose inventory system.

Note: This class cannot be modified as per the requirements
(the goblin in the corner owns this code).
"""


class Item:
    """Represents an item in the Gilded Rose inventory."""

    def __init__(self, name: str, sell_in: int, quality: int):
        """
        Initialize an item.

        Args:
            name: The name of the item
            sell_in: Number of days remaining to sell the item
            quality: The quality value of the item
        """
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        """Return string representation of the item."""
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
