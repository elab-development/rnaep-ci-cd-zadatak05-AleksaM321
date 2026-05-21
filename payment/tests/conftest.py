import sys
from unittest.mock import MagicMock

# Pravimo lažni Redis objekat sa svim potrebnim metodama
fake_redis = MagicMock()
fake_redis.xadd = MagicMock(return_value="mock-id-123")
fake_redis.xgroup_create = MagicMock(return_value=True)
fake_redis.xreadgroup = MagicMock(return_value=[])
fake_redis.get = MagicMock(return_value=None)
fake_redis.set = MagicMock(return_value=True)
fake_redis.hgetall = MagicMock(return_value={})
fake_redis.hset = MagicMock(return_value=1)
fake_redis.flushall = MagicMock(return_value=True)
fake_redis.httl = MagicMock(return_value=[])  # Za redis_om TTL
fake_redis.ping = MagicMock(return_value=True)  # Dodajemo ping

# Pravimo lažni database modul
mock_database = MagicMock()
mock_database.redis = fake_redis

# Zamenjujemo database modul PRE svega
sys.modules['database'] = mock_database

# NE mockujemo 'redis' modul - neka ostane pravi redis
# SAMO ako redis nije instaliran, onda bi trebalo mockovati
# Ali pošto smo instalirali redis, ne treba nam to