import pytest
from profiler import generate_profile_cmd

@pytest.mark.parametrize(
    "target,args,expected",
    [
        ("myprog.exe", ["arg1", "arg2"], "sudo ./perf_profiler myprog.exe arg1 arg2"),
    ],
)
def test_generate_profile_cmd(target, args, expected):
    result = generate_profile_cmd(target, args)
    assert result == expected