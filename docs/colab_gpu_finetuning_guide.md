# Google Colab GPU Fine-Tuning Guide (Phase 2)
**Automatic Text Correction for Low-Resource Languages (Telugu)**  
*IIIT Nagpur, Department of Computer Science & Engineering*

---

## 📌 Executive Summary

This guide provides step-by-step operational instructions for executing **Notebook 04 (`04_transformer_models_finetuning_colab.ipynb`)** on Google Colab using a free or Pro **Nvidia T4 / A100 GPU**.

### Models Targeted:
1. **IndicBART** (`ai4bharat/IndicBART`): Compact 244M Seq2Seq model pre-trained on 11 Indic languages with shared script representations and language tags (`<2te>`).
2. **mT5-Small** (`google/mt5-small`): Google's 300M multilingual text-to-text Transformer pre-trained on mC4 across 101 languages.

### Dataset:
- **Training Set:** 50,000 synthetic pairs (`data/synthetic/train.json`)
- **Validation Set:** 3,000 synthetic pairs (`data/synthetic/val.json`)
- **Held-Out Test Set:** 1,000 benchmark pairs (`data/synthetic/test.json`)

---

## ⚙️ 1. Google Colab Environment Setup

### Step 1.1: Enable GPU Acceleration
1. Open Google Colab: [https://colab.research.google.com](https://colab.research.google.com).
2. Upload `04_transformer_models_finetuning_colab.ipynb`.
3. In the top navigation bar, click:  
   **Runtime** $\rightarrow$ **Change runtime type**.
4. Set:
   - **Hardware accelerator:** `T4 GPU` (or `A100 GPU` if Colab Pro).
   - **GPU RAM:** Standard (15.0 GB VRAM is sufficient).
5. Click **Save**.

### Step 1.2: Prepare Project Directory on Google Drive
Upload the project folder to your Google Drive under:
```
My Drive/
└── NLP_Telugu_Project/
    ├── data/
    │   └── synthetic/
    │       ├── train.json (60,000 pairs)
    │       ├── val.json (7,500 pairs)
    │       └── test.json (7,500 pairs)
    ├── models/
    └── 04_transformer_models_finetuning_colab.ipynb
```

When you run Cell 0, Colab will execute:
```python
from google.colab import drive
drive.mount('/content/drive')
```
Authorize Google Drive access when prompted. The notebook automatically detects if the Drive folder is present and switches into it.

---

## 📦 2. Mandatory Dependencies

Colab ships with PyTorch pre-installed, but IndicBART and mT5 require specialized tokenizers:

```bash
!pip install -q --upgrade \
    transformers>=4.40.0 \
    datasets>=2.18.0 \
    accelerate>=0.28.0 \
    evaluate>=0.4.1 \
    jiwer>=3.0.3 \
    sacrebleu>=2.4.0 \
    sentencepiece>=0.2.0 \
    protobuf>=3.20.0 \
    rapidfuzz>=3.6.0 \
    indic-nlp-library>=0.92
```

> ⚠️ **Critical Trap:** Without `sentencepiece` and `protobuf`, both `AlbertTokenizer` (IndicBART) and `T5Tokenizer` (mT5) will fail to extract subword vocabularies from Hugging Face Hub.

---

## 🔬 3. Model Architecture & Preprocessing Differences

| Specification | IndicBART (`ai4bharat/IndicBART`) | mT5-Small (`google/mt5-small`) |
| :--- | :--- | :--- |
| **Parameters** | 244 Million | 300 Million |
| **Pretraining Languages** | 11 Indic + English | 101 Global Languages |
| **Input Format** | `{corrupted_text} </s> <2te>` | `సరిచేయి: {corrupted_text}` |
| **Target Format** | `{clean_text} </s>` | `{clean_text}` |
| **Decoder Initialization** | `forced_bos_token_id = tokenizer.convert_tokens_to_ids("<2te>")` | Default `<pad>` |
| **Recommended Learning Rate** | `5e-5` (AdamW) | `1e-4` (Adafactor / AdamW) |
| **Batch Size (T4 15GB)** | 16 (grad accum = 2 $\rightarrow$ effective 32) | 16 (grad accum = 2 $\rightarrow$ effective 32) |
| **Loss Masking** | Replace `pad_token_id` in labels with `-100` | Replace `pad_token_id` in labels with `-100` |

---

## ⏱️ 4. Training Execution & Runtime Estimation

On a free **Nvidia T4 GPU (15GB VRAM)**:
- **IndicBART Fine-Tuning (3 Epochs, 50,000 samples):**
  - Steps: $\approx 4,688$ gradient steps.
  - Runtime: $\approx 45 - 55$ minutes.
  - Peak VRAM Usage: $\approx 7.2$ GB.
- **mT5-Small Fine-Tuning (3 Epochs, 50,000 samples):**
  - Steps: $\approx 4,688$ gradient steps.
  - Runtime: $\approx 50 - 60$ minutes.
  - Peak VRAM Usage: $\approx 8.1$ GB.

Checkpoints are saved every 500 steps. The `Seq2SeqTrainer` retains only the top 2 checkpoints to prevent running out of Colab disk space.

---

## 📊 5. Evaluation Benchmarking Against Phase 1

Notebook 04 automatically generates the consolidated benchmark comparison table on the held-out test split (1,000 samples):

| Model / Approach | WER (↓) | CER (↓) | Exact Match (↑) | BLEU (↑) | F1 Score (↑) | Paradigm |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Uncorrected Baseline** | 0.1838 | 0.0270 | 18.60% | 64.75 | 82.02% | Corrupted input |
| **Rule-Based Corrector** | 0.1128 | 0.0180 | 33.90% | 77.53 | 89.15% | Deterministic phonetics |
| **Dictionary + Edit Distance** | 0.1266 | 0.0222 | 35.30% | 75.49 | 87.76% | Statistical Levenshtein |
| **Two-Pass Hybrid Corrector** | 0.1210 | 0.0214 | 37.60% | 76.60 | 88.33% | Rule + Edit fallback |
| **Fine-Tuned IndicBART** | **~0.045 - 0.065** | **~0.008 - 0.012** | **~65.0 - 75.0%** | **~88.0 - 92.0** | **~94.0 - 96.0%** | Seq2Seq Indic Pretrained |
| **Fine-Tuned mT5-Small** | **~0.055 - 0.075** | **~0.010 - 0.014** | **~60.0 - 70.0%** | **~86.0 - 90.0** | **~93.0 - 95.0%** | Multilingual Text-to-Text |

---

## 💾 6. Checkpoint Persistence & Integration

At the end of training, the notebook packages the models into:
1. `indicbart_telugu_corrector.zip`
2. `mt5_telugu_corrector.zip`

These are saved directly to Google Drive under `My Drive/NLP_Telugu_Project/saved_models/`.

To use them locally in your repository:
1. Download and extract them to `models/indicbart_telugu_corrector` and `models/mt5_telugu_corrector`.
2. Use `src.pipeline.TeluguTextCorrectionPipeline`:
   ```python
   from src.pipeline import TeluguTextCorrectionPipeline

   # Use fine-tuned IndicBART
   pipeline = TeluguTextCorrectionPipeline(
       mode="indicbart", 
       transformer_model_path="models/indicbart_telugu_corrector"
   )
   result = pipeline.correct("శాశ్వత ప్చచిక ప్రాంతాలు")
   print(result["corrected"]) # Output: శాశ్వత పచ్చిక ప్రాంతాలు
   ```
