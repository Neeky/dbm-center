from django.test import TestCase, RequestFactory, Client
from .views import AgentsView
from .models import Agent
from django.utils.timezone import now

# Create your tests here.

class AgentViewTestCase(TestCase):
    """
    """
    def setup(self):
        Agent.objects.create(host="127.0.0.1", version='0.0.1', port=8086, register_at=now(), heartbeat_at=now())

    def test_get_all_agents(self):
        """
        """
        c = Client()
        response = c.get("/apis/agents/")
        self.assertEqual(response.status_code, 200)
        print(response.json())


