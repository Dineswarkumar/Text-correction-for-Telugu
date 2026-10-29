# Literature Survey: Automatic Text Correction for Low-Resource Languages

## 1. Introduction
Automatic text correction is a foundational Natural Language Processing (NLP) task that includes spell checking, grammatical error correction (GEC), and morphological fixing. While high-resource languages like English have robust, context-aware grammar and spell checkers (e.g., Grammarly), these tools are severely lacking for low-resource languages. Indian languages, specifically Dravidian languages like Telugu, represent a massive user base but remain "low-resource" in the context of advanced NLP tools. Developing automated text correction for Telugu is crucial for improving digital literacy, educational tools, search engine accuracy, and content creation for millions of native speakers.

## 2. Background and Challenges
Telugu is a Dravidian language with over 80 million speakers. It presents unique challenges for automated text correction:
*   **Agglutinative Morphology:** Telugu words are formed by adding multiple suffixes to a root word. This leads to a theoretically infinite vocabulary, making dictionary-based spell checkers ineffective.
*   **Sandhi and Samasa:** Complex word-formation rules (morphophonemic changes at word boundaries) mean that merging words changes their spelling and pronunciation.
*   **Script Complexity:** The Telugu script is an abugida where consonants, vowels, and diacritics (matras) combine into complex ligatures. Errors often occur at the sub-character level (e.g., confusing similar-looking matras).
*   **Lack of Gold-Standard Data:** There is a severe scarcity of human-annotated parallel datasets mapping incorrect Telugu text to correct text.

## 3. Related Work

### 3.1. Rule-Based and Dictionary Approaches
Early approaches to Indic language text correction heavily relied on morphological analyzers and finite-state transducers.
*   **Recent Hybrid Systems (2025):** Recent papers (e.g., published in the International Journal of Computer Application, 2025) present hybrid systems combining Conditional Random Fields (CRF) for POS tagging with handcrafted rule-based validation. These systems address syntactic nuances like subject-verb agreement and postposition correctness by relying on explicit linguistic rules. While precise, they struggle to scale to unrestricted text.
*   **Sentence Analysis (2024):** Work in 2024 has explored grammar checking for complex and compound sentences by identifying clause structures, heavily relying on POS tagging to analyze inflectional features.

### 3.2. Statistical and Deep Learning Approaches
*   **Automatic Spelling Correction for Resource-Scarce Languages** 
    *   *Authors:* Pravallika Etoori, Manoj Chinnakotla, Radhika Mamidi (IIIT Hyderabad)
    *   *Venue:* COLING 2018
    *   *Problem:* Lack of parallel noisy-correct corpora for Indic languages.
    *   *Methodology:* Proposed an end-to-end character-level sequence-to-sequence (Seq2Seq) deep learning model. They generated synthetic datasets for Hindi and Telugu by injecting character-level spelling mistakes into clean text.
    *   *Results:* The model achieved competitive performance compared to traditional spell-checking techniques, proving that synthetic data and deep learning can bridge the resource gap.
    *   *Relevance:* This serves as the **direct baseline** for our project, specifically regarding the synthetic generation of sub-word/character-level errors in Telugu.

### 3.3. Neural and Transformer Approaches
*   **IndicBERT: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages**
    *   *Authors:* Divyanshu Kakwani et al. (AI4Bharat)
    *   *Venue:* Findings of EMNLP 2020
    *   *Contribution:* Introduced IndicCorp (8.8 billion tokens) and IndicBERT (an ALBERT-based model). Demonstrated that compact models specifically trained on Indic languages outperform massive general models like mBERT.
*   **IndicBERT v2: Towards High-Quality and Efficient Language Models for Indic Languages**
    *   *Authors:* Sumanth Doddapaneni et al. (AI4Bharat)
    *   *Venue:* ACL 2023
    *   *Contribution:* Upgraded to IndicCorp v2 (20.9 billion tokens). IndicBERT v2 significantly improved tokenization and contextual representations for 24 Indic languages, making it a powerful backbone for contextual error detection.
