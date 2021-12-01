run: build/s3

clean:
	rm -rf build

build/%: build/%.tmp
	mv build/out $@

.PHONY: run clean
.SECONDARY:;
.DELETE_ON_ERROR:;

build/s3.tmp: build/s2
	$< < shr.shr
	readelf -a build/out

build/s2.tmp: build/s1
	$< < shr.shr
	readelf -a build/out

# Bootstrapping
build/s1.asm: transpile_shr_to_asm.py shr.shr  Makefile
	@mkdir -p $(@D)
	python $< < shr.shr > $@

build/s1.o: build/s1.asm
	nasm -f elf64 -F dwarf $< -o $@

build/s1: build/s1.o
	ld -o $@ $< -e _start -T bootstrap.ld -g
