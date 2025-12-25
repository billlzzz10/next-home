# BL1NK Skill Implementation Checklist

Comprehensive checklist for creating and validating BL1NK skills.

## Pre-Implementation

- [ ] Identify phase (Phase 1-4)
- [ ] Review similar skills in `references/blk-examples.md`
- [ ] Check integration points needed
- [ ] Team assignment (1-3 developers based on phase)
- [ ] Estimate effort (based on phase and pattern)

## Step 1: Planning

- [ ] Define concrete usage examples
- [ ] Identify required scripts
- [ ] Plan references/documentation
- [ ] Plan assets/templates if needed
- [ ] Create manifest.json entry (draft)

## Step 2: Initialize Skill

- [ ] Create skill directory structure
- [ ] Copy SKILL.md template
- [ ] Fill in basic metadata
- [ ] Add reference to phase in SKILL.md

## Step 3: Implement Scripts

- [ ] Create scripts/ directory
- [ ] Implement main run.py
- [ ] Add JSON input/output handling
- [ ] Add error handling
- [ ] Add testing/validation code

### Script Checklist

- [ ] Accept JSON from stdin
- [ ] Parse input parameters
- [ ] Validate input
- [ ] Execute main logic
- [ ] Handle errors gracefully
- [ ] Output valid JSON
- [ ] Test with sample inputs

## Step 4: Add References

- [ ] Create references/ directory
- [ ] Add pattern reference (e.g., blk-patterns.md snippet)
- [ ] Add integration guide (if needed)
- [ ] Add API documentation (if external service)
- [ ] Link to workspace resources

## Step 5: Create Assets

- [ ] Create assets/ directory (if templates needed)
- [ ] Add boilerplate/template files
- [ ] Add example configurations
- [ ] Add checklist templates (if complex)

## Step 6: Write SKILL.md Body

- [ ] Introduction and purpose
- [ ] Core principles explanation
- [ ] Step-by-step usage guide
- [ ] Bundled resources documentation
- [ ] BL1NK context section
- [ ] Integration points section
- [ ] Testing section with examples
- [ ] Troubleshooting section
- [ ] Related skills/resources

## Step 7: Test Implementation

### Unit Tests

- [ ] Basic operation test
- [ ] Error handling test
- [ ] Edge case test
- [ ] Invalid input test

### Integration Tests

- [ ] Test with workspace patterns
- [ ] Test manifest.json entry
- [ ] Test external integrations (if any)

### Manual Testing

- [ ] Run scripts with samples
- [ ] Verify JSON output format
- [ ] Check error messages
- [ ] Test with real data

## Step 8: Update Manifest

- [ ] Add to `/home/user/skills/manifest.json`
- [ ] Add to `/home/user/skills/skills.json`
- [ ] Update `/home/user/skills/README.md`

### Manifest Entry

```json
{
  "name": "my-skill",
  "title": "My Skill",
  "description": "...",
  "author": "BL1NK Team",
  "version": "1.0.0",
  "tags": ["tag1", "tag2"],
  "category": "category",
  "complexity": "low|medium|high",
  "estimated_runtime": 30,
  "phase": "1|2|3|4"
}
```

## Step 9: Validate

- [ ] Run `scripts/validate_blk_skill.py my-skill`
- [ ] Run `scripts/quick_validate.py my-skill`
- [ ] Check for warnings/issues
- [ ] Fix any failures

## Step 10: Package

- [ ] Run `scripts/package_skill.py /path/to/skill`
- [ ] Verify .skill file created
- [ ] Check file is valid zip
- [ ] Test unzipping contents

## Step 11: Documentation

- [ ] Complete SKILL.md
- [ ] Add usage examples
- [ ] Add troubleshooting guide
- [ ] Add related skills list
- [ ] Review for clarity

## Step 12: Final Validation

- [ ] All tests passing
- [ ] Documentation complete
- [ ] Manifest entries correct
- [ ] Code reviewed
- [ ] No hardcoded credentials
- [ ] Error messages user-friendly

## Phase-Specific Checklist

### Phase 1 Skills

- [ ] No external dependencies
- [ ] High business value
- [ ] Can run standalone
- [ ] Clear single purpose
- [ ] Minimal configuration

### Phase 2 Skills

- [ ] External integration defined
- [ ] Client library available
- [ ] Error handling for API failures
- [ ] Credentials management clear
- [ ] Fallback logic included

### Phase 3 Skills

- [ ] Orchestration logic clear
- [ ] Dependency management defined
- [ ] Error propagation strategy
- [ ] Data flow documented
- [ ] Interaction patterns clear

### Phase 4 Skills

- [ ] Optional features documented
- [ ] Advanced use cases covered
- [ ] Performance considerations
- [ ] Extensibility planned
- [ ] Future enhancement notes

## Integration Checklist

### Notification Integration

- [ ] NotificationManager imported correctly
- [ ] Credentials handled securely
- [ ] Supported channels: Slack, Linear, ClickUp
- [ ] Error handling for delivery failures
- [ ] Documentation with examples

### GitHub Integration

- [ ] GithubClient imported correctly
- [ ] Authentication configured
- [ ] Error handling for API calls
- [ ] Rate limiting considered
- [ ] Documentation with API examples

### POE Protocol Integration

- [ ] FastAPI setup correct
- [ ] POE protocol handlers implemented
- [ ] SSE event streaming working
- [ ] Error responses formatted correctly
- [ ] Documentation with examples

### Skill Orchestration

- [ ] SkillLoader imported correctly
- [ ] Skill discovery working
- [ ] Data flow between skills
- [ ] Error handling strategies
- [ ] Documentation with examples

## Code Quality

- [ ] No hardcoded credentials
- [ ] No hardcoded paths
- [ ] Proper error messages
- [ ] Code comments where needed
- [ ] DRY principles followed
- [ ] No unused imports
- [ ] Consistent formatting

## Documentation Quality

- [ ] Clear and concise
- [ ] Examples provided
- [ ] Use cases documented
- [ ] Integration points clear
- [ ] Troubleshooting included
- [ ] Related resources linked
- [ ] No typos/grammar errors

## Ready for Production

- [ ] ✅ All tests passing
- [ ] ✅ Documentation complete
- [ ] ✅ Manifest updated
- [ ] ✅ Code reviewed
- [ ] ✅ Validated with scripts
- [ ] ✅ No blockers identified
- [ ] ✅ Ready for next phase/release