*   **MuRIL: Multilingual Representations for Indian Languages**
    *   *Authors:* Simran Khanuja et al. (Google Research India)
    *   *Venue:* ACL 2021 (Findings)
    *   *Contribution:* A BERT-based model explicitly trained on native script and transliterated Indic text. It is highly robust to the code-mixing and transliteration variability common in digital Telugu text.

### 3.4. Dataset Creation and Transliteration
*   **Samanantar: The Largest Publicly Available Parallel Corpora Collection for 11 Indic Languages**
    *   *Authors:* Gowtham Ramesh et al. (AI4Bharat)
    *   *Venue:* TACL 2022
    *   *Contribution:* Provides 4.82M English-Telugu parallel sentences, serving as a massive resource for pre-training and synthetic error generation.
*   **Aksharantar: Open Transliteration Datasets and Models for 21 Indic Languages**
    *   *Authors:* Yash Madhani et al. (AI4Bharat)
    *   *Venue:* ACL 2023
    *   *Contribution:* Developed IndicXlit and the largest transliteration dataset (26M pairs). Vital for correcting transliteration-induced spelling errors in Telugu.
*   **Processing South Asian Languages Written in the Latin Script: the Dakshina Dataset**
    *   *Authors:* Brian Roark et al. (Google Research)
    *   *Venue:* LREC 2020
    *   *Contribution:* Provided a gold-standard benchmark for Romanized Indic text, useful for evaluating transliteration and spelling standardizations.

## 4. Research Gaps
Despite the advent of models like IndicBERT and MuRIL, several gaps remain:
1.  **Lack of Human-Annotated GEC Datasets:** There is no publicly available, large-scale, human-annotated Grammatical Error Correction dataset for Telugu. Most research relies on synthetic perturbations.
2.  **Context-Aware Spell Checking:** Most Telugu spell checkers are still non-contextual. They cannot fix real-word errors (e.g., using a valid Telugu word in the wrong context).
3.  **Handling Agglutination:** Neural models still struggle with generating the correct, heavily inflected suffixes dynamically without hallucinating invalid Telugu characters.

## 5. How Our Work Addresses These Gaps
Our project builds upon the foundational Seq2Seq approach of Etoori et al. (2018) but upgrades the architecture using modern Transformer representations (like IndicBERT/MuRIL). By developing a comprehensive taxonomy of Telugu errors and building a structured, context-aware error correction model, we aim to bridge the gap between traditional synthetic spell-checkers and true grammatical error correction for heavily agglutinative low-resource languages.

## 6. References
1. Etoori, P., Chinnakotla, M., & Mamidi, R. (2018). *Automatic Spelling Correction for Resource-Scarce Languages using Deep Learning*. COLING. [URL](https://aclanthology.org/C18-1176/)
2. Kakwani, D., et al. (2020). *IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages*. EMNLP Findings. [URL](https://aclanthology.org/2020.findings-emnlp.445/)
3. Khanuja, S., et al. (2021). *MuRIL: Multilingual Representations for Indian Languages*. ACL Findings. [URL](https://arxiv.org/abs/2103.10730)
4. Doddapaneni, S., et al. (2023). *IndicBERT v2: Towards High-Quality and Efficient Language Models for Indic Languages*. ACL. [URL](https://arxiv.org/abs/2303.04881)
5. Ramesh, G., et al. (2022). *Samanantar: The Largest Publicly Available Parallel Corpora Collection for 11 Indic Languages*. TACL. [URL](https://aclanthology.org/2022.tacl-1.9/)
6. Madhani, Y., et al. (2023). *Aksharantar: Open Transliteration Datasets and Models for 21 Indic Languages*. ACL. [URL](https://aclanthology.org/2023.acl-long.474/)
7. Roark, B., et al. (2020). *Processing South Asian Languages Written in the Latin Script: the Dakshina Dataset*. LREC. [URL](https://aclanthology.org/2020.lrec-1.309/)
