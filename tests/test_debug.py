import pytest
import subprocess
from debug import generate_debug_cmd
from debug import parse_backtrace


@pytest.mark.parametrize(
    "target,args,expected",
    [
        (
            "myprog.exe",
            ["arg1", '"ar g2"'],
            "gdb -q --batch -ex b _exit -ex run -ex bt -ex quit --args myprog.exe arg1 '\"ar g2\"'",
        ),
        (
            "myprog.exe",
            ["-b", "True"],
            "gdb -q --batch -ex b _exit -ex run -ex bt -ex quit --args myprog.exe -b True",
        ),
        (
            "./path/to/binary.exe",
            [],
            "gdb -q --batch -ex b _exit -ex run -ex bt -ex quit --args ./path/to/binary.exe",
        ),
    ],
)
def test_generate_debug_cmd(target, args, expected):
    result = generate_debug_cmd(target, args)
    print(result)
    print(expected)
    assert expected == result


def test_parse_backtrace_extracts_backtrace():
    gdb_output = (
        b"Loaded /software/valgrind/libexec/valgrind/valgrind-monitor.py\n"
        b'Type "help valgrind" for more info.\n'
        b"loading eigen prettyprinters...\n"
        b"loading stdc++ prettyprinters...\n"
        b"No default breakpoint address now.\n"
        b"[Thread debugging using libthread_db enabled]\n"
        b'Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".\n'
        b"Generated number: 77\n"
        b"Number is greater than 75. Crashing the program...\n"
        b"\n"
        b"Program received signal SIGSEGV, Segmentation fault.\n"
        b"0x000055555555522c in decoyFunction3 () at occasional.cpp:12\n"
        b"12\t  *ptr = 42; // Dereferencing a null pointer to cause a crash\n"
        b"#0  0x000055555555522c in decoyFunction3 () at occasional.cpp:12\n"
        b"#1  0x0000555555555242 in decoyFunction2 () at occasional.cpp:18\n"
        b"#2  0x0000555555555252 in decoyFunction () at occasional.cpp:23\n"
        b"#3  0x00005555555552dd in main () at occasional.cpp:35\n"
        b"A debugging session is active.\n"
        b"\n"
        b"\tInferior 1 [process 310636] will be killed.\n"
        b"\n"
        b"Quit anyway? (y or n) [answered Y; input not from terminal]"
    )
    expected = (
        "#0  0x000055555555522c in decoyFunction3 () at occasional.cpp:12\n"
        "#1  0x0000555555555242 in decoyFunction2 () at occasional.cpp:18\n"
        "#2  0x0000555555555252 in decoyFunction () at occasional.cpp:23\n"
        "#3  0x00005555555552dd in main () at occasional.cpp:35"
    )
    result = parse_backtrace(
        subprocess.CompletedProcess(args=[], returncode=0, stdout=gdb_output)
    )
    assert result == expected
