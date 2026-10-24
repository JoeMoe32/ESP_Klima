"""Read-only hardware acceptance test. Python standard library, no extra packages.

Usage: python tools/test_modbus_tcp.py [192.168.77.2]
"""
import http.client as http_client
import json
from pathlib import Path
import socket
import struct
import sys
import time

IP = sys.argv[1] if len(sys.argv) > 1 else "192.168.77.2"
report = {"ip": IP, "port": 502, "tests": {}}


def connect():
    return socket.create_connection((IP, 502), timeout=3)


def adu(tid, function=3, address=0, count=1, unit=1):
    return struct.pack(">HHHBBHH", tid, 0, 6, unit, function, address, count)


def read_exact(sock, count):
    data = b""
    while len(data) < count:
        block = sock.recv(count - len(data))
        if not block:
            raise AssertionError("Peer closed an incomplete response")
        data += block
    return data


def receive(sock, tid, unit=1):
    header = read_exact(sock, 6)
    actual_tid, protocol, size = struct.unpack(">HHH", header)
    assert actual_tid == tid and protocol == 0 and 2 <= size <= 254
    payload = read_exact(sock, size)
    assert payload[0] == unit
    return payload[1:]


def check(name, condition):
    report["tests"][name] = bool(condition)
    print(name, "PASS" if condition else "FAIL", flush=True)
    assert condition, name


def http(method, path, body=None):
    conn = http_client.HTTPConnection(IP, timeout=4)
    try:
        conn.request(method, path, body=body, headers={"Connection": "close"})
        response = conn.getresponse()
        return response.status, response.read()
    finally:
        conn.close()


def expect_closed(sock):
    try:
        return sock.recv(1) == b""
    except (ConnectionResetError, ConnectionAbortedError):
        return True
    except socket.timeout:
        return False


def run():
    with connect() as sock:
        sock.sendall(adu(101, count=64))
        pdu = receive(sock, 101)
        check("read_all_fc03", len(pdu) == 130 and pdu[:2] == b"\x03\x80")
        regs = struct.unpack(">64H", pdu[2:])
        report["registers"] = list(regs)
        report["values"] = {"temperature": struct.unpack(">h", pdu[20:22])[0] / 100,
                            "humidity": regs[10] / 100, "di": regs[29], "relays": regs[30],
                            "alarm": regs[39], "fault": regs[40], "ready": regs[41]}
        check("hcho_unavailable", regs[19] == regs[20] == 0x8000)
        sock.sendall(adu(102, 4, 29, 2))
        check("read_di_relays_fc04", receive(sock, 102) == b"\x04\x04" + struct.pack(">HH", regs[29], regs[30]))
        request = adu(103, 3, 39, 3)
        for block in (request[:2], request[2:7], request[7:]):
            sock.sendall(block)
            time.sleep(0.025)
        check("fragmented_request", receive(sock, 103)[:2] == b"\x03\x06")
        sock.sendall(adu(104) + adu(105, 4, 1))
        first, second = receive(sock, 104), receive(sock, 105)
        check("coalesced_requests", first[:2] == b"\x03\x02" and second[:2] == b"\x04\x02")
        for tid, name, function, address, count, error in [
            (106, "invalid_address", 3, 64, 1, 2),
            (107, "zero_quantity", 3, 0, 0, 3),
            (108, "unsupported_function", 1, 0, 1, 1),
            (109, "quantity_above_limit", 3, 0, 126, 3),
        ]:
            sock.sendall(adu(tid, function, address, count))
            check(name, receive(sock, tid) == bytes([function | 0x80, error]))
        sock.sendall(adu(110, unit=255))
        check("unit_255", receive(sock, 110, 255)[:2] == b"\x03\x02")
        # Keep this client connected while a second client and HTTP are active.
        with connect() as second:
            second.sendall(adu(111))
            check("two_tcp_clients", receive(second, 111)[:2] == b"\x03\x02")
            code, page = http("GET", "/")
            check("http_during_modbus", code == 200 and b"Sensorstation" in page)
        code, content = http("GET", "/api/status")
        status = json.loads(content)
        report["http_status"] = status
        check("http_live_status", code == 200 and status["temperature"] is not None and status["hcho"] is None and status["ip"] == IP)
        code, _ = http("POST", "/api/command", "status")
        check("web_service_requires_key", code == 403)
    for name, data in [
        ("invalid_protocol_closes", struct.pack(">HHH", 200, 1, 6)),
        ("invalid_short_length_closes", struct.pack(">HHH", 201, 0, 1)),
        ("oversized_length_closes", struct.pack(">HHH", 202, 0, 255)),
    ]:
        with connect() as sock:
            sock.sendall(data)
            check(name, expect_closed(sock))
    with connect() as sock:
        sock.sendall(adu(203)[:7])
        sock.settimeout(5)
        check("incomplete_frame_timeout", expect_closed(sock))
    with connect() as sock:
        sock.sendall(adu(204, 3, 39, 3))
        check("read_after_errors", receive(sock, 204)[:2] == b"\x03\x06")


try:
    run()
except Exception as error:
    report["error"] = f"{type(error).__name__}: {error}"
    print(report["error"], flush=True)
finally:
    target = Path(__file__).resolve().parents[1] / "docs/tcp-test.json"
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report.get("values", {}), indent=2))
raise SystemExit(1 if "error" in report or not all(report["tests"].values()) else 0)
