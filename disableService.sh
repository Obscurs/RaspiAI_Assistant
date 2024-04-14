#!/bin/bash

SERVICE_NAME=ai_service.service

systemctl --user stop $SERVICE_NAME

systemctl --user disable $SERVICE_NAME

sudo systemctl enable lightdm