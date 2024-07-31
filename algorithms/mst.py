import math

class MetroOptimizer:
    def __init__(self):
        """Инициализирует оптимизатор сети метро."""
        self.stations = []
        self.distances = {}

    def add_station(self, x, y):
        """Добавляет станцию метро с координатами (x, y)."""
        self.stations.append((x, y))
        self.distances.clear()

    def _distance(self, station1, station2):
        """Вычисляет евклидово расстояние между двумя станциями."""
        key = tuple(sorted((station1, station2)))
        if key not in self.distances:
            x1, y1 = station1
            x2, y2 = station2
            self.distances[key] = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return self.distances[key]

    def build_mst(self):
        """
        Строит минимальное остовное дерево (MST) с помощью модифицированного алгоритма Прима.

        Возвращает:
            Список кортежей, представляющих ребра MST, например, [((x1, y1), (x2, y2)), ...].
        """
        num_stations = len(self.stations)
        if num_stations < 2:
            return []

        mst = []
        key = [float('inf')] * num_stations
        parent = [-1] * num_stations
        visited = [False] * num_stations

        key[0] = 0
        for _ in range(num_stations - 1):
            min_key = float('inf')
            min_index = -1
            for v in range(num_stations):
                if not visited[v] and key[v] < min_key:
                    min_key = key[v]
                    min_index = v

            visited[min_index] = True

            for v in range(num_stations):
                if not visited[v]:
                    weight = self._distance(self.stations[min_index], self.stations[v])
                    if weight < key[v]:
                        parent[v] = min_index
                        key[v] = weight

        for i in range(1, num_stations):
            mst.append((self.stations[parent[i]], self.stations[i]))

        return mst