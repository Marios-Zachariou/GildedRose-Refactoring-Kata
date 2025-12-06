# -*- coding: utf-8 -*-
import unittest

from item import Item, ItemStore, ItemCategory
from gilded_rose import GildedRose


class GildedRoseTest(unittest.TestCase):
    
    def setUp(self):
        """Clear ItemStore before each test."""
        ItemStore._store.clear()
    
    def test_normal_item_before_sell_date(self):
        """Test that normal items degrade correctly before sell date."""
        items = [Item("foo", sell_in=5, quality=10)]
        ItemStore.register_item_category(items[0], ItemCategory.NORMAL)
        
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(9, items[0].quality)
    
    def test_normal_item_after_sell_date(self):
        """Test that normal items degrade twice as fast after sell date."""
        items = [Item("foo", sell_in=0, quality=10)]
        ItemStore.register_item_category(items[0], ItemCategory.NORMAL)
        
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(8, items[0].quality)
    
    def test_quality_never_negative(self):
        """Test that quality never goes negative."""
        items = [Item("foo", sell_in=5, quality=0)]
        ItemStore.register_item_category(items[0], ItemCategory.NORMAL)
        
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertEqual(0, items[0].quality)
    
    def test_aged_brie_increases_quality(self):
        """Test that Aged Brie increases in quality."""
        items = [Item("Aged Brie", sell_in=5, quality=10)]
        ItemStore.register_item_category(items[0], ItemCategory.AGING)
        
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertEqual(11, items[0].quality)
    
    def test_quality_never_exceeds_50(self):
        """Test that quality never exceeds 50."""
        items = [Item("Aged Brie", sell_in=5, quality=50)]
        ItemStore.register_item_category(items[0], ItemCategory.AGING)
        
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertEqual(50, items[0].quality)
    
    def test_sulfuras_never_changes(self):
        """Test that Sulfuras never changes."""
        items = [Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)]
        ItemStore.register_item_category(items[0], ItemCategory.LEGENDARY)
        
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(80, items[0].quality)
    
    def test_backstage_pass_increases_as_concert_approaches(self):
        """Test that backstage passes increase in quality."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20)]
        ItemStore.register_item_category(items[0], ItemCategory.CONCERT)
        
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertEqual(21, items[0].quality)
    
    def test_backstage_pass_drops_to_zero_after_concert(self):
        """Test that backstage passes drop to 0 after concert."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=50)]
        ItemStore.register_item_category(items[0], ItemCategory.CONCERT)
        
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertEqual(0, items[0].quality)
    
    def test_conjured_item_degrades_twice_as_fast(self):
        """Test that conjured items degrade twice as fast."""
        items = [Item("Conjured Mana Cake", sell_in=3, quality=6)]
        ItemStore.register_item_category(items[0], ItemCategory.CONJURED)
        
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertEqual(2, items[0].sell_in)
        self.assertEqual(4, items[0].quality)

        
if __name__ == '__main__':
    unittest.main()
