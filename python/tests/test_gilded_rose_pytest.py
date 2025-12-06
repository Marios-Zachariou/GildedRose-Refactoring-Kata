# -*- coding: utf-8 -*-
"""
Comprehensive test suite for the Gilded Rose refactored code.

Tests all item categories, edge cases, and business rules.
"""

import pytest
from item import Item, ItemStore, ItemCategory
from gilded_rose import GildedRose


class TestNormalItems:
    """Tests for normal items that degrade in quality."""

    def setup_method(self):
        """Setup run before each test method."""
        ItemStore._store.clear()  # Clear store between tests

    def test_normal_item_decreases_quality_by_one(self):
        """Normal items lose 1 quality per day before sell date."""
        item = Item("Normal Item", sell_in=10, quality=20)
        ItemStore.register_item_category(item, ItemCategory.NORMAL)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 19
        assert item.sell_in == 9

    def test_normal_item_decreases_quality_twice_as_fast_after_sell_date(self):
        """Normal items lose 2 quality per day after sell date."""
        item = Item("Normal Item", sell_in=0, quality=10)
        ItemStore.register_item_category(item, ItemCategory.NORMAL)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 8
        assert item.sell_in == -1

    def test_normal_item_quality_never_negative(self):
        """Quality cannot go below 0."""
        item = Item("Normal Item", sell_in=5, quality=0)
        ItemStore.register_item_category(item, ItemCategory.NORMAL)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 0

    def test_normal_item_quality_stops_at_zero_after_sell_date(self):
        """Quality stops at 0 even with 2x degradation."""
        item = Item("Normal Item", sell_in=0, quality=1)
        ItemStore.register_item_category(item, ItemCategory.NORMAL)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 0

    def test_multiple_normal_items_update_independently(self):
        """Multiple normal items update correctly."""
        items = [
            Item("Item 1", sell_in=5, quality=10),
            Item("Item 2", sell_in=0, quality=8),
        ]
        for item in items:
            ItemStore.register_item_category(item, ItemCategory.NORMAL)
        
        GildedRose(items).update_quality()
        
        assert items[0].quality == 9
        assert items[1].quality == 6


class TestAgingItems:
    """Tests for aging items that improve in quality (e.g., Aged Brie)."""

    def setup_method(self):
        ItemStore._store.clear()

    def test_aging_item_increases_quality(self):
        """Aging items gain 1 quality per day before sell date."""
        item = Item("Aged Brie", sell_in=10, quality=20)
        ItemStore.register_item_category(item, ItemCategory.AGING)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 21
        assert item.sell_in == 9

    def test_aging_item_increases_quality_twice_as_fast_after_sell_date(self):
        """Aging items gain 2 quality per day after sell date."""
        item = Item("Aged Brie", sell_in=0, quality=10)
        ItemStore.register_item_category(item, ItemCategory.AGING)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 12
        assert item.sell_in == -1

    def test_aging_item_quality_never_exceeds_50(self):
        """Quality cannot exceed 50."""
        item = Item("Aged Brie", sell_in=10, quality=50)
        ItemStore.register_item_category(item, ItemCategory.AGING)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 50

    def test_aging_item_quality_caps_at_50_with_double_increase(self):
        """Quality caps at 50 even with 2x improvement after sell date."""
        item = Item("Aged Brie", sell_in=0, quality=49)
        ItemStore.register_item_category(item, ItemCategory.AGING)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 50

    def test_aging_item_from_zero_quality(self):
        """Aging items can start at 0 and increase."""
        item = Item("Aged Brie", sell_in=2, quality=0)
        ItemStore.register_item_category(item, ItemCategory.AGING)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 1


class TestLegendaryItems:
    """Tests for legendary items that never change (e.g., Sulfuras)."""

    def setup_method(self):
        ItemStore._store.clear()

    def test_legendary_item_never_changes_quality(self):
        """Legendary items maintain quality."""
        item = Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)
        ItemStore.register_item_category(item, ItemCategory.LEGENDARY)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 80
        assert item.sell_in == 0

    def test_legendary_item_never_decreases_sell_in(self):
        """Legendary items don't have sell dates."""
        item = Item("Sulfuras, Hand of Ragnaros", sell_in=5, quality=80)
        ItemStore.register_item_category(item, ItemCategory.LEGENDARY)
        
        GildedRose([item]).update_quality()
        
        assert item.sell_in == 5

    def test_legendary_item_quality_above_50(self):
        """Legendary items can have quality above 50."""
        item = Item("Excalibur", sell_in=0, quality=100)
        ItemStore.register_item_category(item, ItemCategory.LEGENDARY)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 100


