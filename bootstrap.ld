ENTRY(_start)

PHDRS {
  none   PT_NULL FLAGS(0);
  text   PT_LOAD FLAGS((1 << 2) | (1 << 1) | (1 << 0));
}

SECTIONS {
    . = 0x410000;

    .text . : {
        *(.memes*)
    }:text
}
