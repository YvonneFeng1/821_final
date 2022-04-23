"""Connect to Redis database."""


from redis import Redis

conn = Redis()

bid_value = conn.get("BID")
pid_value = conn.get("PID")
init_bid = 1 if bid_value is None else int(bid_value.decode("utf-8"))
init_pid = 1 if pid_value is None else int(pid_value.decode("utf-8"))
conn.set("BID", init_bid)
conn.set("PID", init_pid)
