# Task
Identify programming and markup languages in code snippets https://contest.com/docs/ML-Competition-2023

# Structure
```
├── lib
│   ├── data
│   │   ├── dataset - dataset for testing (1968 files)
│   │   ├── model
│   │   │   ├── model.hpp - model inbuilt to c++ header (was generated automatically)
│   │   │   ├── model_meta.hpp - configuration and vocabulary (was generated automatically)
│   │   ├── report
│   │   │   ├── test_results_analysis.txt - report after lib testing
│   ├── libtglang - library for language identification
│   ├── scripts - build, test and test analysis scripts
├── ml - code for training and data processing
│   ├── train.py - training loop
│   ├── data.ipynb - scripts to collect and process datasets
│   ├── playground.ipynb - some code to validate and convert model
```

# Algorithm

## Data preprocessing

1. Process source string:

    * resize to 4096 symbols
    * remove all symbols inside '' and ""
    * find minimal number of leading spaces and shift all text to the left
    * rtrim each line
    * remove empty lines

2. Encode text:
    * tokenise with vocabulary (~2.5x times reduce number of symbols)
    * merge all continious unknown tokens to one unknown (for example all single letters and numbers were marked as unknown)
    * while we have more than MAX_SIZE tokens in vector, we cut each line up to N tokens, where N is max(MAX_SIZE/len(line), MAX_LINE_SIZE)
    * if we still have more than MAX_SIZE tokens, we remove lines which starts with the same token as previous line (excluding spaces). Idea here is to remove comments or repeated contructions like variables declaration.
    * if it's still more than MAX_SIZE, we take first MAX_SIZE tokens

### Example:
Source
```c
#include <stdio.h>

int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d", a + b);
}
```
Decoded text after encoding
```
#include <std<UNK>.<UNK>>
int main() {
    int <UNK>, <UNK>;
    scan<UNK>("", &<UNK>, &<UNK>);
    printf("", <UNK> + <UNK>);
}
```


## Inference

I used pruned 2-layers MobileBERT (https://huggingface.co/docs/transformers/model_doc/mobilebert) with such config:

```yaml
embedding_size: 96
hidden_size: 164
intermediate_size: 164
num_attention_heads: 4
num_feedforward_networks: 2
num_hidden_layers: 2
max_tokens: 128
threshold: 0.2
```

# Testing

- For testing I selected 1968 files from source dataset (~20 per language). I didn't have enough time to manually check all of them, but roughly checked that all languages are presented.
- Environment:
    - AMD Ryzen Threadripper PRO 5965WX
    - Docker image 'debian:10'
    - Docker container with limited cpu (8 cores)
- Testing script measures full program time thourgh inbuilt command '_time_', including library initialization and file reading.
- From experiments the code without prediction takes 0.004s -> ~0.009s is a time for prediction for 128 tokens.

|MaxTokens=256|||
|----|----|---|
|__Accuracy__|0.979  | [1926/1968]|
|__Program avg time__|0.020s | [min:  0.003s, max:  0.026s]|
|__Func call avg time__|0.016s | (theoretically) |

|MaxTokens=128 (target)|||
|----|----|---|
|__Accuracy__|0.975  | [1918/1968]|
|__Program avg time__|0.013s | [min:  0.003s, max:  0.017s]|
|__Func call avg time__|0.009s | (theoretically) |

|MaxTokens=96|||
|----|----|---|
|__Accuracy__|0.971  | [1911/1968]|
|__Avg time__|0.011s | [min:  0.003s, max:  0.014s]|
|__Func call avg time__|0.007s | (theoretically) |

|MaxTokens=64|||
|----|----|---|
|__Accuracy__|0.957  | [1884/1968]|
|__Avg time__|0.010s | [min:  0.003s, max:  0.014s]|
|__Func call avg time__|0.006s | (theoretically) |

# Training

## Datasets

|Source|Files|
|---|---|
|GitHub|1862768|
|StackOverflow|129122|
|Rosetta|98106|
|DLLD|48463|
|Generated|16000|
|ShortSamples|100|

- Rosetta and DLLD as it is + manually reassigned names.
- For GitHub I implemented parser by language, generated list of extensions for each language (utils/lang_enum.py) through ChatGPT and parsed files by extension.
- For StackOverflow I used dump from https://archive.org/details/stackexchange and only used comments and posts as TGLANG_OTHER label. (Seems quite close to posts in TG)
- For rare languages (FIFT, TL and FUNC) I prepared set of ~100 short snippets for each language and used them to generate variative combinations.
- I didn't implement any sortings by popularity of the language in this solution. Therefore I added some short samples with high weight to overfit model predict this syntax as popular language (for C vs D, JSON vs Other, etc.)

## Vocabulary

- Using ChatGPT I generated set of special chars and keywords for each language (utils/lang_constructs.py) and merged them into one vocabulary.
- Additionally I used top 200 ngrams from all languages.
- Munually reviewed it and removed strange symbols and long ngrams.

## TrainConfig

|||
|----|----|
|__Model__|MobileBERT (https://huggingface.co/docs/transformers/model_doc/mobilebert)|
|__Loss__|CrossEntropyLoss with label smoothing (0.15) and with Exponential class frequency weighting|
|__Optimizer__|AdaBelief (WEIGHT_DECAY = 1e-1, BETAS = (0.9, 0.95))|
|__Scheduler__|CosineAnnealing (LR = 2e-3, MIN_LR = 2e-5)|
|__BatchSize__|epochs 1-60: 512, 61-200: 1024, 201-350: 1536, >351: 2048|
|__Augs__|Randomly select 5-100 lines from each file|
|__GradientClip__|2.0|
|__Precision__|MixedPrecision|
|__Epochs__|1100 (~1.2min per epoch for 2xNVIDIA 4090)|
|__MaxTokens__|512|

# Solution

- converted model from pytorch to tflite (torchlib doesn't support static linking)
- quantization to float16 (~1.5 times faster for some cpu)
- model inbuilt directly to library (no need to load weights) through `xxd -i model.tflite > model.h`

# Known issues

- Short snippets of code 1-4 lines could be classified wrong because of difficulty to prepare such dataset automatically. (didn't find some fast solutions to recognize comments and code for my dataset...)
- Some snippets of different languages with similar syntax could be randomly classified without taking into account popularity of the language. (e.g. a+b could be classified as D language)
