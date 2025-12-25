.PHONY: help setup install dev build test lint format validate deploy clean

help:
	@echo "BL1NK Monorepo - Available Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup              Full environment setup"
	@echo "  make install            Install dependencies only"
	@echo ""
	@echo "Development:"
	@echo "  make dev                Run all services"
	@echo "  make dev-api            Run API server"
	@echo "  make dev-web            Run web portal"
	@echo ""
	@echo "Building:"
	@echo "  make build              Build all packages"
	@echo "  make build-api          Build API"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test               Run all tests"
	@echo "  make test-unit          Unit tests only"
	@echo "  make lint               Lint all code"
	@echo "  make format             Format code"
	@echo "  make validate           Validate structure"
	@echo ""
	@echo "Skills:"
	@echo "  make new-skill PHASE=1 NAME=my-skill"
	@echo "  make list-skills"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy             Deploy to production"
	@echo "  make clean              Clean build artifacts"

setup:
	@echo "🔧 Setting up BL1NK monorepo..."
	@mkdir -p .local/{cache,credentials,temp}
	@echo "📦 Installing dependencies..."
	@pnpm install || npm install
	@echo "✅ Setup complete!"

install:
	@pnpm install || npm install

dev:
	@echo "🚀 Starting all services..."
	@echo "Note: Use specific targets (dev-api, dev-web, dev-cli)"

dev-api:
	@echo "🚀 Starting API server..."
	@cd apps/api-server && pnpm dev

dev-web:
	@echo "🚀 Starting web portal..."
	@cd apps/web-portal && pnpm dev

build:
	@echo "🏗️ Building all packages..."
	@pnpm -r build

test:
	@echo "🧪 Running all tests..."
	@pnpm -r test

test-unit:
	@echo "🧪 Running unit tests..."
	@pnpm -r test:unit

lint:
	@echo "🔍 Linting code..."
	@pnpm -r lint

format:
	@echo "✨ Formatting code..."
	@pnpm -r format

validate:
	@echo "✓ Validating monorepo structure..."
	@bash tools/scripts/validate-monorepo.sh

new-skill:
	@bash tools/scripts/new-skill.sh $(PHASE) $(NAME)

list-skills:
	@find skills/phase-* -maxdepth 1 -type d -printf '%f\n' | sort

deploy:
	@echo "🚀 Deploying to production..."
	@bash tools/scripts/deploy.sh

clean:
	@echo "🧹 Cleaning build artifacts..."
	@pnpm -r clean
	@rm -rf dist build

.DEFAULT_GOAL := help
