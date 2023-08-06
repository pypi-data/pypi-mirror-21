# test_dot.py
# flake8: noqa

import unittest
import itertools

from graphviz.dot import Graph, Digraph


class TestDot(unittest.TestCase):

    def test_repr_svg(self, pattern=r'(?s)^<\?xml .+</svg>\s*$'):
        self.assertRegexpMatches(Graph('spam')._repr_svg_(), pattern)

    def test_iter_subgraph_strict(self):
        with self.assertRaisesRegexp(ValueError, r'strict'):
            Graph().subgraph(Graph(strict=True))

    def test_iter_strict(self):
        self.assertEqual(Graph(strict=True).source, 'strict graph {\n}')
        self.assertEqual(Digraph(strict=True).source, 'strict digraph {\n}')

    def test_attr_invalid_kw(self):
        with self.assertRaisesRegexp(ValueError, r'attr'):
            Graph().attr('spam')

    def test_attr_kw_none(self):
        dot = Graph()
        dot.attr(spam='eggs')
        self.assertEqual(dot.source, 'graph {\n\tspam=eggs\n}')

    def test_subgraph_graph_none(self):
        dot = Graph()
        with dot.subgraph(name='name', comment='comment'):
            pass
        self.assertEqual(dot.source, 'graph {\n\t// comment\n\tsubgraph name {\n\t}\n}')

    def test_subgraph_graph_notsole(self):
        with self.assertRaisesRegexp(ValueError, r'sole'):
            Graph().subgraph(Graph(), name='spam')

    def test_subgraph_mixed(self):
        for cls1, cls2 in itertools.permutations([Graph, Digraph], 2):
            with self.assertRaisesRegexp(ValueError, r'kind'):
                cls1().subgraph(cls2())

    def test_subgraph_reflexive(self):  # guard against potential infinite loop
        dot = Graph()
        dot.subgraph(dot)
        self.assertEqual(dot.source, 'graph {\n\t{\n\t}\n}')

    def test_subgraph(self):
        s1 = Graph()
        s1.node('A')
        s1.node('B')
        s1.node('C')
        s1.edge('A', 'B', constraint='false')
        s1.edges(['AC', 'BC'])

        s2 = Graph()
        s2.node('D')
        s2.node('E')
        s2.node('F')
        s2.edge('D', 'E', constraint='false')
        s2.edges(['DF', 'EF'])

        dot = Graph()
        dot.subgraph(s1)
        dot.subgraph(s2)
        dot.attr('edge', style='dashed')
        dot.edges(['AD', 'BE', 'CF'])

        self.assertEqual(dot.source, '''graph {
	{
		A
		B
		C
			A -- B [constraint=false]
			A -- C
			B -- C
	}
	{
		D
		E
		F
			D -- E [constraint=false]
			D -- F
			E -- F
	}
	edge [style=dashed]
		A -- D
		B -- E
		C -- F
}''')


class TestHTML(unittest.TestCase):
    """http://www.graphviz.org/doc/info/shapes.html#html"""

    def test_label_html(self):
        dot = Digraph('structs', node_attr={'shape': 'plaintext'})
        dot.node('struct1', '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>left</TD>
    <TD PORT="f1">middle</TD>
    <TD PORT="f2">right</TD>
  </TR>
</TABLE>>''')
        dot.node('struct2', '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD PORT="f0">one</TD>
    <TD>two</TD>
  </TR>
</TABLE>>''')
        dot.node('struct3', '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
  <TR>
    <TD ROWSPAN="3">hello<BR/>world</TD>
    <TD COLSPAN="3">b</TD>
    <TD ROWSPAN="3">g</TD>
    <TD ROWSPAN="3">h</TD>
  </TR>
  <TR>
    <TD>c</TD>
    <TD PORT="here">d</TD>
    <TD>e</TD>
  </TR>
  <TR>
    <TD COLSPAN="3">f</TD>
  </TR>
</TABLE>>''')
        dot.edge('struct1:f1', 'struct2:f0')
        dot.edge('struct1:f2', 'struct3:here')
        self.assertEqual(dot.source, '''digraph structs {
	node [shape=plaintext]
	struct1 [label=<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>left</TD>
    <TD PORT="f1">middle</TD>
    <TD PORT="f2">right</TD>
  </TR>
</TABLE>>]
	struct2 [label=<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD PORT="f0">one</TD>
    <TD>two</TD>
  </TR>
</TABLE>>]
	struct3 [label=<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
  <TR>
    <TD ROWSPAN="3">hello<BR/>world</TD>
    <TD COLSPAN="3">b</TD>
    <TD ROWSPAN="3">g</TD>
    <TD ROWSPAN="3">h</TD>
  </TR>
  <TR>
    <TD>c</TD>
    <TD PORT="here">d</TD>
    <TD>e</TD>
  </TR>
  <TR>
    <TD COLSPAN="3">f</TD>
  </TR>
</TABLE>>]
		struct1:f1 -> struct2:f0
		struct1:f2 -> struct3:here
}''')
        dot.render('test-output/html.gv')
