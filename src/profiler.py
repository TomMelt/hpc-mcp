import subprocess
import shlex
from collections import defaultdict
from fastmcp import FastMCP

mcp = FastMCP(name="Profile")


@mcp.tool
def profile(target: str, args: list[str]) -> str:
    """
    Profile the target binary and return the profile data.

    The profile data is cleaned by removing the header and footer of the profile data.
    Each line is a number followed by a function name.
    The number indicates the number of times the function was called.

    Sample output:
    199 area(unsigned long) const
    27 add(unsigned long)
    40 start_thread

    This sample output indicates that the function area(unsigned long) const was called 199 times, the function add(unsigned long) was called 27 times, and the function start_thread was called 40 times.

    Args:
        target: The target binary name to profile.
        args: The arguments to pass to the target binary.

    Returns:
        Cleaned profile data
    """
    # run profiler with target binary and args
    profile_cmd = generate_profile_cmd(target, args)
    profile_output = subprocess.run(
        shlex.split(profile_cmd), capture_output=True, check=True
    )

    with open("profile.out", "r") as f:
        profile_data = f.read()

        return clean_profile_data(profile_data)


def generate_profile_cmd(target: str, args: list[str]) -> str:
    """Create the profile command."""
    return shlex.join(["sudo", "./perf_profiler", target] + args)


def clean_profile_data(profile_data: str) -> str:
    """Clean the profile data."""

    function_call_counts = defaultdict(int)

    for line in profile_data.splitlines():
        counts, functions = line.strip().split(" ", 1)[0], line.strip().split(" ", 1)[1]

        functions_present = functions.strip().split(";")

        for function in functions_present:
            function_call_counts[function] = function_call_counts[function] + int(
                counts
            )

    return "\n".join(
        [
            f"{count} {function}"
            for function, count in sorted(
                function_call_counts.items(), key=lambda x: x[1], reverse=True
            )
        ]
    )
