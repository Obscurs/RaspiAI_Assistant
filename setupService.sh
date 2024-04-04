#!/bin/bash

SERVICE_NAME=ai_service.service

mkdir -p $HOME/.config/system/user

cat <<EOF > $HOME/.config/systemd/user/$SERVICE_NAME
[Unit]
Description=AI Script Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/admin/Desktop/RaspiAI_Assistant
ExecStart=/home/admin/Desktop/RaspiAI_Assistant/env/bin/python3 main.py
Environment="PATH=/home/admin/Desktop/RaspiAI_Assistant/env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Restart=on-failure

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload

systemctl --user enable $SERVICE_NAME

systemctl --user start $SERVICE_NAME

echo "service created, enabled and started"
