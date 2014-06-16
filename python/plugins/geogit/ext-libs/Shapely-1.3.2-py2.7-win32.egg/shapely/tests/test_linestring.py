from . import unittest, numpy
from shapely.geometry import LineString, asLineString, Point


class LineStringTestCase(unittest.TestCase):

    def test_linestring(self):

        # From coordinate tuples
        line = LineString(((1.0, 2.0), (3.0, 4.0)))
        self.assertEqual(len(line.coords), 2)
        self.assertEqual(line.coords[:], [(1.0, 2.0), (3.0, 4.0)])

        # From Points
        line2 = LineString((Point(1.0, 2.0), Point(3.0, 4.0)))
        self.assertEqual(len(line2.coords), 2)
        self.assertEqual(line2.coords[:], [(1.0, 2.0), (3.0, 4.0)])

        # From mix of tuples and Points
        line3 = LineString((Point(1.0, 2.0), (2.0, 3.0), Point(3.0, 4.0)))
        self.assertEqual(len(line3.coords), 3)
        self.assertEqual(line3.coords[:], [(1.0, 2.0), (2.0, 3.0), (3.0, 4.0)])

        # From lines
        copy = LineString(line)
        self.assertEqual(len(copy.coords), 2)
        self.assertEqual(copy.coords[:], [(1.0, 2.0), (3.0, 4.0)])

        # Bounds
        self.assertEqual(line.bounds, (1.0, 2.0, 3.0, 4.0))

        # Coordinate access
        self.assertEqual(tuple(line.coords), ((1.0, 2.0), (3.0, 4.0)))
        self.assertEqual(line.coords[0], (1.0, 2.0))
        self.assertEqual(line.coords[1], (3.0, 4.0))
        with self.assertRaises(IndexError):
            line.coords[2]  # index out of range

        # Geo interface
        self.assertEqual(line.__geo_interface__,
                         {'type': 'LineString',
                          'coordinates': ((1.0, 2.0), (3.0, 4.0))})

        # Coordinate modification
        line.coords = ((-1.0, -1.0), (1.0, 1.0))
        self.assertEqual(line.__geo_interface__,
                         {'type': 'LineString',
                          'coordinates': ((-1.0, -1.0), (1.0, 1.0))})

        # Adapt a coordinate list to a line string
        coords = [[5.0, 6.0], [7.0, 8.0]]
        la = asLineString(coords)
        self.assertEqual(la.coords[:], [(5.0, 6.0), (7.0, 8.0)])

        # Test Non-operability of Null geometry
        l_null = LineString()
        self.assertEqual(l_null.wkt, 'GEOMETRYCOLLECTION EMPTY')
        self.assertEqual(l_null.length, 0.0)

        # Check that we can set coordinates of a null geometry
        l_null.coords = [(0, 0), (1, 1)]
        self.assertAlmostEqual(l_null.length, 1.4142135623730951)

    @unittest.skipIf(not numpy, 'Numpy required')
    def test_numpy(self):

        from numpy import array, asarray
        from numpy.testing import assert_array_equal

        # Construct from a numpy array
        line = LineString(array([[0.0, 0.0], [1.0, 2.0]]))
        self.assertEqual(len(line.coords), 2)
        self.assertEqual(line.coords[:], [(0.0, 0.0), (1.0, 2.0)])

        line = LineString(((1.0, 2.0), (3.0, 4.0)))
        la = asarray(line)
        expected = array([[1.0, 2.0], [3.0, 4.0]])
        assert_array_equal(la, expected)

        # Coordinate sequences can be adapted as well
        la = asarray(line.coords)
        assert_array_equal(la, expected)

        # Adapt a Numpy array to a line string
        a = array([[1.0, 2.0], [3.0, 4.0]])
        la = asLineString(a)
        assert_array_equal(la.context, a)
        self.assertEqual(la.coords[:], [(1.0, 2.0), (3.0, 4.0)])

        # Now, the inverse
        self.assertEqual(la.__array_interface__,
                         la.context.__array_interface__)

        pas = asarray(la)
        assert_array_equal(pas, array([[1.0, 2.0], [3.0, 4.0]]))

        # From Array.txt
        a = asarray([[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]])
        line = LineString(a)
        self.assertEqual(line.coords[:], [(0.0, 0.0), (2.0, 2.0), (1.0, 1.0)])

        data = line.ctypes
        self.assertEqual(data[0], 0.0)
        self.assertEqual(data[5], 1.0)

        b = asarray(line)
        assert_array_equal(b, array([[0., 0.], [2., 2.], [1., 1.]]))


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(LineStringTestCase)
