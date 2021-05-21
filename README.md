# Minecart Protocol

> The Internet in survival Minecraft

This repository includes a simulation of an "internet" running on Minecraft minecarts.

## Vision

We can use chest minecarts like packets in a network.

The chest minecarts carry routing information and a payload.
Routers route chest minecarts to the correct destination based on the routing items inside.
A redstone machine at the destination processes the payload.
After processing, the cart travels to its next destination with any response payload.

This is different from a computer network because it is not easy to copy items.
We need to design a protocol that allows autonomous network systems to operate while conserving resources.
There are also limitations with item sorting and stacking mechanics.

Each destination is a *function* because it has an input and output.
These functions can be arbitrary, and we should be able to freely compose them.

For example, imagine a smelting function:
```
smelt(cobblestone) => stone
```

A minecart routed to `smelt` with a payload full of cobblestone would return with stone.

A more complicated example:
```
set(smelt(get("cobblestone")), "stone")
```

The minecart would go to pick up cobblestone from the key-value store at key `"cobblestone"`.
Then it would go to `smelt` and turn the cobblestone into stone.
Finally, it would store the stone items under the `"stone"` key in the key-value store.

## Possible Functions

- Key-value store: `get(key)`, `set(key, value)`
- Smelting: `smelt(items)`
- Trash (to be stored in some central storage): `trash(items)`
- Mail delivery: `recipient-mailbox-name(items)`
- Fetch by item type: `fetch(item-name)`

## Chunk Loading

Normally, minecarts get stuck when they enter unloaded chunks.
Nether portal chunk loaders can load chunks ahead of minecarts so the carts can travel as far as required.

## Protocol Specification

This is under development as we work on the simulation program.
The general idea is to include:
- Routing items (named paper)
- Payload (shulker boxes only) 
