import math
import pytest

from dijkstra import dijkstra_modified, get_neighbors


@pytest.fixture
def source_with_eight_neighbors():
    expected_dist = 1 + 2 * math.sqrt(2)
    return [(3, 3), (5, 6), 7, 7, expected_dist]


@pytest.fixture
def source_with_three_neighbors():
    return [(0, 1), 7, 7]


@pytest.fixture
def source_with_five_neighbors():
    return [(3, 1), 7, 7]


# TODO: test pred so that the shortest path is defined correctly
def test_dijkstra(source_with_eight_neighbors):
    vals = source_with_eight_neighbors
    assert dijkstra_modified(vals[0], vals[1], vals[2], vals[3])[0] == vals[4]


def test_get_neighbors(source_with_eight_neighbors, source_with_three_neighbors, source_with_five_neighbors):
    assert get_neighbors(source_with_eight_neighbors[0], source_with_eight_neighbors[2],
                         source_with_eight_neighbors[3]) == {(2, 2), (3, 2), (4, 2), (2, 3), (4, 3), (2, 4), (3, 4),
                                                             (4, 4)}

    assert get_neighbors(source_with_three_neighbors[0], source_with_three_neighbors[1], source_with_three_neighbors[2]) \
           == {(0, 2), (1, 1), (1, 2)}

    assert get_neighbors(source_with_eight_neighbors[0], source_with_eight_neighbors[2], source_with_eight_neighbors[3]) \
           == {(2, 3), (4, 3), (2, 2), (3, 2), (4, 2), (2, 4), (3, 4), (4, 4)}