class TestConcertItems:
    """Tests for concert/event items (e.g., Backstage passes)."""

    def setup_method(self):
        ItemStore._store.clear()

    def test_concert_item_increases_by_1_when_more_than_10_days(self):
        """Concert items gain 1 quality when > 10 days away."""
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20)
        ItemStore.register_item_category(item, ItemCategory.CONCERT)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 21
        assert item.sell_in == 14

    def test_concert_item_increases_by_2_when_10_days_or_less(self):
        """Concert items gain 2 quality when 10 days or less."""
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=20)
        ItemStore.register_item_category(item, ItemCategory.CONCERT)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 22
        assert item.sell_in == 9

    def test_concert_item_increases_by_2_when_6_to_10_days(self):
        """Concert items gain 2 quality when 6-10 days away."""
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=6, quality=20)
        ItemStore.register_item_category(item, ItemCategory.CONCERT)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 22

    def test_concert_item_increases_by_3_when_5_days_or_less(self):
        """Concert items gain 3 quality when 5 days or less."""
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=20)
        ItemStore.register_item_category(item, ItemCategory.CONCERT)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 23
        assert item.sell_in == 4

    def test_concert_item_increases_by_3_when_1_day_left(self):
        """Concert items gain 3 quality on last day."""
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=1, quality=20)
        ItemStore.register_item_category(item, ItemCategory.CONCERT)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 23

    def test_concert_item_drops_to_zero_after_concert(self):
        """Concert items become worthless after event."""
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=50)
        ItemStore.register_item_category(item, ItemCategory.CONCERT)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 0
        assert item.sell_in == -1

    def test_concert_item_quality_caps_at_50(self):
        """Concert items respect quality cap."""
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49)
        ItemStore.register_item_category(item, ItemCategory.CONCERT)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 50


