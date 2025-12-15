import random
import time

from prometheus_client import Gauge, start_http_server


# Gauges are Prometheus-compatible and will be scraped by vmagent.
rssi_gauge = Gauge("rssi", "Cellular signal strength in dBm")
network_type_gauge = Gauge("network_type", "Network type (1=GSM, 2=LTE)")
rtt_gauge = Gauge("rtt", "Server round-trip time in milliseconds")
packet_loss_gauge = Gauge("packet_loss", "Packet loss percentage")
http_status_gauge = Gauge("http_status", "HTTP status code from server")
temp_gauge = Gauge("temp", "Ambient temperature in Celsius")
timestamp_gauge = Gauge("esp_timestamp", "Synthetic device timestamp")


def jitter(value: float, low: float, high: float, delta: float) -> float:
    """Clamp value inside [low, high] with a small random delta."""
    value += random.uniform(-delta, delta)
    return max(low, min(high, value))


def generate_metrics():
    # Start with sane defaults
    rssi = -70.0
    temp = 7.0
    last_temp_update = time.time()
    temp_update_period = 24 * 60 * 60  # once per 24h
    rtt = 120.0
    packet_loss = 1.0
    http_status = 200.0
    network_type = 2.0  # 1=GSM, 2=LTE

    while True:
        # Randomly flip network type every few cycles
        if random.random() < 0.2:
            network_type = 1.0 if network_type == 2.0 else 2.0

        # Base fluctuations
        rssi = jitter(rssi, -100, -50, 2.5)
        # Температуру меняем очень редко — раз в сутки
        if time.time() - last_temp_update >= temp_update_period:
            temp = 6 + random.random() * 2
            last_temp_update = time.time()
        rtt = jitter(rtt, 50, 450, 15)
        packet_loss = jitter(packet_loss, 0, 10, 0.8)

        # Inject occasional degradations to trigger alerts
        if random.random() < 0.1:
            rssi = -95 + random.uniform(-3, 2)
        # Температура между обновлениями остаётся стабильной
        if random.random() < 0.08:
            packet_loss = 6 + random.random() * 3
        if random.random() < 0.05:
            http_status = 500.0
            rtt = min(700.0, rtt + 200)
        else:
            http_status = 200.0

        # Expose metrics
        rssi_gauge.set(rssi)
        network_type_gauge.set(network_type)
        rtt_gauge.set(rtt)
        packet_loss_gauge.set(packet_loss)
        http_status_gauge.set(http_status)
        temp_gauge.set(temp)
        timestamp_gauge.set(time.time())

        time.sleep(5)


if __name__ == "__main__":
    # Expose /metrics on port 9100
    start_http_server(9100)
    generate_metrics()

