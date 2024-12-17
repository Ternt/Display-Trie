@echo off


if not exist build mkdir build

pushd build
call gcc ../src/main.c -o main.exe
popd
