# landuo (lazyproperty)
_just a property but lazier_...

Simply put, `lazyproperty` = `property` + `cached_property`.
Version: 0.1.0

# Reasons for Creating This
1. In-built `property` decorator allows you to manage your instances' attributes but at a cost of repeated computation for each read of the attribute.
2. `cached_property` built by many [1], allows you to cache your instances' attributes but at a cost of losing the ability to implement `setter` methods of them.

`lazyproperty` solves this problem by enabling caching of the values of your instances' attributes AND implementing `setter` methods for each of them.

# Objectives
#TODO

# How to Use
#TODO

# References
[1] Here is a list of implementations for '`cached_property`'.
#TODO


