class Item:
    def __init__(self, type, name=None, stackability=64, metadata=None):
        self.type = type
        self.name = name or type
        self.stackability = stackability
        self.metadata = metadata
    def __repr__(self):
        string = self.type
        if self.type != self.name:
            string += f': "{self.name}"'
        if self.metadata:
            string += f" <{self.metadata}>"
        return string
    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.type == other.type and self.name == other.name and self.metadata == other.metadata
    def __hash__(self):
        return hash((self.type, self.name, self.metadata))

class ItemStack:
    def __init__(self):
        self.item = None
        self.count = 0
    def add(self, item):
        if self.is_empty():
            self.item = item
        if self.item != item:
            return 0
        return self.set_count(self.count + 1)
    def pull(self):
        if self.count > 0:
            self.set_count(self.count - 1)
            return self.item
    def set_count(self, count):
        if count > self.item.stackability:
            return False
        self.count = count
        return True
    def is_empty(self):
        return self.count == 0
    def __repr__(self):
        if self.count == 0:
            return "()"
        return f"({self.item}, {self.count})"
    def __str__(self):
        if self.count == 0:
            return "()"
        if self.count == 1:
            return str(self.item)
        return f"({self.item}, {self.count})"

class Inventory:
    def __init__(self, size):
        self.contents = [ ItemStack() for _ in range(size) ]
    def add_item(self, item):
        for stack in self.contents:
            if stack.add(item):
                return True
        return False
    def pull_item(self):
        for stack in self.contents:
            item = stack.pull()
            if item:
                return item
    def pull_filtered(self, inventory_filter):
        for stack in self.contents:
            if stack.item == inventory_filter:
                item = stack.pull()
                if item:
                    return item
    def transfer_into(self, inventory, count=None):
        transferred = 0
        for stack in self.contents:
            while not stack.is_empty():
                item = stack.pull()
                if inventory.add_item(item):
                    transferred += 1
                    if count is not None and transferred >= count:
                        return True
                else:
                    break
        return self.is_empty()
    def is_empty(self):
        for stack in self.contents:
            if not stack.is_empty():
                return False
        return True
    def __repr__(self):
        return repr(self.contents)
    def __str__(self):
        if self.is_empty():
            return "[]"
        string = "["
        wrote_ellipsis = False
        for stack in self.contents:
            if stack.is_empty():
                wrote_ellipsis = True
            else:
                if wrote_ellipsis:
                    string += "...,"
                string += f"{str(stack)},"
                wrote_ellipsis = False
        return f"{string[:-1]}]"
    def __hash__(self):
        return hash(self.contents)

class ChestMinecart(Inventory):
    def __init__(self):
        Inventory.__init__(self, 27)

class ShulkerBox(Item):
    def __init__(self, inventory=None):
        self.inventory = inventory or Inventory(27)
        Item.__init__(self, "Box", stackability=1, metadata=self.inventory)
    def add_item(self, *args):
        return self.inventory.add_item(*args)
    def pull_item(self, *args):
        return self.inventory.pull_item(*args)
    def pull_filtered(self, *args):
        return self.inventory.pull_filtered(*args)
    def transfer_into(self, *args):
        return self.inventory.transfer_into(*args)
    def is_empty(self, *args):
        return self.inventory.is_empty(*args)

def bad_route(minecart):
    minecart.add_item(Item("paper", "bad route"))

def arity(arity):
    def decorator(f):
        def inner(minecart):
            dest = minecart.pull_item()
            args = [ minecart.pull_item() for _ in range(arity) ]
            next_dest_box = minecart.pull_item()
            next_dest = next_dest_box.pull_item()
            next_args = Inventory(27)
            minecart.transfer_into(next_args)

            return_values = f(*args)

            minecart.add_item(next_dest)
            next_args.transfer_into(minecart)
            for value in return_values:
                minecart.add_item(value)
            next_dest_box.add_item(dest)
            minecart.add_item(next_dest_box)
        return inner
    return decorator

def inventory_filter(filters, inventory):
    for key, value in filters:
        pulled = inventory.pull_filtered(key)
        if pulled:
            inventory.add_item(pulled)
            return value

def box_items(*items, mult=1):
    box = ShulkerBox()
    for _ in range(mult):
        for item in items:
            box.add_item(item)
    return box

from collections import defaultdict
kv_store = defaultdict(lambda: Inventory(27))

@arity(2)
def get2_function(item_box, key_box):
    key = key_box.pull_item()
    chest = kv_store.pop(key)
    key_box.add_item(key)
    key_box.add_item(key)
    while not chest.is_empty():
        item_box.add_item(chest.pull_item())
    return item_box, key_box

@arity(2)
def set2_function(item_box, key_box):
    key = key_box.pull_item()
    chest = kv_store[key]
    item_box.transfer_into(chest)
    kv_store[key] = chest
    return item_box, key_box

@arity(1)
def smelt_function(item_box):
    furnace = {
        Item("cobblestone"): Item("stone")
    }
    chest = Inventory(27)
    while not item_box.is_empty():
        item = item_box.pull_item()
        chest.add_item(furnace[item])
    chest.transfer_into(item_box)
    return item_box

@arity(27)
def permute_function(perm, *boxes):
    input_items = Inventory(27)
    for box in boxes:
        input_items.add_item(box)
    
    output_items = []
    chest = Inventory(27)

    current_item = None
    while not perm.is_empty():
        item = perm.pull_item()
        if current_item is None:
            current_item = item
        elif current_item != item:
            current_item = item
            output_items.append(27)
            chest.transfer_into(input_items)
        else:
            chest.add_item(item)
    
    return output_items

routes = [
    (Item("paper", name="get(2)"), get2_function),
    (Item("paper", name="set(2)"), set2_function),
    (Item("paper", name="smelt(1)"), smelt_function),
    (Item("paper", name="permute(27)"), permute_function),
]
def route(minecart):
    function = inventory_filter(routes, minecart)
    if function:
        function(minecart)
        return True
    return False

minecart = ChestMinecart()
minecart.add_item(Item("paper", name="set(2)"))
minecart.add_item(box_items(Item("cobblestone"), mult=64))
minecart.add_item(box_items(Item("paper", name="key"), mult=2))
minecart.add_item(box_items(Item("paper", name="permute(27)")))
minecart.add_item(box_items(
    *[Item("paper", name="1")]*1,
    *[Item("paper", name="2")]*4,
    *[Item("paper", name="3")]*4,
    *[Item("paper", name="4")]*1,
    *[Item("paper", name="5")]*1,
    *[Item("paper", name="6")]*1,
    *[Item("paper", name="7")]*1,
))

print("Initial condition")
print(minecart)
i, max_iters = 0, 4
while route(minecart) and i < max_iters:
    print(f"\nIteration {i+1}:")
    print(minecart)
    i += 1