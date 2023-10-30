from transformers import MobileBertConfig, MobileBertForSequenceClassification

from utils import vocab, lang_enum


def get_model(size="t"):
    id2label = {idx: label for idx, label in enumerate(lang_enum.languages)}
    label2id = {label: idx for idx, label in enumerate(lang_enum.languages)}

    if size == "t":
        configuration = MobileBertConfig(
            architectures=["MobileBertForSequenceClassification"],
            embedding_size=96,
            hidden_size=164,
            intermediate_size=164,
            intra_bottleneck_size=96,
            max_position_embeddings=512,
            num_attention_heads=4,
            num_feedforward_networks=2,
            num_hidden_layers=2,
            attention_probs_dropout_prob=0.1,
            classifier_activation=True,
            classifier_dropout=None,
            hidden_act="relu",
            hidden_dropout_prob=0.0,
            id2label=id2label,
            initializer_range=0.02,
            key_query_shared_bottleneck=True,
            label2id=label2id,
            layer_norm_eps=1e-12,
            model_type="mobilebert",
            normalization_type="no_norm",
            pad_token_id=0,
            problem_type="single_label_classification",
            trigram_input=True,
            type_vocab_size=2,
            use_bottleneck=True,
            use_bottleneck_attention=False,
            vocab_size=len(vocab.vocab_list),
        )
    else:
        raise NotImplementedError

    return MobileBertForSequenceClassification(config=configuration)
