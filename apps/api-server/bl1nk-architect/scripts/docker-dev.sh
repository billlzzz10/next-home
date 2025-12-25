#!/bin/bash
case "$1" in
  build) docker-compose build ;;
  up) docker-compose up -d ;;
  down) docker-compose down ;;
  logs) docker-compose logs -f ;;
  health) docker-compose exec app python health_check.py ;;
  *) echo "Usage: $0 {build|up|down|logs|health}" ;;
esac
