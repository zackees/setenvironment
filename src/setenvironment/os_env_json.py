import json
import os
import sys

from setenvironment.util import parse_paths


def main() -> None:
    """Main entry point for the script."""
    os_env = os.environ.copy()
    paths = os_env.pop("PATH", "")
    out: dict[str, dict | list[str]] = {}
    out["PATH"] = parse_paths(paths)
    env = {}
    for key, value in sorted(os_env.items()):
        env[key] = value
    out["ENVIRONMENT"] = env
    json.dump(out, sys.stdout, indent=4)
    return


if __name__ == "__main__":
    main()
