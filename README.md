# BuildBudget

A small Minecraft block and storage calculator for rectangular floors, circular
floors, rings, and closed hollow boxes. Python 3.11+, no external packages,
MIT licensed. It runs offline and prints plain text or JSON.

## Why I'm building this

I like planning Minecraft builds, especially when a project needs a lot of
materials. I want to turn dimensions into an exact block count and a practical
shopping list in stacks and shulker boxes, without doing the same maths each
time. This project starts with a few clearly defined shapes rather than trying
to guess the shape of a whole build.

This is a new project. I'm interested in feedback from people using it to plan
real builds, especially where the shape rules could be clearer.

## Quick start

Download **Code → Download ZIP**, extract the folder, and open a terminal there.
Install Python 3.11 or newer. On Windows, `py` can replace `python`.

```sh
python build_budget.py rectangle 20 30 --layers 2
python build_budget.py circle 15 --inner-radius 12 --extra-percent 10
python build_budget.py box 20 30 12 --thickness 1
python build_budget.py rectangle 20 30 --stack-size 16 --json
```

`rectangle 20 30 --layers 2` needs 1,200 blocks: 18 full stacks plus 48 blocks,
19 storage slots, or one shulker box when stacks hold 64. Storage calculations
assume empty containers and one material per slot.

## Shape rules

| Shape | Exact meaning |
| --- | --- |
| Rectangle | Length × width × layers, all positive integers |
| Circle | Integer block centres satisfy x² + z² ≤ radius²; centred on one block |
| Ring | Outer circle with all centres at x² + z² ≤ inner radius² removed |
| Box | Closed shell including floor and roof; interior dimensions shrink by twice the wall thickness |

A radius is measured from the centre block, so a solid circle's bounding width
is `2 × radius + 1`. Radius 0 contains one block. Radius 1 contains five; radius
2 contains thirteen. A ring with outer radius 2 and inner radius 1 has eight.
These are filled grid shapes, not estimates from π and not a decorative
outline algorithm. A thick box wall that fills the interior becomes solid.
Open-top containers, spheres, ellipses and even-width circle centres aren't
supported yet.

## Storage and spare blocks

The default stack size is 64. Use `--stack-size 16` for items that stack to 16,
or `1` for unstackable items. `--extra-percent` adds 0–100 percent spare blocks,
rounding up once to the next whole block. Shulker boxes have 27 slots in this
calculation. JSON contains the base count, spare count, total, full stacks,
loose blocks, slots and required shulker boxes.

Circle radius is limited to 10,000 to keep runtime bounded. Counts use integer
geometry; spare percentages use decimal arithmetic. Invalid dimensions produce
an error and exit code 1. Successful results exit with code 0. The tool does
not open a world, change blocks or write files; redirect JSON output if desired.

## Development

```sh
python -m unittest discover -v
```

Nine tests include an independent grid enumeration to check circle counts,
small-radius cases, ring boundaries, corners in hollow boxes, exact stack and
shulker boundaries, spare rounding, invalid values and CLI JSON output.
GitHub Actions runs tests on Windows, macOS and Ubuntu with Python 3.11 and 3.13.

## Next steps

- Even-width circles with explicitly documented centre rules.
- Open-top boxes and per-material budgets.
- A browser or desktop view of the same tested calculations.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [LICENSE](LICENSE).
