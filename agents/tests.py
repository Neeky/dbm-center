from django.test import TestCase, Client
from django.utils import timezone


from .models import Agent
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

class AgentModelTestCase(TestCase):
    """
    针对 Agent 这个 model 的测试
    """

    def setUp(self) -> None:
        """
        """
        now = timezone.now()
        self.agent_not_time_out = Agent.objects.create(host="127.0.0.1", heartbeat_at=now - timezone.timedelta(seconds=10))
        self.agent_time_out = Agent.objects.create(host="127.0.0.2", heartbeat_at=now - timezone.timedelta(seconds=12))

    def test_given_agent_heartbeat_at_when_check_agent_is_alive_then_return_false(self):
        """
        given: agent 心跳上报超时(数据库里面保存的值与，当前时间之前差大于 11s )
        when: 检查 agent 是不是活着的
        then: Flase
        """
        # now = timezone.now()
        # now = now - timezone.timedelta(seconds=12)
        # agent = Agent.(heartbeat_at=now)
        self.assertFalse(self.agent_time_out.is_alive)

    def test_given_agent_heartheat_at_not_timeout_when_check_agent_is_alive_then_return_true(self):
        """
        given: agent 的心路上报时间为 10 秒以前
        when: 检查 agent 是不是活着的
        then: True
        """
        now = timezone.now()
        now = now - timezone.timedelta(seconds=10)
        agent = Agent(heartbeat_at=now)
        self.assertTrue(self.agent_not_time_out.is_alive)
