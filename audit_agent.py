from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from deepagents import create_deep_agent
from loguru import logger

ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"
DEFAULT_MODEL = "openrouter:inclusionai/ring-2.6-1t:free"

CONTRACTS_DIR = ROOT / "contracts"
SYSTEM_PROMPT = """
You are the Senior Financial Auditor for Shree Manufacturing Pvt. Ltd.
Business rules: report any discrepancy greater than INR 0, use 30 days net unless specified otherwise, and check contract clauses for late-delivery penalties.
Data conventions: currency is INR and dates use YYYY-MM-DD.
Protocol: BEFORE taking any action, use write_todos to outline a 3-step audit plan. Update the todo list as you progress. Use read_file to access vendor contracts. Only answer questions related to finance, auditing, or corporate compliance.
You have access to: write_todos (planning), read_file (contract access).
""".strip()


def _contract_filename(vendor_name: str) -> str:
    return vendor_name.replace(" ", "_") + "_Contract.txt"


def find_contract(vendor_name: str) -> Path:
    path = CONTRACTS_DIR / _contract_filename(vendor_name)
    if not path.exists():
        raise FileNotFoundError(f"No contract found for {vendor_name}: {path}")
    return path


def read_contract(vendor_name: str) -> str:
    return find_contract(vendor_name).read_text(encoding="utf-8")


def read_file(vendor_name: str) -> str:
    """Read a contract file for a vendor by name. Returns the full contract text."""
    try:
        return read_contract(vendor_name)
    except FileNotFoundError:
        return f"Contract not found for vendor: {vendor_name}. Available contracts are in {CONTRACTS_DIR}"


def write_todos(plan: str) -> str:
    """Write a todo list/plan for the audit. Called first before any other action."""
    logger.info(f"Audit Plan:\n{plan}")
    return f"Plan noted: {plan}"


def build_agent(model_name: str):
    return create_deep_agent(
        model=model_name,
        tools=[write_todos, read_file],
        system_prompt=SYSTEM_PROMPT,
    )


def run_self_check() -> str:
    return read_contract("Gujarat Steel Corp")


def load_model_name() -> str:
    load_dotenv(ENV_PATH)
    return os.getenv("OPENROUTER_MODEL") or os.getenv("MODEL_NAME") or DEFAULT_MODEL


def invoke_agent(prompt: str) -> str:
    agent = build_agent(load_model_name())
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    messages = result.get("messages", [])
    if not messages:
        return ""
    final = messages[-1]
    return str(getattr(final, "content", final))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="?", default="What is your job?")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)

    if args.self_check:
        print(run_self_check())
        return 0

    print(invoke_agent(args.prompt))
    return 0
