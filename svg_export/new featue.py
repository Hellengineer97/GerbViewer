class SmartTraceList(list):
    """Кастомный список, который выглядит как обычный,
    но при добавлении дорожки запускает её логику переезда."""

    def __init__(self, iterable=None, net=None):
        super().__init__(iterable or [])
        self.net = net  # Ссылка на сеть, которой принадлежит этот список

    def append(self, trace: 'Trace') -> None:
        """Перехватываем .append()"""
        if trace.net is not self.net:
            trace.net = self.net  # Запускает всю цепочку автоматического переезда

    def extend(self, traces) -> None:
        """Перехватываем .extend() для массового добавления"""
        for trace in traces:
            self.append(trace)

    def __setitem__(self, index, trace: 'Trace') -> None:
        """Перехватываем прямую замену по индексу: net.traces[0] = trace"""
        # Сначала выписываем старую дорожку, которая была на этом месте
        old_trace = self[index]
        if old_trace.net is self.net:
            # Напрямую просим менеджер выписать её
            self.net._manager.move_trace_to_net(old_trace, None)

        # Прописываем новую дорожку
        if trace.net is not self.net:
            trace.net = self.net

    def __add__(self, other) -> 'SmartTraceList':
        """Перехватываем сложение через плюс: net.traces + [trace]"""
        # Создаем новый независимый умный список
        new_list = SmartTraceList(super().__add__(other), net=self.net)
        return new_list

    def __iadd__(self, other) -> 'SmartTraceList':
        """Перехватываем оператор += : net.traces += [trace]"""
        self.extend(other)
        return self


class ConnectivityManager:
    def __init__(self, board):
        self.board = board
        self._trace_to_net_map: dict[int, 'Net'] = {}

    def get_net_of_trace(self, trace: 'Trace') -> 'Net | None':
        return self._trace_to_net_map.get(id(trace))

    def move_trace_to_net(self, trace: 'Trace', new_net: 'Net | None') -> None:
        old_net = self._trace_to_net_map.get(id(trace))
        if old_net is new_net:
            return

        # 1. Выписываем из старой сети с помощью базового метода list
        if old_net is not None and trace in old_net._traces:
            list.remove(old_net._traces, trace)

        # 2. Прописываем в новую сеть с помощью базового метода list
        if new_net is not None:
            self._trace_to_net_map[id(trace)] = new_net
            if trace not in new_net._traces:
                list.append(new_net._traces, trace)
        else:
            self._trace_to_net_map.pop(id(trace), None)


class Net:
    def __init__(self, name: str, manager: ConnectivityManager):
        self.name = name
        self._manager = manager
        # Наш кастомный список, привязанный к этой сети
        self._traces = SmartTraceList(net=self)

    @property
    def traces(self) -> SmartTraceList:
        """Снаружи это выглядит как абсолютно обычный список!"""
        return self._traces

    @traces.setter
    def traces(self, new_traces) -> None:
        """Позволяет полностью перезаписать список: net.traces = [t1, t2]"""
        self._traces.clear()
        self._traces.extend(new_traces)

    def __repr__(self) -> str:
        return f"Net({self.name!r}, Traces: {len(self._traces)})"


class Trace:
    def __init__(self, polygon, layer_id: str, connectivity_manager: ConnectivityManager):
        self.polygon = polygon
        self.layer_id = layer_id
        self._manager = connectivity_manager

    @property
    def net(self) -> 'Net | None':
        return self._manager.get_net_of_trace(self)

    @net.setter
    def net(self, new_net: 'Net | None') -> None:
        self._manager.move_trace_to_net(self, new_net)


# Инициализируем (представим, что мы внутри BoardView)
class FakeBoard: pass
board = FakeBoard()
manager = ConnectivityManager(board)

net_gnd = Net("GND", manager)
net_vcc = Net("VCC", manager)

trace1 = Trace(None, "F_Cu", manager)

print("1. Добавляем через обычный .append():")
net_gnd.traces.append(trace1)  # Работает как родной список!

print(f"Где дорожка? -> {trace1.net.name}")  # Выведет: GND
print(f"В GND лежит дорожек: {len(net_gnd.traces)}")  # Выведет: 1

print("\n2. Переносим в другую сеть через .append() новой сети:")
net_vcc.traces.append(trace1)  # Снова используем стандартный метод!

print(f"Где ТЕПЕРЬ дорожка? -> {trace1.net.name}")  # Выведет: VCC
print(f"Из старой сети GND она удалилась? -> {len(net_gnd.traces) == 0}")  # Выведет: True
