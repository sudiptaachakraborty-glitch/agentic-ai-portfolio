# SPDX-License-Identifier: MIT
# Part of: agentic-ai-portfolio  (https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio)
# Adapted from Ed Donner's "AI Engineer Agentic Track" course companion repo
# (https://github.com/ed-donner/agents, MIT, Copyright (c) 2025 Ed Donner).
# Modifications Copyright (c) 2026 Sudipta Chakraborty.

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
