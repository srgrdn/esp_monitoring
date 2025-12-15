# Минимальная система мониторинга (VictoriaMetrics + Grafana + Alertmanager)

Синтетический стенд эмулирует ESP32+GSM+BME280, собирает метрики каждые 5 сек, пишет их в VictoriaMetrics, визуализирует в Grafana и шлет алерты через Alertmanager.

## Что внутри

- `docker-compose.yml` — все сервисы (VictoriaMetrics, vmagent, vmalert, Alertmanager, Grafana, Mailhog, генератор метрик).
- `generator/` — Python-скрипт, отдающий метрики в формате Prometheus на `:9100/metrics`.
- `config/vmagent/config.yml` — vmagent скрейпит генератор и пишет в VictoriaMetrics.
- `config/vmalert/rules.yml` — правила алертов (rssi, temp, packet_loss).
- `config/alertmanager/alertmanager.yml` — фиктивные уведомления: Webhook и Email через Mailhog.
- `config/grafana/*` — провиженинг датасорса и готового дашборда.

## Быстрый старт

```bash
cd /home/s_grudinin/code/Ops/monitoring_esp
docker-compose up -d --build
```

Доступы:

- Grafana: `http://localhost:3000` (admin / admin). Дашборд `ESP Monitoring` уже импортирован.
- VictoriaMetrics UI/API: `http://localhost:8428`
- vmagent UI: `http://localhost:8429`
- Alertmanager: `http://localhost:9093`
- Mailhog веб-интерфейс (просмотр писем): `http://localhost:8025`

## Метрики и алерты

- `rssi` (дБм): алерт при `< -90`
- `temp` (°C): алерт при `> 30` или `< 15`
- `packet_loss` (%): алерт при `> 5`
- Дополнительно: `rtt`, `http_status`, `network_type`, `esp_timestamp`

Скрипт каждые 5 секунд обновляет показатели и периодически добавляет ухудшения, чтобы срабатывали алерты.

## Как проверить

1. Убедитесь, что контейнеры работают: `docker-compose ps`.
2. В Grafana на дашборде дождитесь периодического провала RSSI/роста потерь — должны появиться алерты.
3. В Alertmanager увидите активные алерты. Email-уведомления можно смотреть в Mailhog (Inbox). Webhook в примере уходит на `http://example.com/alert-webhook` — при необходимости замените на реальный URL.

## Настройки под себя

- Email/Telegram: замените блоки в `config/alertmanager/alertmanager.yml` (для Telegram используйте `telegram_configs` с вашим ботом/чатом).
- Порты/ретеншн: правятся в `docker-compose.yml`.
- Дашборд: JSON в `config/grafana/dashboards_json/esp_monitoring.json`.

## Остановка

```bash
docker-compose down
```
