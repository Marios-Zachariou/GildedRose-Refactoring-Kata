# -*- coding: utf-8 -*-
"""
Item update strategies for the Gilded Rose inventory system.

This module implements the Strategy pattern to handle different item update behaviors.
Each strategy encapsulates the update logic for a specific item type.
"""

from abc import ABC, abstractmethod
from item import Item, ItemStore, ItemCategory


class ItemUpdateStrategy(ABC):
    """Abstract base class for item update strategies."""

    @abstractmethod
    def update(self, item: Item) -> None:
        """
        Update the item's sell_in and quality values.

        Args:
            item: The item to update
        """
        pass

    def _clamp_quality(self, quality: int, max_quality: int = 50) -> int:
        """
        Clamp quality value within valid bounds.

        Args:
            quality: The quality value to clamp
            max_quality: Maximum quality allowed (default: 50)

        Returns:
            Clamped quality value between 0 and max_quality
        """
        return max(0, min(quality, max_quality))


class NormalItemStrategy(ItemUpdateStrategy):
    """Strategy for normal items that degrade in quality over time."""

    def update(self, item: Item) -> None:
        """
        Update normal item: quality degrades by 1, or by 2 after sell_in date.

        Args:
            item: The item to update
        """
        item.sell_in -= 1
        degradation = 2 if item.sell_in < 0 else 1
        item.quality = self._clamp_quality(item.quality - degradation)


class AgingItemStrategy(ItemUpdateStrategy):
    """Strategy for aging items which increase in quality over time (e.g., Aged Brie, fine wine)."""

    def update(self, item: Item) -> None:
        """
        Update aging item: quality increases by 1, or by 2 after sell_in date.

        Args:
            item: The item to update
        """
        item.sell_in -= 1
        improvement = 2 if item.sell_in < 0 else 1
        item.quality = self._clamp_quality(item.quality + improvement)


class LegendaryItemStrategy(ItemUpdateStrategy):
    """Strategy for legendary items that never change (e.g., Sulfuras, mythical artifacts)."""

    def update(self, item: Item) -> None:
        """
        Update legendary item: no changes (quality and sell_in remain constant).

        Args:
            item: The item to update
        """
        # Legendary items never change!
        pass


class ConcertItemStrategy(ItemUpdateStrategy):
    """Strategy for concert/event items that increase in value as the event approaches."""

    def update(self, item: Item) -> None:
        """
        Update concert item (e.g., backstage passes):
        - More than 10 days: quality +1
        - 10 days or less: quality +2
        - 5 days or less: quality +3
        - After event (sell_in < 0): quality drops to 0

        Args:
            item: The item to update
        """
        item.sell_in -= 1

        if item.sell_in < 0:
            # Event has passed, no value
            item.quality = 0
        else:
            # Determine quality increase based on days until event
            if item.sell_in < 5:
                improvement = 3
            elif item.sell_in < 10:
                improvement = 2
            else:
                improvement = 1

            item.quality = self._clamp_quality(item.quality + improvement)


class ConjuredItemStrategy(ItemUpdateStrategy):
    """Strategy for Conjured items which degrade twice as fast as normal items."""

    def update(self, item: Item) -> None:
        """
        Update Conjured item: quality degrades by 2, or by 4 after sell_in date.

        Args:
            item: The item to update
        """
        item.sell_in -= 1
        degradation = 4 if item.sell_in < 0 else 2
        item.quality = self._clamp_quality(item.quality - degradation)


class ItemStrategyFactory:
    """
    Factory class for creating appropriate update strategies based on item category.
    
    Uses ItemStore to determine item category, eliminating the need for string matching.
    """

    # Strategy instances mapped to categories (reusable for better performance)
    _strategies: dict[ItemCategory, ItemUpdateStrategy] = {
        ItemCategory.NORMAL: NormalItemStrategy(),
        ItemCategory.AGING: AgingItemStrategy(),
        ItemCategory.LEGENDARY: LegendaryItemStrategy(),
        ItemCategory.CONCERT: ConcertItemStrategy(),
        ItemCategory.CONJURED: ConjuredItemStrategy(),
    }

    @classmethod
    def get_strategy(cls, item: Item) -> ItemUpdateStrategy:
        """
        Get the appropriate update strategy for an item.
        
        Uses ItemStore to determine the item's category, then returns
        the corresponding strategy. This approach:
        - Separates categorization logic from strategy selection
        - Allows database-driven item categories in production
        - Makes the code more maintainable and testable

        Args:
            item: The item to get a strategy for

        Returns:
            The appropriate ItemUpdateStrategy instance
        """
        category = ItemStore.get_item_category(item.name)
        return cls._strategies[category]
