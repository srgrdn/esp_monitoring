# Дашборд: ESP Analytics

Расширенный аналитический обзор, с фильтрацией по устройствам (label `instance`), корреляциями и квантилями.

## Источник данных

- Datasource: `VictoriaMetrics`.
- Переменная `$device`: `label_values(rssi, instance)`, поддерживает All (`.*`) и мультивыбор.

## Панели и метрики

- **Current status snapshot** — stat, последние значения (5m окно): `rssi`, `temp`, `rtt`, `packet_loss`, `http_status`, `network_type`.
- **RSSI with thresholds** — timeseries `rssi{instance=~"$device"}` с порогом -90.
- **Temperature with thresholds** — timeseries `temp{instance=~"$device"}` с порогами 15/30.
- **RTT and Packet Loss (dual axis)** — timeseries `rtt` (пороги 200/400) + `packet_loss` (порог 5) на правой оси.
- **HTTP status over time** — timeseries `http_status`.
- **RTT vs RSSI (overlay)** — оверлей `rtt` и `rssi` (вторая ось) для визуальной корреляции.
- **RSSI vs Temp (overlay)** — оверлей `rssi` и `temp` (вторая ось).
- **Min/Max/Avg (last 30m)** — stat: `min/max/avg` по rssi/temp, `avg` по rtt/packet_loss за 30m.
- **RTT p95 / p99 (15m window)** — `quantile_over_time(0.95|0.99, rtt[15m])`.
- **Alerts fired (per minute)** — `sum by (alertname) (increase(ALERTS{alertstate="firing"}[1m]))`.
- **Latest per instance (5m window)** — table с `last_over_time` по rssi/temp/rtt/packet_loss/http_status/network_type.

## Аналитика и применение

- Быстрый поиск причин деградаций: смотрите корреляции RTT↔RSSI, RSSI↔Temp.
- Оценка стабильности: p95/p99 RTT и Packet Loss пороги.
- Контроль качества связи: по алертам и частоте срабатываний.
- Фильтрация по `$device` — сравнение нескольких инстансов или агрегировано (All).
