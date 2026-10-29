import unittest
from router import route

class RoutingTests(unittest.TestCase):
    def test_report_examples(self):
        self.assertFalse(route([('car', .6)]).use_large)
        self.assertTrue(route([('tricycle', .85)]).use_large)
    def test_empty_fallback(self):
        self.assertEqual(route([]).reason, 'empty_detections')
    def test_threshold_equality(self):
        self.assertFalse(route([('car', 1)], .76).use_large)
    def test_image_mean_not_any_box(self):
        self.assertFalse(route([('car', .8)] * 9 + [('tricycle', .6)]).use_large)
    def test_invalid_values(self):
        for value in [float('nan'), float('inf'), -.1, 1.1, True]:
            with self.assertRaises(ValueError): route([('car', value)])
            with self.assertRaises(ValueError): route([], value)
    def test_unmapped_class_rejected(self):
        with self.assertRaises(ValueError): route([('pedestrian', .8)])
    def test_permutation_invariance(self):
        boxes = [('car', .8), ('person', .4), ('tricycle', .3)]
        self.assertEqual(route(boxes), route(reversed(boxes)))

if __name__ == '__main__': unittest.main()
