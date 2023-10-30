#include "tglang.h"

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  if (argc != 2) {
    fprintf(stderr, "Usage: tglang-tester <input_file>\n");
    return 1;
  }

  FILE *in = fopen(argv[1], "rb");
  if (in == NULL) {
    fprintf(stderr, "Failed to open input file %s\n", argv[1]);
    return 1;
  }

  fseek(in, 0, SEEK_END);
  long fsize = ftell(in);
  fseek(in, 0, SEEK_SET);

  char *text = malloc(fsize + 1);
  fread(text, fsize, 1, in);
  if (ferror(in)) {
    fprintf(stderr, "Failed to read input file %s\n", argv[1]);
    return 1;
  }
  fclose(in);

  text[fsize] = 0;

  printf("%d\n", tglang_detect_programming_language(text));
  return 0;
}
