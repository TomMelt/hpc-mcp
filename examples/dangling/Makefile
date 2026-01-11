CXX:=g++
FLAGS=-g -O0 -Wall -fno-omit-frame-pointer
.PHONY: all

all: dangling.exe

dangling.exe: dangling.cpp
	$(CXX) $(FLAGS) $^ -o $@

clean:
	rm -f *.exe
