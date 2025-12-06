"""
Functional tests for the Gilded Rose 30-day simulation.

Replaces approval tests with concrete assertions.
"""

from item import Item, ItemStore, ItemCategory
from gilded_rose import GildedRose


def test_thirty_day_simulation():
    """
    Test that the 30-day simulation runs without errors.
    
    This replaces the approval test with a functional test.
    """
    from item import Item, ItemStore, ItemCategory
    from gilded_rose import GildedRose
    
    # Clear store
    ItemStore._store.clear()
    
    # Create items
    items = [
        Item("+5 Dexterity Vest", sell_in=10, quality=20),
        Item("Aged Brie", sell_in=2, quality=0),
        Item("Elixir of the Mongoose", sell_in=5, quality=7),
        Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
        Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
        Item("Conjured Mana Cake", sell_in=3, quality=6),
    ]
    
    # Register items
    categories = [
        ItemCategory.NORMAL,
        ItemCategory.AGING,
        ItemCategory.NORMAL,
        ItemCategory.LEGENDARY,
        ItemCategory.CONCERT,
        ItemCategory.CONJURED,
    ]
    
    for item, category in zip(items, categories):
        ItemStore.register_item_category(item, category)
    
    gilded_rose = GildedRose(items)
    
    # Run for 30 days
    for day in range(30):
        gilded_rose.update_quality()
    
    # Verify expected outcomes after 30 days
    assert items[0].quality == 0, "Normal item should degrade to 0"
    assert items[1].quality == 50, "Aged Brie should reach max quality"
    assert items[2].quality == 0, "Elixir should degrade to 0"
    assert items[3].quality == 80, "Sulfuras should remain at 80"
    assert items[4].quality == 0, "Backstage pass should be worthless after concert"
    assert items[5].quality == 0, "Conjured item should degrade to 0"


if __name__ == "__main__":
    test_thirty_day_simulation()
    print("✅ 30-day simulation test passed!")