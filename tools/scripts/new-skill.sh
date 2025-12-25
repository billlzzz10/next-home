#!/bin/bash

PHASE=$1
NAME=$2

if [ -z "$PHASE" ] || [ -z "$NAME" ]; then
  echo "Usage: make new-skill PHASE=1 NAME=my-skill"
  echo ""
  echo "PHASE can be:"
  echo "  1 - Critical foundation (phase-1-critical)"
  echo "  2 - Integration (phase-2-integration)"
  echo "  3 - Platform (phase-3-platform)"
  echo "  4 - Advanced (phase-4-advanced)"
  exit 1
fi

case $PHASE in
  1) PHASE_DIR="skills/phase-1-critical" ;;
  2) PHASE_DIR="skills/phase-2-integration" ;;
  3) PHASE_DIR="skills/phase-3-platform" ;;
  4) PHASE_DIR="skills/phase-4-advanced" ;;
  *) echo "Invalid phase: $PHASE"; exit 1 ;;
esac

SKILL_PATH="$PHASE_DIR/$NAME"

if [ -d "$SKILL_PATH" ]; then
  echo "✗ Skill already exists: $SKILL_PATH"
  exit 1
fi

mkdir -p "$SKILL_PATH/scripts"
mkdir -p "$SKILL_PATH/references"
mkdir -p "$SKILL_PATH/assets"

cat > "$SKILL_PATH/SKILL.md" << SKILL_MD
---
name: $NAME
description: [Add description]
version: 1.0.0
author: BL1NK Team
tags: [tag1, tag2]
license: Complete terms in LICENSE.txt
---

# $NAME

[Add documentation here]

## Purpose

[Explain what this skill does]

## How It Works

[Explain the workflow]

## Testing

### Test Case 1
Input: [example]
Output: [expected result]
SKILL_MD

cat > "$SKILL_PATH/scripts/run.py" << 'RUN_PY'
#!/usr/bin/env python3
import json
import sys

# Read input
data = json.loads(sys.stdin.read())

try:
    # TODO: Implement your skill logic here
    result = {"status": "success", "message": "Skill executed"}
    print(json.dumps(result))
except Exception as e:
    error_result = {"status": "error", "message": str(e)}
    print(json.dumps(error_result))
    sys.exit(1)
RUN_PY

chmod +x "$SKILL_PATH/scripts/run.py"

echo "✓ Created skill: $SKILL_PATH/"
echo ""
echo "Next steps:"
echo "  1. Edit SKILL.md with your skill details"
echo "  2. Implement scripts/run.py"
echo "  3. Add references and assets as needed"
echo "  4. Test with: bash tools/scripts/validate-monorepo.sh"
