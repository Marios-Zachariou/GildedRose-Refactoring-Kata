# -*- coding: utf-8 -*-
"""
Item class and ItemStore for the Gilded Rose inventory system.

Note: The Item class cannot be modified as per the requirements
(the goblin in the corner owns this code).
"""

from typing import Dict, Optional
from enum import Enum


class ItemCategory(Enum):
    """Enumeration of item categories based on behavior type."""
    NORMAL = "normal"          # Items that degrade normally
    AGING = "aging"            # Items that improve with age (e.g., Aged Brie)
    LEGENDARY = "legendary"    # Items that never change (e.g., Sulfuras)
    CONCERT = "concert"        # Items tied to events (e.g., Backstage passes)
    CONJURED = "conjured"      # Items that degrade twice as fast
    UNKNOWN = "unknown"        # Item category not found


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


class ItemStore:
    """
    Manages item categorization for the Gilded Rose inventory system.
    
    In a production system, this would load categories from a database.
    For now, it uses pattern matching on item names.
    """

    # Static category mappings - in production, this would come from a database
    _store: Dict[str, ItemCategory] = {}

    @classmethod
    def get_item_category(cls, item_name: str) -> ItemCategory:
        """
        Get the category for an item based on its name.
        
        In a production system, this would query a database:
        SELECT category FROM items WHERE name = ?
        
        Args:
            item_name: The name of the item
            
        Returns:
            The ItemCategory for this item
        """
        # O(1) lookup - fast!
        return cls._store.get(item_name, ItemCategory.UNKNOWN)

    @classmethod
    def register_item_category(cls, item: Item, category: ItemCategory) -> None:
        """
        Register an item's category in the store.
        
        This allows dynamic registration of new item types.
        In production, this would insert into a database.
        
        Args:
            item: The item to register
            category: The category to assign to this item
        """
        cls._store[item.name] = category

    @classmethod
    def load_categories_from_db(cls, db_connection) -> None:
        """
        Load item categories from a database (placeholder for production use).
        
        Example implementation:
            cursor = db_connection.cursor()
            cursor.execute("SELECT pattern, category FROM item_categories")
            for pattern, category in cursor.fetchall():
                cls.register_item_category(pattern, ItemCategory(category))
        
        Args:
            db_connection: Database connection object
        """
        # TODO: Implement when database integration is needed
        pass
