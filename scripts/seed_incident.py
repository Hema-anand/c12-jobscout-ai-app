#!/usr/bin/env python3
"""Prints the supported seeded-incident modes for instructor use."""

MODES = {
    "slow": "Delays agent steps. Set FAULT_DELAY_MS to control the delay.",
    "llm_error": "Fails the LLM step.",
    "db_error": "Fails before persistence.",
    "queue_error": "Fails while publishing messaging events.",
}


def main():
    print("Available incident modes:")
    for name, description in MODES.items():
        print(f"- {name}: {description}")
    print()
    print("Example:")
    print("  set FAULT_MODE=slow")
    print("  set FAULT_DELAY_MS=1500")


if __name__ == "__main__":
    main()
