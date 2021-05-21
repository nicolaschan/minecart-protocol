# Minecart Protocol

> The Internet in survival Minecraft

This repository includes a simulation of an "internet" running on Minecraft minecarts.

## Vision

We can use chest minecarts like packets in a network.

The chest minecarts carry routing information and a payload.
Routers route chest minecarts to the correct destination based on the routing items inside.
The payload is processed at the destination.
Then the cart is sent to its next destination with any response payload.

Each destination is a *function* because it has an input and output.
These functions can be arbitrary, and we should be able to freely compose them.

For example, imagine a smelting function:
```
smelt(cobblestone) => stone
```

A minecart routed to `smelt` with a payload full of cobblestone would return with stone.

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
