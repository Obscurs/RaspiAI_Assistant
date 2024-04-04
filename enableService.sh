#!/bin/bash

SERVICE_NAME=ai_service.service

systemctl --user enable $SERVICE_NAME

systemctl --user start $SERVICE_NAME