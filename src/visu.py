from gi.repository import Gtk
from graph_tool.all import *
import datetime


class MyListBox(Gtk.ListBox):
    def __init__(self, node_dict):
        Gtk.ListBox.__init__(self)
        self.init_ui(node_dict)


class MyGraphWidget(GraphWidget):
    def __init__(self, graph):
        self.graph = graph
        GraphWidget.__init__(self, graph, fruchterman_reingold_layout(graph), vertex_text=graph.v_name,
                             display_props_size=20,
                             # vertex_font_size=20,
                             vertex_size=20,
                             edge_text=graph.e_weight,
                             edge_color=graph.e_color)


class MyGraph(Graph):
    def __init__(self, node_dict):
        Graph.__init__(self, directed=False)
        self.e_weight = self.new_edge_property("string")
        self.e_color = self.new_edge_property("vector<float>")
        self.v_name = self.new_vertex_property("int")
        self.v_diction = {}
        indexes = node_dict.keys()
        for i in indexes:
            vertex = self.add_vertex()
            self.v_name[vertex] = i
            self.v_diction[i] = vertex

        for i in range(0, (len(indexes) - 1)):
            for j in range(i + 1, (len(indexes))):
                edge = self.add_edge(self.v_diction[indexes[i]], self.v_diction[indexes[j]])
                self.e_weight[edge] = round(node_dict[indexes[i]].connections[indexes[j]], 3)
                if len(node_dict[indexes[i]].routingPath[indexes[j]].path) > 2:
                    self.e_color[edge] = [1, 0.7, 0, 1]
                else:
                    self.e_color[edge] = [0.45, 1, 0.50, 1]


class MyWindow(Gtk.Window):
    def __init__(self, node_dict):
        Gtk.Window.__init__(self, title="MyWindow")
        self.resize(1000, 600)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.table = Gtk.Table(14, 14, True)
        self.add(self.table)
        self.label = Gtk.Label(label="Nodes :(choose tow of them)", xalign=0)
        self.nodes = node_dict
        self.node_choose = []
        self.graphWidget = MyGraphWidget(MyGraph(node_dict))
        self.listbox = Gtk.ListBox()
        self.init_ui(self.listbox, node_dict)
        self.refresh_button = Gtk.Button(label="Generat Graph")
        self.refresh_button.connect("clicked", self.on_button_clicked)
        self.table.attach(self.label, 1, 4, 0, 1)
        self.table.attach(self.listbox, 1, 4, 1, 13)
        self.table.attach(self.refresh_button, 1, 4, 13, 14)
        self.table.attach(self.graphWidget, 5, 14, 0, 14)
        self.connect("delete-event", Gtk.main_quit)

    def init_ui(self, listbox, node_dict):
        for i in range(1, len(node_dict) + 1):
            self.add_row(listbox, str(i), node_dict[str(i)].ip_address)

    def add_row(self, listbox, index, name):
        row = Gtk.ListBoxRow()
        h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.add(h_box)
        check = Gtk.CheckButton()
        check.connect("toggled", self.callback, index)

        h_box.pack_start(Gtk.Label(index, xalign=0), True, True, 0)
        h_box.pack_start(Gtk.Label(name, xalign=0), True, True, 0)
        h_box.pack_start(check, True, True, 0)
        listbox.add(row)

    def callback(self, widget, data=None):
        print("%s was toggled %s" % (data, widget.get_active()))
        if widget.get_active():
            self.node_choose.append(data)
        else:
            self.node_choose.remove(data)

    def on_button_clicked(self, widget, data=None):

        if len(self.node_choose) == 2:
            print(self.regenerate_graph())
        if len(self.node_choose) == 0:
            self.table.attach(MyGraphWidget(MyGraph(self.nodes)), 5, 14, 0, 14)
            self.show_all()
        else:
            print("please choose 2 nodes")

    def regenerate_graph(self):
        print(self.node_choose)
        path = self.nodes[self.node_choose[0]].routingPath[self.node_choose[1]].path
        print(path)

        part_graph_widget = MyGraphWidget(MyGraph({k: self.nodes[k] for k in path}))
        '''
        for k in range(0, len(path) - 1):
            self.graphWidget.highlight_color = [0., 0., 0., 0.5]

            if path[k] < path[k+1]:
                self.graphWidget.graph.e_color[self.graphWidget.graph.edge(path[k], path[k + 1])] = [1, 1, 0., 1]
            else:
                self.graphWidget.graph.e_color[self.graphWidget.graph.edge(path[k+1], path[k])] = [1, 1, 0., 1]
        '''
        self.table.attach(part_graph_widget, 5, 14, 0, 14)
        self.show_all()


def main():
    a = {}
    win = MyWindow(a)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
