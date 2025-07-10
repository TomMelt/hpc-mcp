CXX:=g++
FLAGS=-g -O0 -Wall -fno-omit-frame-pointer
.PHONY: all

all: segfault.exe

segfault.exe: segfault.cpp
	$(CXX) $(FLAGS) $^ -o $@

clean:
	rm -f *.exe
