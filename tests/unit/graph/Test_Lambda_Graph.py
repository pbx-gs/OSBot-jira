from unittest import TestCase

from pbx_gs_python_utils.gs_elk.GS_Graph import GS_Graph
from pbx_gs_python_utils.gs_elk.Lambda_Graph import Lambda_Graph
from pbx_gs_python_utils.utils.Dev import Dev


class Test_Lambda_Graph(TestCase):
    def setUp(self):
        self.lambda_graph = Lambda_Graph()

    def test___init__(self):
        results = self.lambda_graph.save_to_elk.find_documents_of_type('unit-test')
        Dev.pprint(results)

    def test_get_gs_graph_by_name(self):
        graph = self.lambda_graph.get_gs_graph___by_name("test_save_gs_graph_____org_chart")
        assert graph.stats() == {'count_edges': 42, 'count_nodes': 59, 'size_puml': 5204}

    # def test_get_gs_graph_by_name__reload(self):
    #     graph = self.lambda_graph.get_gs_graph___by_name('sec-9696-up' )
    #     Dev.pprint(graph.nodes)



    def test_get_gs_graph_by_type(self):
        graph = self.lambda_graph.get_gs_graph___by_type("keys___['FACT-47']__up___depth_3")
        assert graph.stats() == {'count_edges': 24, 'count_nodes': 20, 'size_puml': 2509}

    def test_get_gs_graph___from_user(self):
        user = 'test-user'
        graph = GS_Graph().add_node("aaa").add_edge("aaa", "->", "bbb")
        self.lambda_graph.save_gs_graph(graph, user = user)
        graph = self.lambda_graph.get_gs_graph___from_user(user)
        assert graph.stats() == {'count_edges': 1, 'count_nodes': 1, 'size_puml': 88}

    def test_get_graph_png___by_name(self):
        name  = "test_save_gs_graph_____org_chart"
        data  = self.lambda_graph.get_graph_png___by_name(name)
        assert len(data['png_base64']) > 300000


    def test_handle_lambda_event(self):
        command = 'last_5_graphs'
        payload = {
            "params": [command],
            "data": {"channel": "DDKUZTK6X"}
        }
        self.lambda_graph.handle_lambda_event(payload)

    def test_send_graph_to_slack___by_type(self):
        result = self.lambda_graph.send_graph_to_slack___by_type("keys___['FACT-47']__up___depth_3", "DDKUZTK6X")
        assert result == 'image sent .... '


    def test_get_last_n_graphs_of_type(self):
        results = self.lambda_graph.get_last_n_graphs_of_type('lambda_graph' ,10)
        print()
        for item in results:
            print('{0} {1} - {2}'.format(item["id"],item['value'].get('date'), item['value'].get('doc_data').get('type')))
            #Dev.pprint(item)
            #D[graph['date']]={ "_id": _id, "graph": 'graph'}

        #Dev.pprint(sorted(indexed_by_date.keys(),"desc")) #list(results.values()).pop())

    def test_save_graph(self):
        nodes      = ['a','b']
        edges      = [('a', 'goes to','b')]
        extra_data = None
        graph_id   = None # 'unit_test_test_save_graph_nodes_edges'
        graph_name = 'test_save_graph_nodes_edges'
        graph_type = 'unit-test'
        result     = self.lambda_graph.save_graph(nodes, edges, extra_data, graph_id, graph_name, graph_type)
        Dev.pprint(result)

    def test_save_gs_graph(self):
        graph = GS_Graph()
        graph.add_node("aaa")
        graph.add_edge("aaa","->","bbb")
        result = self.lambda_graph.save_gs_graph(graph, "test_save_gs_graph", "from unit test")
        Dev.pprint(result)

    def test_render_and_save_gs_graph_____org_chart(self):
        graph = GS_Graph()
        is_a_manager_nodes = graph.api_issues.link_types('it_assets')['is manager of'].keys()
        graph.add_nodes(is_a_manager_nodes)
        graph.add_linked_issues_of_type('is manager of')
        graph.render_and_save_to_elk   ("test_save_gs_graph_____org_chart", "from unit test")

        #self.lambda_graph.save_gs_graph(graph, "test_save_gs_graph_____org_chart", "from unit test")


    #def test_lambda_update(self):
    #    self.lambda_graph = Lambda('lambdas.gsbot.gsbot_graph').update()