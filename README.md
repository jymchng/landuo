# landuo (lazyproperty)
_just a property but lazier_...

Simply put, `lazyproperty` = `property` + `cached_property`.

# Reasons for Creating This
1. In-built `property` decorator allows you to manage your instances' attributes but at a cost of repeated computation for each read of the attribute.
2. `cached_property` built by many [1], allows you to cache your instances' attributes but at a cost of losing the ability to implement `setter` methods of them.

`lazyproperty` solves this problem by enabling caching of the values of your instances' attributes AND implementing `setter` methods for each of them.

# How to Use
#TODO
