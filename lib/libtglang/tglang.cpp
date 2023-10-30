#include "tglang.h"
#include "tglang_detector.hpp"

TglangDetector global_detector;

enum TglangLanguage tglang_detect_programming_language(const char *text)
{
    return global_detector.detect_programming_language(text);
}
