# Presentation & Document Defense Master Guide
**Project:** Automatic Text Correction for Low-Resource Languages (Telugu)  
**Institution:** Indian Institute of Information Technology, Nagpur (IIITN) — Dept. of CSE  
**Team:** Leela Venkata Sai Nerella (BT24CSA008), Parthasaradhi Guda (BT24CSA061), Dineswara Kumar Mangali (BT24CSA062)  
**Supervisors:** Ms. Dipti Pawade, Ms. Jaya Pathak  

---

## 📁 Generated Deliverables

| Deliverable | File Path | Format & Tool | Purpose |
| :--- | :--- | :--- | :--- |
| **Comprehensive Technical Report** | [`Telugu_Text_Correction_Comprehensive_Report.docx`](file:///t:/B-Tech/SEMESTER/Sem%205/Mini%20proj/Telugu_Text_Correction_Comprehensive_Report.docx) | Microsoft Word (.docx) | Full formal academic report with institutional header, metadata, tables, formulas, citations, and in-depth linguistic sections. Ready for submission or printing. |
| **Presentation Deck** | [`Telugu_Text_Correction_Presentation.pptx`](file:///t:/B-Tech/SEMESTER/Sem%205/Mini%20proj/Telugu_Text_Correction_Presentation.pptx) | PowerPoint (.pptx) / Canva | 12-slide 16:9 widescreen presentation with clean typography, tables, and embedded speaker notes. |

---

## 🎨 How to Open & Present in Canva (3 Easy Steps)

Canva has a built-in PPTX import engine. You do **not** need to recreate slides manually:

1. **Open Canva**: Go to [canva.com](https://www.canva.com) and log into your account.
2. **Import PPTX**:
   - In the top-right corner, click **Create a design** $\rightarrow$ Click **Import file** (or simply drag and drop [`Telugu_Text_Correction_Presentation.pptx`](file:///t:/B-Tech/SEMESTER/Sem%205/Mini%20proj/Telugu_Text_Correction_Presentation.pptx) directly onto the Canva dashboard).
   - Canva will automatically convert all 12 slides into native, fully-editable Canva presentation elements (text boxes, tables, shapes, and colors).
3. **Customize / Present**:
   - You can change fonts, add college logos, or apply Canva presentation animation effects.
   - Click **Present** in Canva to deliver the slideshow.

*(Note: You can also present the same file directly using Microsoft PowerPoint or Google Slides).*

---

## 🗣️ Slide-by-Slide Oral Defense & Presentation Script

Use this exact technical phrasing during your meeting. Every sentence is grounded in computational linguistics and empirical data.

---

### Slide 1: Title & Project Overview
- **What to say:**  
  *"Good morning/afternoon, Respected Supervisors. Today, we are presenting our mid-term progress on our 5th-semester mini project titled **'Automatic Text Correction for Low-Resource Languages (Telugu)'**. Our team consists of Leela Venkata Sai, Parthasaradhi, and Dineswara Kumar under the guidance of Ms. Dipti Pawade and Ms. Jaya Pathak. Over the past phase, we formulated the linguistic problem, curated over 100,000 sentences and vocabulary words, implemented an end-to-end multi-tier pipeline in Python, and empirically benchmarked our initial baselines on 1,000 test sentences."*

---

### Slide 2: Problem Statement & Linguistic Motivation
- **Supervisors' Core Interest:** *Why is Telugu difficult? Why can't we just use normal spellcheckers?*
- **What to say:**  
  *"Telugu is spoken by over 85 million people worldwide, yet it remains low-resource in computational NLP. Standard proofing tools (like Grammarly or MS Word's English spellcheck) do not work for Telugu due to three fundamental linguistic challenges:*
  1. ***Agglutinative Morphology:*** *Telugu forms words by chaining suffixes (denoting case markers, tenses, and postpositions) onto a base root. A single root word can generate thousands of valid surface inflections. Therefore, static dictionary lookups suffer from an explosive Out-Of-Vocabulary (OOV) rate, falsely flagging valid words as errors.*
  2. ***Abugida Script & Sub-Character Ligatures:*** *Unlike the Latin alphabet where letters sit in a linear sequence, Telugu is an abugida script. Consonants combine with vowel diacritics (matras / గుణింతాలు) and subscript conjuncts (vattulu / వత్తులు). Most real-world typing errors occur at the sub-character level—such as short versus long vowel confusion (ి vs ీ, ు vs ూ) or phonetically similar consonant confusion (retroflex ణ vs dental న, or sibilants శ/ష/స).*
  3. ***Informal Transliteration ('Tenglish'):*** *A significant portion of digital communication is typed in Roman script (e.g., 'namaskaram ela unnaru'). There is heavy spelling inconsistency and no unified tool that can ingest both Romanized and native Telugu script."*

---

### Slide 3: Gaps in Existing Solutions
- **Supervisors' Core Interest:** *What is wrong with current solutions?*
- **What to say:**  
  *"We identified four critical gaps in existing technology:*
  - ***Gap 1: Failure of Dictionary-Based Tools (Aspell/Hunspell):*** *They rely on exact matching. Because Telugu concatenates suffixes dynamically, they reject valid inflections, causing massive false positives.*
  - ***Gap 2: Scarcity of Human-Annotated GEC Corpora:*** *Unlike English, which has large public benchmark datasets like CoNLL-2014 or BEA-2019, Telugu has zero public human-annotated Grammatical Error Correction datasets.*
  - ***Gap 3: Context-Blindness of Isolate Edit-Distance:*** *Standard edit distance checks words in isolation. It cannot detect 'real-word errors'—for example, if a typo accidentally produces another valid dictionary word that makes no sense in the sentence context.*
  - ***Gap 4: Disconnect in Transliteration Tools:*** *Existing tools like Google Indic Input only transliterate phonetically; they do not perform downstream grammatical or spelling error recovery if the user typed noisy Tenglish."*

---

### Slide 4: Literature Review
- **Supervisors' Core Interest:** *Which research papers did you read? Cite the authors and venues.*
- **What to say:**  
  *"To ground our engineering in established research, we studied 5 key papers:*
  1. ***Etoori, Chinnakotla, and Mamidi (COLING 2018, IIIT Hyderabad):*** *They pioneered character-level Seq2Seq models for Hindi and Telugu. They showed that injecting synthetic phonological noise (matra and consonant confusions) overcomes the lack of manual error corpora. This paper is our direct baseline.*
  2. ***Kakwani et al. (EMNLP 2020, AI4Bharat):*** *Introduced IndicCorp (8.8B tokens) and IndicBERT. They proved Indic-specific pre-training significantly outperforms general models like mBERT. We used IndicCorp to extract our Telugu training data and vocabulary.*
  3. ***Khanuja et al. (ACL 2021, Google Research India):*** *Developed MuRIL, pre-trained jointly on native Indic script and transliterated Roman script. This provides our foundation for contextual Masked Language Modeling.*
  4. ***Doddapaneni et al. (ACL 2023, AI4Bharat):*** *IndicBERT v2, which improved akshara-level tokenizers and script representations across 24 Indic languages.*
  5. ***Roark et al. (LREC 2020, Google Research):*** *The Dakshina dataset, which gave us 70,000 verified Roman-to-Telugu word pairs to build our transliteration engine."*

---

### Slide 5: System Architecture (How Are We Solving It)
- **Supervisors' Core Interest:** *Explain the exact step-by-step pipeline.*
- **What to say:**  
  *"We solve this through a **Cascaded Multi-Tier Architecture** consisting of four stages:*
  - ***Stage 1 (Preprocessing):*** *Unicode NFC normalization to ensure canonical diacritic ordering, zero-width space/non-joiner removal, and automatic script detection.*
  - ***Stage 2 (Transliteration):*** *If Roman script (Tenglish) is detected, it is immediately converted to native Telugu script using our 70K Dakshina lexicon and phonetic mapping.*
  - ***Stage 3 (Error Detection):*** *Words are tokenized into linguistic Aksharas. We screen against our 100K frequency dictionary to flag OOV words, while phonotactic rules inspect for illegal vowel diacritic stacking.*
  - ***Stage 4 (Cascaded Correction):*** *We use a multi-pass approach. First, deterministic linguistic rules resolve high-frequency matra and consonant confusions (zero hallucination). Second, frequency-weighted Levenshtein Edit Distance handles arbitrary single-keystroke typos.*
  - ***Why this design?*** *Pure deep learning models tend to hallucinate words on short sentences, while pure rule-based systems are too rigid. Cascading rules first and statistical search second gives both high precision and high coverage."*

---

### Slide 6: Implemented Modules
- **Supervisors' Core Interest:** *What code did you actually write? Show the folder structure.*
- **What to say:**  
  *"We built modular Python packages located under `src/`:*
  - *In `src/preprocessing/`: `normalizer.py` handles Unicode cleaning and NFC equivalence; `tokenizer.py` splits text into valid Telugu orthographic syllables (Aksharas); `transliteration.py` handles Tenglish.*
  - *In `src/error_detection/`: `dictionary_based.py` performs sub-millisecond OOV checks against our 100K vocabulary; `rule_based.py` verifies phonotactic validity; `neural_detector.py` provides the interface for MLM scoring.*
  - *In `src/correction/`: `rule_based_corrector.py` applies bidirectional phonetic rules (ి/ీ, ు/ూ, ణ/న, శ/ష/స); `edit_distance_corrector.py` executes bounded Levenshtein search ($k \le 2$); `transformer_corrector.py` provides the Seq2Seq fine-tuning harness.*
  - *In `src/pipeline.py`: The `TeluguTextCorrectionPipeline` class orchestrates all stages into a single callable object."*

---

### Slide 7: Datasets & Contents
- **Supervisors' Core Interest:** *Where is the data? How many sentences?*
- **What to say:**  
  *"All our data is stored locally in `data/processed/`:*
  1. ***IndicCorp Telugu Subset:*** *`indiccorp_telugu_100k.txt` (20.1 MB) contains 100,000 clean, deduplicated sentences filtered for lengths of 5–30 words.*
  2. ***Curated Telugu Vocabulary:*** *`telugu_vocab.json` (3.6 MB) contains 100,000 unique Telugu words with their empirical frequency distribution.*
  3. ***Google Dakshina Transliteration:*** *`dakshina_transliteration.json` (7.2 MB) contains 70,000+ Roman-to-Telugu word pairs.*
  4. ***Synthetic Benchmark Corpus:*** *`data/synthetic/test.json` contains 1,000 test sentences with 2,130 injected typos covering matra, consonant, and keyboard errors."*

---

### Slide 8: Current Models & Baseline Results
- **Supervisors' Core Interest:** *What are your numbers? Explain the metrics.*
- **What to say:**  
  *"We evaluated our baselines on 1,000 test sentences and measured Word Error Rate (WER), Character Error Rate (CER), Exact Match, and BLEU:*
  - *The **Uncorrected Baseline** had a WER of 18.38% and BLEU of 64.75.*
  - *Our **Rule-Based Corrector** reduced WER significantly down to **11.28%** and increased BLEU to **77.53**, achieving an ultra-fast throughput of **2,656 sentences per second**.*
  - *Our **Dictionary + Edit Distance** achieved a WER of 12.68% and Exact Match of 35.30%.*
  - *The **Hybrid System (Rules + Edit Distance)** achieved the highest **Exact Sentence Match at 37.50%** (more than double the uncorrected baseline of 18.60%).*
  - *These results demonstrate that combining deterministic phonetic rules with statistical edit distance provides a solid, verifiable baseline before introducing deep neural models."*

---

### Slide 9: Qualitative Error Correction Examples
- **What to say:**  
  *"We verified our pipeline across several qualitative test cases:*
  - ***Phonetic errors:*** *'తేలుగు భాశ చాల అందమైణది' was corrected to 'తెలుగు భాష చాలా అందమైనది' by fixing short/long matras and retroflex consonants.*
  - ***Academic typos:*** *'విద్యార్ధులు పరిక్షలు' was corrected to 'విద్యార్థులు పరీక్షలు'.*
  - ***Tenglish:*** *'namaskaram ela unnaru' was automatically transliterated to native Telugu.*
  - ***Zero False Positives:*** *When fed clean sentences like 'భారతదేశం ఒక గొప్ప ప్రజాస్వామ్య దేశం', our system verified all words in the dictionary and left the text completely untouched."*

---

### Slide 10: Future Approach (Phase 2 Roadmap)
- **Supervisors' Core Interest:** *What is your plan for the rest of the semester?*
- **What to say:**  
  *"For Phase 2, we will implement three major enhancements:*
  1. ***Seq2Seq Transformer Fine-Tuning:*** *We will fine-tune IndicBART and mT5-small on Google Colab GPU using 80,000 synthetic sentence pairs to handle complex multi-token reordering and full sentence rewriting.*
  2. ***Contextual MLM Scoring with MuRIL:*** *We will compute pseudo-log-likelihood scores to detect real-word semantic errors that dictionaries cannot catch.*
  3. ***Morphological Stemmer / Sandhi Splitter:*** *We will implement a lightweight morphological splitter to peel off common Telugu case suffixes (విభక్తులు), further reducing OOV false positives.*
  4. ***Streamlit Web Application:*** *We will deploy an interactive web UI with real-time error highlighting and suggestion dropdowns."*

---

### Slide 11 & 12: Final Solution & Conclusion
- **What to say:**  
  *"In conclusion, our final target solution is an explainable, production-ready Telugu text correction suite. It combines high throughput for common typing mistakes with deep neural accuracy for complex grammar. We have already prepared a live terminal demo and we welcome your questions."*

---

## 🧠 Technical Terminology Glossary (Know Every Term)

| Term | Exact Technical Definition | Why It Matters for Telugu |
| :--- | :--- | :--- |
| **Agglutinative Morphology** | A morphological system where words are constructed by stringing together morphemes (prefixes/suffixes) representing discrete grammatical categories (case, tense, gender, number). | Root words (e.g., 'చేయు') produce thousands of forms ('చేసాడు', 'చేసింది', 'చేయగలడు', 'చేయలేకపోతున్నాడు'), making static wordlists insufficient. |
| **Abugida Script** | A segmental writing system in which consonant-vowel sequences are written as a unit; each consonant unit has an inherent vowel that can be modified by vowel diacritics. | In Telugu, each letter is an orthographic syllable. Errors happen in the diacritics (matras) attached to the consonant base. |
| **Akshara (అక్షరం)** | The atomic orthographic syllable unit in Indic scripts, structured as $(C + V_h)^* + C + M$, where $C$ is consonant, $V_h$ is virama/halant, and $M$ is matra. | Standard character counts fail in Indic scripts; tokenization must operate at the akshara level. |
| **Matra (గుణింతం)** | A dependent vowel sign attached to a consonant base (e.g., ి for short /i/, ీ for long /iː/). | Typists frequently confuse short and long vowel matras due to fast typing or regional dialect variations. |
| **Conjunct (వత్తు / Ligature)** | A stacked consonant form created by placing a Virama (Halant, U+0C4D) between two consonants. | Missed or misplaced viramas create broken character sequences. |
| **Sandhi (సంధి)** | Morpho-phonemic change that occurs at word boundaries when two words fuse together into one token. | Causes words to concatenate without whitespace, requiring sandhi-splitting algorithms. |
| **OOV (Out-Of-Vocabulary)** | Tokens present in the input text that do not exist in the reference dictionary/lexicon. | High OOV rates lead to false-positive spelling error detections if morphological variants are unhandled. |
| **NFC Normalization** | Unicode Normalization Form C: Canonical Decomposition followed by Canonical Composition. | Ensures composite characters (e.g., consonant + vowel sign) share identical binary byte representation across different OS keyboards. |
| **WER (Word Error Rate)** | Ratio of word-level substitutions, deletions, and insertions to the total reference words: $\text{WER} = \frac{S + D + I}{N}$. | The primary benchmark metric for text correction systems. |
| **CER (Character Error Rate)** | Levenshtein edit distance at the character level normalized by total reference characters. | Sensitive to minor sub-character diacritic corrections. |
| **BLEU Score** | Bilingual Evaluation Understudy: measures n-gram overlap between predicted corrected sentences and ground-truth references. | Proves that sentence fluency and linguistic order are improved by correction. |
| **Seq2Seq Denoising** | Encoder-Decoder neural architecture trained to map a corrupted input sequence into a clean target sequence. | The core architecture of IndicBART / mT5 for contextual grammar and spelling restoration. |
| **Masked Language Model (MLM)** | A bidirectional Transformer trained to predict randomly masked tokens based on left and right context (e.g., MuRIL). | Used to score candidate replacement words and detect contextually abnormal real-word errors. |

---

## 🛡️ Anticipated Supervisor Questions & Answers

### Q1: "Why did you use synthetic errors instead of real human errors?"
> **Answer:**  
> *"Unlike English, which has large human-annotated datasets like CoNLL-2014 and BEA-2019, Telugu has **zero public human-annotated Grammatical Error Correction datasets**. Following the established methodology of Etoori et al. (COLING 2018, IIIT Hyderabad), we designed a synthetic corruption engine that injects realistic phonological errors—specifically swapping short/long vowel matras, confusing retroflex and dental consonants, and modeling keyboard adjacency. This allows us to train and benchmark models without waiting months for manual human labeling."*

### Q2: "Why didn't you just use Hunspell, Aspell, or Microsoft Word's Telugu spellchecker?"
> **Answer:**  
> *"Traditional spellcheckers rely on static dictionaries and exact string matching. Because Telugu is an agglutinative language, suffixes concatenate onto root words dynamically. A dictionary with even 200,000 words will still miss tens of thousands of legitimate inflected verbs and nouns, resulting in high false-positive error rates. Furthermore, dictionary checkers are completely blind to real-word contextual errors."*

### Q3: "What is your hardware setup and how will you train Transformer models?"
> **Answer:**  
> *"Our local machines are used for data preprocessing, dictionary lookup, rule-based inference, and Streamlit UI development. Because training Transformer models like IndicBART or MuRIL requires 8GB+ of GPU VRAM, we conduct all neural model fine-tuning on **Google Colab Free / Kaggle Notebooks** utilizing Nvidia T4 / P100 GPUs with 15–16 GB VRAM."*

### Q4: "How does your pipeline handle informal Romanized text ('Tenglish')?"
> **Answer:**  
> *"Our preprocessor contains a Unicode script detector. If the input characters fall outside the Telugu range (U+0C00–U+0C7F) and inside ASCII/Latin, it routes the text to our Transliteration Engine. This engine matches words against Google's Dakshina 70,000-word lexicon and converts them to canonical native Telugu script before passing them to the error detection and correction stages."*

---

## 💻 Live Code Demo Execution Instructions

During the meeting, run this exact command in your terminal to demonstrate the working pipeline:

```powershell
cd "t:\B-Tech\SEMESTER\Sem 5\Mini proj\telugu-text-correction"
python scripts\demo_for_supervisors.py
```

This will run 4 preset tests (Tenglish, Matra errors, Academic typos, and Clean text) and then prompt you for interactive typing where your supervisors can enter any custom phrase.
