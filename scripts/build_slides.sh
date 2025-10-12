#!/usr/bin/env bash

# ============================================
# Build Slides Script
# ============================================
# Converts Marp Markdown slides to HTML
# Usage: ./scripts/build_slides.sh
# ============================================

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Building Marp Slides${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if marp is installed
if ! command -v marp &> /dev/null; then
    echo -e "${RED}❌ Marp CLI not found!${NC}"
    echo ""
    echo "Please install Marp CLI:"
    echo "  npm install -g @marp-team/marp-cli"
    echo ""
    exit 1
fi

# Get marp version
MARP_VERSION=$(marp --version)
echo -e "${GREEN}✓${NC} Marp CLI detected: ${MARP_VERSION}"
echo ""

# Create output directory if it doesn't exist
OUTPUT_DIR="slides/output"
mkdir -p "$OUTPUT_DIR"
echo -e "${GREEN}✓${NC} Output directory: ${OUTPUT_DIR}"
echo ""

# Define slide files
SLIDES=(
    "slides/day1_kickoff.md"
    "slides/day1_block_a_intro.md"
    "slides/day1_block_b_intro.md"
    "slides/day2_kickoff.md"
    "slides/day2_block_a_intro.md"
    "slides/day2_block_b_intro.md"
)

# Build each slide deck
for SLIDE_FILE in "${SLIDES[@]}"; do
    if [ -f "$SLIDE_FILE" ]; then
        BASENAME=$(basename "$SLIDE_FILE" .md)
        OUTPUT_FILE="${OUTPUT_DIR}/${BASENAME}.html"

        echo -e "${BLUE}Building:${NC} ${SLIDE_FILE}"

        # Build with theme directory
        marp "$SLIDE_FILE" \
            --theme-set slides/themes/ceu-theme.css \
            --html \
            -o "$OUTPUT_FILE"

        if [ $? -eq 0 ]; then
            echo -e "  ${GREEN}✓${NC} Generated: ${OUTPUT_FILE}"
        else
            echo -e "  ${RED}✗${NC} Failed to build ${SLIDE_FILE}"
            exit 1
        fi
        echo ""
    else
        echo -e "${YELLOW}⚠${NC}  Skipping (not found): ${SLIDE_FILE}"
        echo ""
    fi
done

# Print summary
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Slides built successfully!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "HTML files generated in: ${OUTPUT_DIR}/"
echo ""
echo "To present:"
echo "  open ${OUTPUT_DIR}/day1_kickoff.html"
echo ""
echo "In browser:"
echo "  • Press 'F' for fullscreen"
echo "  • Press '→' or Space to advance"
echo "  • Press '←' to go back"
echo "  • Press 'Esc' to exit fullscreen"
echo ""