class TestConjuredItems:
    """Tests for conjured items that degrade twice as fast as normal items."""

    def setup_method(self):
        ItemStore._store.clear()

    def test_conjured_item_decreases_quality_by_two(self):
        """Conjured items lose 2 quality per day before sell date."""
        item = Item("Conjured Mana Cake", sell_in=10, quality=20)
        ItemStore.register_item_category(item, ItemCategory.CONJURED)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 18
        assert item.sell_in == 9

    def test_conjured_item_decreases_quality_by_four_after_sell_date(self):
        """Conjured items lose 4 quality per day after sell date."""
        item = Item("Conjured Wand", sell_in=0, quality=20)
        ItemStore.register_item_category(item, ItemCategory.CONJURED)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 16
        assert item.sell_in == -1

    def test_conjured_item_quality_never_negative(self):
        """Conjured item quality cannot go below 0."""
        item = Item("Conjured Potion", sell_in=5, quality=1)
        ItemStore.register_item_category(item, ItemCategory.CONJURED)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 0

    def test_conjured_item_quality_stops_at_zero_after_sell_date(self):
        """Conjured item quality stops at 0 even with 4x degradation."""
        item = Item("Conjured Ring", sell_in=0, quality=3)
        ItemStore.register_item_category(item, ItemCategory.CONJURED)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 0

    def test_conjured_item_from_high_quality(self):
        """Conjured items degrade correctly from high quality."""
        item = Item("Conjured Sword", sell_in=5, quality=50)
        ItemStore.register_item_category(item, ItemCategory.CONJURED)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 48


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def setup_method(self):
        ItemStore._store.clear()

    def test_unknown_item_category_handled(self):
        """Items without registered categories return UNKNOWN."""
        item = Item("Mysterious Item", sell_in=5, quality=10)
        # Don't register the item
        
        category = ItemStore.get_item_category(item.name)
        
        assert category == ItemCategory.UNKNOWN

    def test_multiple_items_of_different_types(self):
        """Multiple items of different types update correctly together."""
        items = [
            Item("Normal Item", sell_in=5, quality=10),
            Item("Aged Brie", sell_in=5, quality=10),
            Item("Sulfuras, Hand of Ragnaros", sell_in=5, quality=80),
            Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=10),
            Item("Conjured Item", sell_in=5, quality=10),
        ]
        
        categories = [
            ItemCategory.NORMAL,
            ItemCategory.AGING,
            ItemCategory.LEGENDARY,
            ItemCategory.CONCERT,
            ItemCategory.CONJURED,
        ]
        
        for item, category in zip(items, categories):
            ItemStore.register_item_category(item, category)
        
        GildedRose(items).update_quality()
        
        assert items[0].quality == 9   # Normal: -1
        assert items[1].quality == 11  # Aging: +1
        assert items[2].quality == 80  # Legendary: no change
        assert items[3].quality == 13  # Concert (5 days): +3
        assert items[4].quality == 8   # Conjured: -2

    def test_quality_boundary_at_zero(self):
        """Quality boundary at 0 is respected."""
        item = Item("Normal Item", sell_in=-5, quality=1)
        ItemStore.register_item_category(item, ItemCategory.NORMAL)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 0

    def test_quality_boundary_at_fifty(self):
        """Quality boundary at 50 is respected."""
        item = Item("Aged Brie", sell_in=5, quality=49)
        ItemStore.register_item_category(item, ItemCategory.AGING)
        
        GildedRose([item]).update_quality()
        
        assert item.quality == 50

    def test_sell_in_can_be_negative(self):
        """Sell_in can go negative."""
        item = Item("Normal Item", sell_in=-5, quality=10)
        ItemStore.register_item_category(item, ItemCategory.NORMAL)
        
        GildedRose([item]).update_quality()
        
        assert item.sell_in == -6

    def test_empty_items_list(self):
        """Empty items list doesn't cause errors."""
        GildedRose([]).update_quality()
        # Should not raise any exceptions

    def test_thirty_days_simulation(self):
        """Simulate 30 days of updates (integration test)."""
        items = [
            Item("+5 Dexterity Vest", sell_in=10, quality=20),
            Item("Aged Brie", sell_in=2, quality=0),
            Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
            Item("Conjured Mana Cake", sell_in=3, quality=6),
        ]
        
        categories = [
            ItemCategory.NORMAL,
            ItemCategory.AGING,
            ItemCategory.LEGENDARY,
            ItemCategory.CONCERT,
            ItemCategory.CONJURED,
        ]
        
        for item, category in zip(items, categories):
            ItemStore.register_item_category(item, category)
        
        gilded_rose = GildedRose(items)
        
        # Run for 30 days
        for _ in range(30):
            gilded_rose.update_quality()
        
        # Verify some expected outcomes
        assert items[0].quality == 0  # Normal item degraded to 0
        assert items[1].quality == 50  # Aged Brie maxed at 50
        assert items[2].quality == 80  # Sulfuras unchanged
        assert items[3].quality == 0  # Backstage pass worthless after concert
        assert items[4].quality == 0  # Conjured degraded to 0


class TestItemStore:
    """Tests for ItemStore functionality."""

    def setup_method(self):
        ItemStore._store.clear()

    def test_register_and_retrieve_category(self):
        """Items can be registered and retrieved."""
        item = Item("Test Item", sell_in=5, quality=10)
        ItemStore.register_item_category(item, ItemCategory.NORMAL)
        
        category = ItemStore.get_item_category(item.name)
        
        assert category == ItemCategory.NORMAL

    def test_unknown_item_returns_unknown_category(self):
        """Unknown items return UNKNOWN category."""
        category = ItemStore.get_item_category("Non-existent Item")
        
        assert category == ItemCategory.UNKNOWN

    def test_register_multiple_items_same_name(self):
        """Items with same name share category (last registration wins)."""
        item1 = Item("Duplicate", sell_in=5, quality=10)
        item2 = Item("Duplicate", sell_in=3, quality=8)
        
        ItemStore.register_item_category(item1, ItemCategory.NORMAL)
        ItemStore.register_item_category(item2, ItemCategory.CONJURED)
        
        category = ItemStore.get_item_category("Duplicate")
        
        assert category == ItemCategory.CONJURED  # Last registration wins

    def test_store_can_be_cleared(self):
        """Store can be cleared between tests."""
        item = Item("Test", sell_in=5, quality=10)
        ItemStore.register_item_category(item, ItemCategory.NORMAL)
        
        ItemStore._store.clear()
        
        category = ItemStore.get_item_category("Test")
        assert category == ItemCategory.UNKNOWN


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
