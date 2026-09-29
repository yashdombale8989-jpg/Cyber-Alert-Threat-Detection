"""Passive local real-time telemetry collector."""
from datetime import datetime, timezone
import psutil

def collect_snapshot():
    conns = psutil.net_connections(kind="inet")
    established = sum(c.status == psutil.CONN_ESTABLISHED for c in conns)
    listening = sum(c.status == psutil.CONN_LISTEN for c in conns)
    remote = len({(c.raddr.ip, c.raddr.port) for c in conns if c.raddr})
    cpu = psutil.cpu_percent(interval=0.2)
    memory = psutil.virtual_memory().percent

    reasons = []
    if established >= 80: reasons.append("High number of established connections")
    if remote >= 60: reasons.append("Many unique remote endpoints")
    if listening >= 25: reasons.append("Many listening sockets")
    if cpu >= 95: reasons.append("Very high CPU utilization")
    if memory >= 95: reasons.append("Very high memory utilization")

    risk = "HIGH" if len(reasons) >= 2 else "MEDIUM" if reasons else "NORMAL"
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "connections_total": len(conns),
        "connections_established": established,
        "listening_sockets": listening,
        "unique_remote_endpoints": remote,
        "cpu_percent": cpu,
        "memory_percent": memory,
        "risk": risk,
        "reasons": reasons,
    }
