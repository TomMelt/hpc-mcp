import subprocess
import shlex
from fastmcp import FastMCP

mcp = FastMCP(name="Profile")


@mcp.tool
def profile(target: str, args: list[str]) -> str:
    """
    Profile the target binary and return the profile data.

    The profile data is cleaned by removing the header and footer of the profile data.
    Each line is a number followed by a call stack where each function name is separated by a semicolon.
    The number indicates the number of times the call stack was called.

    Sample output:
    70 main(); compute(); matrix_multiply()
    10 main(); read_data(); read_file()
    5 main(); compute(); matrix_multiply(); prepare()

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
    return clean_profile_data(profile_output.stdout.decode("utf-8"))


def generate_profile_cmd(target: str, args: list[str]) -> str:
    """Create the profile command."""
    return shlex.join(["sudo", "./perf_profiler", target] + args)


def clean_profile_data(profile_data: str) -> str:
    """Clean the profile data."""

    return profile_data.strip()
