"""Count Minecraft blocks using exact grid geometry and storage arithmetic."""
import argparse
from decimal import Decimal, InvalidOperation, ROUND_CEILING
import json
from math import isqrt
import sys

VERSION = "0.1.0"


def positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer.")
    return value


def rectangle(length, width, layers=1):
    return positive(length, "Length") * positive(width, "Width") * positive(layers, "Layers")


def disc(radius):
    if type(radius) is not int or not 0 <= radius <= 10000:
        raise ValueError("Radius must be an integer from 0 to 10000.")
    return sum(2 * isqrt(radius * radius - z * z) + 1 for z in range(-radius, radius + 1))


def circle(radius, inner_radius=None, layers=1):
    count = disc(radius)
    if inner_radius is not None:
        if type(inner_radius) is not int or not 0 <= inner_radius < radius:
            raise ValueError("Inner radius must be nonnegative and smaller than the outer radius.")
        count -= disc(inner_radius)
    return count * positive(layers, "Layers")


def box(length, width, height, thickness=1):
    for value, name in ((length, "Length"), (width, "Width"), (height, "Height"), (thickness, "Thickness")):
        positive(value, name)
    interior = max(length - 2 * thickness, 0) * max(width - 2 * thickness, 0) * max(height - 2 * thickness, 0)
    return length * width * height - interior


def budget(count, stack_size=64, extra_percent="0"):
    if type(count) is not int or count < 0:
        raise ValueError("Block count must be a nonnegative integer.")
    positive(stack_size, "Stack size")
    try:
        extra = Decimal(str(extra_percent))
    except InvalidOperation as error:
        raise ValueError("Extra percentage must be a number.") from error
    if not extra.is_finite() or not 0 <= extra <= 100:
        raise ValueError("Extra percentage must be between 0 and 100.")
    total = int((Decimal(count) * (1 + extra / 100)).to_integral_value(rounding=ROUND_CEILING))
    full_stacks, loose_blocks = divmod(total, stack_size)
    slots = full_stacks + bool(loose_blocks)
    return {"base_blocks": count, "extra_blocks": total - count, "total_blocks": total,
            "stack_size": stack_size, "full_stacks": full_stacks, "loose_blocks": loose_blocks,
            "inventory_slots": slots, "shulker_boxes": (slots + 26) // 27}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=VERSION)
    shapes = parser.add_subparsers(dest="shape", required=True)
    rect = shapes.add_parser("rectangle", help="Solid rectangular floor")
    rect.add_argument("length", type=int)
    rect.add_argument("width", type=int)
    rect.add_argument("--layers", type=int, default=1)
    round_shape = shapes.add_parser("circle", help="Block-centred disc or ring")
    round_shape.add_argument("radius", type=int)
    round_shape.add_argument("--inner-radius", type=int)
    round_shape.add_argument("--layers", type=int, default=1)
    shell = shapes.add_parser("box", help="Closed hollow rectangular shell, including floor and roof")
    for dim in ("length", "width", "height"):
        shell.add_argument(dim, type=int)
    shell.add_argument("--thickness", type=int, default=1)
    for shape in (rect, round_shape, shell):
        shape.add_argument("--stack-size", type=int, default=64)
        shape.add_argument("--extra-percent", default="0")
        shape.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.shape == "rectangle":
            count = rectangle(args.length, args.width, args.layers)
        elif args.shape == "circle":
            count = circle(args.radius, args.inner_radius, args.layers)
        else:
            count = box(args.length, args.width, args.height, args.thickness)
        result = budget(count, args.stack_size, args.extra_percent)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Blocks: {result['total_blocks']} ({result['base_blocks']} base + {result['extra_blocks']} spare)")
            print(f"Stacks: {result['full_stacks']} full + {result['loose_blocks']} loose (size {args.stack_size})")
            print(f"Storage: {result['inventory_slots']} slots; {result['shulker_boxes']} shulker boxes")
        return 0
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
