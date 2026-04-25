#!/usr/bin/env bash
set -euo pipefail

command="${1:-}"

case "$command" in
  morning-today)
    just display-morning-today
    ;;

  evening-today)
    just display-evening-today
    ;;

  morning-tomorrow)
    just display-morning-tomorrow
    ;;

  nasa)
    just display-nasa
    ;;

  random-image)
    just display-random-private-image
    ;;

  sync)
    just sync
    ;;

  ""|help|--help|-h)
    echo "Usage: docker run --rm eink-display <command>"
    echo
    echo "Commands:"
    echo "  morning-today"
    echo "  evening-today"
    echo "  morning-tomorrow"
    echo "  nasa"
    echo "  random-image"
    echo "  sync"
    ;;

  *)
    echo "Unknown command: $command" >&2
    echo "Run with 'help' to see available commands." >&2
    exit 1
    ;;
esac
