import subprocess
import shlex
from fastmcp import FastMCP

mcp = FastMCP(name="DebugCrash")


@mcp.tool
def debug_crash(target: str, args: list[str]) -> str:
    """Debug crashing program and return the stack trace."""

    debug_cmd = generate_debug_cmd(target, args)
    debug_output = subprocess.run(shlex.split(debug_cmd), capture_output=True)
    backtrace_text = parse_backtrace(debug_output)
    return backtrace_text


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
