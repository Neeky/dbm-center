from django.test import TestCase, Client

# Create your tests here.


class AgentsViewTestCase(TestCase):
    """
    """
    
    def setup(self):
        """
        """
        pass

    def test_given_agents_is_empty_when_query_all_then_return_empty(self):
        """
        given: 数据库中没有任何一条 agent 的记录
        when: 查询所有 agent 信息的时候
        then: 返回一个空的列表

        期待的返回如下
        {
            agent:[],
            message:''
        }
        """
        client = Client()
        response = client.get("/apis/agents/")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data['agents']), 0)

        self.assertIn('message', data)
