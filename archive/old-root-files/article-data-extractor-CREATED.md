# ✅ Article Data Extractor Skill - Creation Complete

## Skill Created Successfully

Your new **article-data-extractor** skill has been created and is ready to use!

**Location:** `~/skills/custom/article-data-extractor/`

---

## What This Skill Does

Extracts and organizes numerical data from news articles and analytical content into comprehensive, categorized Markdown tables with full contextual information.

### Key Capabilities:
- ✓ Identifies ALL numerical data (numbers, percentages, statistics, metrics, rankings, time-series)
- ✓ Captures full context for each data point (entity, timeframe, source, notes)
- ✓ Organizes data into logical categories
- ✓ Generates Markdown tables with proper formatting
- ✓ Creates data summaries and overviews
- ✓ Handles complex data scenarios (ranges, comparisons, estimates)

---

## Skill Components

### 📄 Core Files

1. **SKILL.md** - Main skill definition with complete workflow
   - 6-step extraction workflow
   - Output guidelines and format specifications
   - Context extraction requirements
   - Data categorization strategy

2. **OVERVIEW.md** - Comprehensive skill guide (this directory)
   - Skill summary and use cases
   - Complete component breakdown
   - Workflow overview
   - Getting started guide

### 📚 Reference Guides

3. **references/quick-reference.md** - 1-page quick lookup
   - 5-minute extraction workflow
   - Column definitions with examples
   - Common category names
   - Format checklist
   - Problem-solving matrix

4. **references/extraction-patterns.md** - Advanced patterns
   - Common data categories with examples
   - How to handle complex scenarios
   - 10+ category types
   - Quality checklist

5. **references/example-scenarios.md** - Real-world examples
   - 5 complete extraction examples:
     * Economic report (China GDP, employment, inflation)
     * Tech company (Apple revenue breakdown)
     * Market research (AI market projections)
     * Healthcare (Clinical trial data)
     * Sports (Tournament statistics)
   - Each with source text and extracted tables

### 🛠️ Tools

6. **scripts/extract_data.py** - Automated pattern detection
   - Identifies 10+ numerical data patterns
   - Finds numbers in context
   - Exports to CSV for manual categorization
   - Usage: `python extract_data.py article.txt`

### 📋 Assets

7. **assets/extraction_template.md** - Reusable template
   - Article metadata fields
   - Extraction checklist
   - Multiple category tables
   - Notes and observations section

---

## Quick Start

### For Manual Extraction:
1. Open **references/quick-reference.md** for 5-minute workflow
2. Use **assets/extraction_template.md** to structure your work
3. Review **references/example-scenarios.md** for real-world patterns

### For Assisted Extraction:
1. Run: `python scripts/extract_data.py article.txt`
2. Review extracted patterns
3. Manually categorize and create tables using template

### For Complex Articles:
1. Check **references/extraction-patterns.md** for handling edge cases
2. Use **SKILL.md** for complete workflow details
3. Refer to **references/example-scenarios.md** for similar cases

---

## Example Usage

**Input:** Article text about quarterly earnings

**Process:** 
1. Read article completely
2. Identify data points (revenue: $81.8B, growth: 4.3%, share: 52%)
3. Extract context (Apple, Q3 2023, YoY comparison)
4. Categorize (Financial Performance, Revenue Breakdown)
5. Create tables

**Output:**

```markdown
### Data Summary
- **Total data points extracted:** 6
- **Main categories:** Financial Performance, Growth Metrics
- **Data focus:** Apple Q3 2023 quarterly results

### Financial Performance

| Data Description | Value | Unit/% | Related Entity | Time Range | Additional Notes |
|------------------|-------|--------|-----------------|------------|-----------------|
| Total revenue | 81.8 | Billion USD | Apple | Q3 2023 | Record quarter, up 4.3% YoY |
| iPhone revenue | 42.6 | Billion USD | Apple | Q3 2023 | 52% of total revenue |
| Services revenue | 16.9 | Billion USD | Apple | Q3 2023 | Up 16% YoY |
```

---

## File Structure

```
~/skills/custom/article-data-extractor/
├── SKILL.md                           ← Main skill definition
├── OVERVIEW.md                        ← This skill guide
├── scripts/
│   └── extract_data.py                ← Pattern detection tool
├── references/
│   ├── quick-reference.md             ← 1-page quick guide
│   ├── extraction-patterns.md          ← Data categories & patterns
│   └── example-scenarios.md            ← 5 real-world examples
└── assets/
    └── extraction_template.md          ← Reusable template
```

---

## Key Features

| Feature | Benefit |
|---------|---------|
| **Comprehensive** | Extracts all numerical content with full context |
| **Organized** | Logically categorizes data for easy analysis |
| **Contextual** | Includes entities, timeframes, and sources |
| **Accurate** | Extraction limited to article content only |
| **Reusable** | Template and script support repeated workflows |
| **Scalable** | Works with single articles or batch datasets |
| **Documented** | 5 example scenarios show real applications |
| **Flexible** | Handles economic, financial, tech, health, sports data |

---

## Common Use Cases

✓ **Financial Analysis** - Extract quarterly earnings, growth rates, market metrics
✓ **Economic Research** - GDP, inflation, employment, trade data
✓ **Market Intelligence** - Market share, sizing, competitive data
✓ **Data Journalism** - Convert articles to structured datasets
✓ **Research & Analysis** - Build datasets from multiple articles
✓ **Business Intelligence** - Create data summaries for presentations
✓ **Academic Research** - Extract statistics from published articles
✓ **Healthcare/Science** - Clinical trial results, medical statistics

---

## Tips for Best Results

1. **Read completely** - Scan entire article multiple times
2. **Be thorough** - Extract ALL numerical data, not just highlights
3. **Keep context** - Always note entity, timeframe, and source
4. **Use categories** - Group logically based on article focus
5. **Verify accuracy** - Double-check all numbers from article
6. **Note caveats** - Include estimates, comparisons, and methodology
7. **Stay focused** - Only extract from provided article content
8. **Format cleanly** - Use consistent table formatting

---

## Getting Help

- **Quick answers:** See references/quick-reference.md
- **Complex cases:** See references/extraction-patterns.md
- **Examples:** See references/example-scenarios.md
- **Full workflow:** See SKILL.md
- **Templates:** See assets/extraction_template.md
- **Automation:** Run scripts/extract_data.py

---

## Next Steps

1. **Try it out** - Use the template to extract data from an article
2. **Run the script** - Test `extract_data.py` on sample text
3. **Study examples** - Review the 5 scenarios in example-scenarios.md
4. **Practice** - Extract data from different article types
5. **Build datasets** - Combine multiple extractions

---

**Skill Ready to Use!** 🎯

The article-data-extractor skill is fully configured and documented. Start extracting structured data from your articles today!

For questions about specific extractions, refer to the appropriate reference guide or example scenario.
