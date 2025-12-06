# -*- coding: utf-8 -*-
"""
Gilded Rose inventory management system.
"""

from typing import List
from item import Item
from strategy import ItemStrategyFactory


class GildedRose:
    """Manages the Gilded Rose inventory and updates item quality daily."""

    def __init__(self, items: List[Item]):
        """
        Initialize the Gilded Rose with a list of items.

        Args:
            items: List of items in the inventory
        """
        self.items = items

    def update_quality(self) -> None:
        """
        Update the quality and sell_in values for all items in inventory.
        
        This method uses the Strategy pattern to delegate item updates
        to appropriate strategy classes based on item category.
        """
        for item in self.items:
            strategy = ItemStrategyFactory.get_strategy(item)
            strategy.update(item)
