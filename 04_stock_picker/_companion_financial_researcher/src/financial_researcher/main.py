# SPDX-License-Identifier: MIT
# Part of: agentic-ai-portfolio  (https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio)
# Adapted from Ed Donner's "AI Engineer Agentic Track" course companion repo
# (https://github.com/ed-donner/agents, MIT, Copyright (c) 2025 Ed Donner).
# Modifications Copyright (c) 2026 Sudipta Chakraborty.

#!/usr/bin/env python
# src/financial_researcher/main.py
import os
from financial_researcher.crew import ResearchCrew

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run():
    """
    Run the research crew.
    """
    inputs = {
        'company': 'Apple'
    }

    # Create and run the crew
    result = ResearchCrew().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")

if __name__ == "__main__":
    run()