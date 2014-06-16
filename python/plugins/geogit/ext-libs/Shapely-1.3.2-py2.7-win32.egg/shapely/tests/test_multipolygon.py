from . import unittest
from shapely.geometry import Polygon, MultiPolygon, asMultiPolygon
from shapely.geometry.base import dump_coords


class MultiPolygonTestCase(unittest.TestCase):

    def test_multipolygon(self):

        # From coordinate tuples
        geom = MultiPolygon(
            [(((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)),
              [((0.25, 0.25), (0.25, 0.5), (0.5, 0.5), (0.5, 0.25))])])
        self.assertIsInstance(geom, MultiPolygon)
        self.assertEqual(len(geom.geoms), 1)
        self.assertEqual(
            dump_coords(geom),
            [[(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0),
              [(0.25, 0.25), (0.25, 0.5), (0.5, 0.5), (0.5, 0.25),
               (0.25, 0.25)]]])

        # Or from polygons
        p = Polygon(((0, 0), (0, 1), (1, 1), (1, 0)),
                    [((0.25, 0.25), (0.25, 0.5), (0.5, 0.5), (0.5, 0.25))])
        geom = MultiPolygon([p])
        self.assertEqual(len(geom.geoms), 1)
        self.assertEqual(
            dump_coords(geom),
            [[(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0),
              [(0.25, 0.25), (0.25, 0.5), (0.5, 0.5), (0.5, 0.25),
               (0.25, 0.25)]]])

        # Or from another multi-polygon
        geom2 = MultiPolygon(geom)
        self.assertEqual(len(geom2.geoms), 1)
        self.assertEqual(
            dump_coords(geom2),
            [[(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0),
              [(0.25, 0.25), (0.25, 0.5), (0.5, 0.5), (0.5, 0.25),
               (0.25, 0.25)]]])

        # Sub-geometry Access
        self.assertIsInstance(geom.geoms[0], Polygon)
        self.assertEqual(
            dump_coords(geom.geoms[0]),
            [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0),
             [(0.25, 0.25), (0.25, 0.5), (0.5, 0.5), (0.5, 0.25),
              (0.25, 0.25)]])
        with self.assertRaises(IndexError):  # index out of range
            geom.geoms[1]

        # Geo interface
        self.assertEqual(
            geom.__geo_interface__,
            {'type': 'MultiPolygon',
             'coordinates': [(((0.0, 0.0), (0.0, 1.0), (1.0, 1.0),
                               (1.0, 0.0), (0.0, 0.0)),
                              ((0.25, 0.25), (0.25, 0.5), (0.5, 0.5),
                               (0.5, 0.25), (0.25, 0.25)))]})

        # Adapter
        coords = ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0))
        holes_coords = [((0.25, 0.25), (0.25, 0.5), (0.5, 0.5), (0.5, 0.25))]
        mpa = asMultiPolygon([(coords, holes_coords)])
        self.assertEqual(len(mpa.geoms), 1)
        self.assertEqual(len(mpa.geoms[0].exterior.coords), 5)
        self.assertEqual(len(mpa.geoms[0].interiors), 1)
        self.assertEqual(len(mpa.geoms[0].interiors[0].coords), 5)


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(MultiPolygonTestCase)
