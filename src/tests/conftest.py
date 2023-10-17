import mock
import pytest
from fakeredis import aioredis, FakeRedis


@pytest.fixture(autouse=True)
def mock_get_redis_client():
    with mock.patch("src.redis_session.RedisCluster", FakeRedis):
        yield


@pytest.fixture(autouse=True)
def mock_get_aredis_client():
    with mock.patch("src.redis_session.ARedisCluster", aioredis.FakeRedis):
        yield


@pytest.fixture
def clear_state():
    # cleaning state
    from src.microwave import state_machine

    state_machine.machine.set_state("off")
    state_machine.current_power = 600
    state_machine.current_time = 60
