import contextlib
import io
import json
import unittest

from build_budget import box, budget, circle, disc, main, rectangle, walls


class GeometryTests(unittest.TestCase):
    def test_rectangle_layers(self):
        self.assertEqual(rectangle(10, 12, 3), 360)

    def test_small_discs_have_exact_grid_counts(self):
        self.assertEqual([disc(r) for r in range(4)], [1, 5, 13, 29])

    def test_disc_matches_independent_grid_enumeration(self):
        for radius in range(12):
            expected = sum(x*x + z*z <= radius*radius for x in range(-radius, radius+1)
                           for z in range(-radius, radius+1))
            self.assertEqual(disc(radius), expected)

    def test_ring_excludes_inner_boundary_and_layers(self):
        self.assertEqual(circle(2, 1), 8)
        self.assertEqual(circle(2, 0, 2), 24)

    def test_hollow_shell_includes_floor_roof_and_corners_once(self):
        self.assertEqual(box(3, 3, 3), 26)
        self.assertEqual(box(2, 2, 2), 8)
        self.assertEqual(box(5, 5, 5, 2), 124)

    def test_walls_matches_independent_grid_enumeration(self):
        for length, width, height, thickness in [(3,3,3,1), (5,7,4,2), (2,4,2,3)]:
            expected = sum(x < thickness or x >= length-thickness or z < thickness or z >= width-thickness
                           for x in range(length) for z in range(width)) * height
            self.assertEqual(walls(length, width, height, thickness), expected)
        self.assertEqual(walls(3, 3, 3), 24)
        with self.assertRaises(ValueError):
            walls(3, 3, 3, 0)

    def test_cli_walls_budget(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["walls", "3", "3", "3", "--extra-percent", "10", "--json"]), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["base_blocks"], 24)
        self.assertEqual(result["total_blocks"], 27)

    def test_exact_stack_and_container_boundaries(self):
        self.assertEqual(budget(64)["loose_blocks"], 0)
        self.assertEqual(budget(65)["inventory_slots"], 2)
        self.assertEqual(budget(1728)["shulker_boxes"], 1)
        self.assertEqual(budget(1729)["shulker_boxes"], 2)
        self.assertEqual(budget(0)["shulker_boxes"], 0)
        self.assertEqual(budget(17, 16)["loose_blocks"], 1)

    def test_spares_round_up_once(self):
        self.assertEqual(budget(65, extra_percent="10")["total_blocks"], 72)
        self.assertEqual(budget(100, extra_percent="0.1")["total_blocks"], 101)

    def test_invalid_input_is_rejected(self):
        for operation in (lambda: rectangle(-1, 4), lambda: circle(2, 2), lambda: disc(10001),
                          lambda: box(1, 1, 1, 0), lambda: budget(1, 0),
                          lambda: budget(1, extra_percent="NaN"), lambda: budget(1, extra_percent="-1")):
            with self.assertRaises(ValueError):
                operation()

    def test_cli_json_reports_expected_geometry(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["circle", "2", "--inner-radius", "1", "--json"]), 0)
        self.assertEqual(json.loads(output.getvalue())["total_blocks"], 8)


if __name__ == "__main__":
    unittest.main()
