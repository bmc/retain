#!/usr/bin/env bash
#
# Create files in "tmp", for testing.

mkdir -p ./tmp
cd tmp
touch a b c .gitignore .hello
mkdir foo
for i in d e f g
do
  touch foo/$i
done

mkdir foo/bar
for i in h i j k
do
  touch foo/bar/$i
done
