"""Passive local telemetry collector.
It reads OS connection metadata and resource statistics.
It does not generate traffic or perform active scanning.
"""
import time
from datetime import datetime, timezone
import psutil

def collect_snapshot():
    conns = psutil.net_connections(kind="inet")
    established = sum(1 for c in conns if c.status == psutil.CONN_ESTABLISHED)
    listening = sum(1 for c in conns if c.status == psutil.CONN_LISTEN)
    remote = len({(c.raddr.ip, c.raddr.port) for c in conns if c.raddr})
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "connections_total": len(conns),
        "connections_established": established,
        "listening_sockets": listening,
        "unique_remote_endpoints": remote,
        "cpu_percent": psutil.cpu_percent(interval=0.2),
        "memory_percent": psutil.virtual_memory().percent,
    }

def stream(interval=2.0):
    while True:
        yield collect_snapshot()
        time.sleep(interval)
