import subprocess
import shlex
import re
from fastmcp import FastMCP

mcp = FastMCP(name="DebugCrash")


@mcp.tool
def debug_crash(target: str, args: list[str]) -> str:
    """Debug crashing program and return the stack trace."""

    debug_cmd = generate_debug_cmd(target, args)
    debug_output = subprocess.run(shlex.split(debug_cmd), capture_output=True)
    backtrace_text = parse_backtrace(debug_output)
    return backtrace_text


@mcp.tool
def debug_memory_problems(target: str, args: list[str]) -> str:
    """Debug memory problems in the program.

    Runs valgrind memcheck and returns the output for analysis.
    """
    valgrind_command = "valgrind"

    # Check if valgrind is available
    if not subprocess.run([valgrind_command, "--version"]):
        raise RuntimeError(
            f"'{valgrind_command}' is not available on the PATH. "
            "Perhaps valgrind is not installed"
        )

    command_list = [valgrind_command, target] + args
    valgrid_output = subprocess.run(command_list, capture_output=True)
    return select_valgrind_lines(valgrid_output.stderr.decode("utf-8"))


def select_valgrind_lines(lines: str) -> str:
    """Select all lines that are Valgrind output.

    Valgrind adds a prefix `==<pid>==` to its lines. We use it to filter.
    At the moment we ignore the pid and just match digits.
    TODO: Fix the above
    """

    regex = re.compile("^==[0-9]+==")
    matching_lines = list(
        filter(lambda single_line: regex.match(single_line), lines.splitlines())
    )
    return "\n".join(matching_lines)


def generate_debug_cmd(target: str, args: list[str]) -> str:
    """Generate a debug command for the target program with args."""
    crash_script = shlex.split("--batch -ex b _exit -ex run -ex bt -ex quit")
    general_gdb_config = "-q"
    debug_cmd = shlex.join(
        ["gdb", general_gdb_config] + crash_script + ["--args", target] + args
    )
    return debug_cmd


def parse_backtrace(debug_output: subprocess.CompletedProcess[bytes]) -> str:
    """Parse the backtrace from the output of gdb."""
    raw_text = debug_output.stdout.decode("utf-8")
    backtrace = "\n".join(
        line for line in raw_text.splitlines() if line.startswith("#")
    )
    return backtrace


if __name__ == "__main__":
    mcp.run(transport="stdio")
    # debug_crash("occasional-cpp.exe", [])
