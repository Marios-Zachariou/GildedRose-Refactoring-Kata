# -*- coding: utf-8 -*-
from __future__ import print_function

from item import Item, ItemStore, ItemCategory
from gilded_rose import GildedRose


def main():
    print("OMGHAI!")
    items = [
        Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
        Item(name="Aged Brie", sell_in=2, quality=0),
        Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
        Item(name="Conjured Mana Cake", sell_in=3, quality=6),  # <-- :O
    ]
    
   
    [ItemStore.register_item_category(item, category) for item, category in [
        (items[0], ItemCategory.NORMAL),
        (items[1], ItemCategory.AGING),
        (items[2], ItemCategory.NORMAL),
        (items[3], ItemCategory.LEGENDARY),
        (items[4], ItemCategory.LEGENDARY),
        (items[5], ItemCategory.CONCERT),
        (items[6], ItemCategory.CONCERT),
        (items[7], ItemCategory.CONCERT),
        (items[8], ItemCategory.CONJURED),
    ]]
    days = 2
    import sys
    if len(sys.argv) > 1:
        days = int(sys.argv[1]) + 1
    for day in range(days):
        print("-------- day %s --------" % day)
        print("name, sellIn, quality")
        for item in items:
            print(item)
        print("")
        GildedRose(items).update_quality()


if __name__ == "__main__":
    main()
