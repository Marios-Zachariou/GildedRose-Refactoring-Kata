# -*- coding: utf-8 -*-
"""
Item update strategies for the Gilded Rose inventory system.

This module implements the Strategy pattern to handle different item update behaviors.
Each strategy encapsulates the update logic for a specific item type.
"""

from abc import ABC, abstractmethod
from item import Item


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


class AgedBrieStrategy(ItemUpdateStrategy):
    """Strategy for Aged Brie which increases in quality over time."""

    def update(self, item: Item) -> None:
        """
        Update Aged Brie: quality increases by 1, or by 2 after sell_in date.

        Args:
            item: The item to update
        """
        item.sell_in -= 1
        improvement = 2 if item.sell_in < 0 else 1
        item.quality = self._clamp_quality(item.quality + improvement)


class SulfurasStrategy(ItemUpdateStrategy):
    """Strategy for Sulfuras, a legendary item that never changes."""

    def update(self, item: Item) -> None:
        """
        Update Sulfuras: no changes (legendary item with quality 80).

        Args:
            item: The item to update
        """
        # Sulfuras never changes - it's legendary!
        pass


class BackstagePassStrategy(ItemUpdateStrategy):
    """Strategy for Backstage passes which increase in value as concert approaches."""

    def update(self, item: Item) -> None:
        """
        Update Backstage pass:
        - More than 10 days: quality +1
        - 10 days or less: quality +2
        - 5 days or less: quality +3
        - After concert (sell_in < 0): quality drops to 0

        Args:
            item: The item to update
        """
        item.sell_in -= 1

        if item.sell_in < 0:
            # Concert has passed, no value
            item.quality = 0
        else:
            # Determine quality increase based on days until concert
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
