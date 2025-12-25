#!/bin/bash

echo "✓ Validating BL1NK Monorepo Structure..."
echo ""

REQUIRED_DIRS=(
  "apps" "packages" "skills" "mcp" "docs" "tests" "tools" "config"
  ".config" ".local"
)

REQUIRED_FILES=(
  "README.md" "Makefile" "package.json" ".gitignore" ".editorconfig"
  "pnpm-workspace.yaml"
)

SKILL_PHASES=(
  "skills/phase-1-critical"
  "skills/phase-2-integration"
  "skills/phase-3-platform"
  "skills/phase-4-advanced"
)

errors=0

# Check required directories
echo "📁 Checking directories..."
for dir in "${REQUIRED_DIRS[@]}"; do
  if [ -d "$dir" ]; then
    echo "  ✓ $dir/"
  else
    echo "  ✗ MISSING: $dir/"
    ((errors++))
  fi
done

# Check required files
echo ""
echo "📄 Checking files..."
for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "  ✓ $file"
  else
    echo "  ✗ MISSING: $file"
    ((errors++))
  fi
done

# Check skill phases
echo ""
echo "🎯 Checking skill phases..."
for phase in "${SKILL_PHASES[@]}"; do
  if [ -d "$phase" ]; then
    echo "  ✓ $phase/"
  else
    echo "  ✗ MISSING: $phase/"
    ((errors++))
  fi
done

echo ""
if [ $errors -eq 0 ]; then
  echo "✅ Monorepo structure validated successfully!"
  exit 0
else
  echo "❌ Found $errors validation errors"
  exit 1
fi
