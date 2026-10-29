# -*- coding: utf-8 -*-
"""
Automatic Telugu Text Correction System
IIIT Nagpur - Department of Computer Science & Engineering
5th Semester Mini Project
"""

import sys
import time
import json
from pathlib import Path
from collections import Counter

import streamlit as st
import pandas as pd

# Project root setup
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline import TeluguTextCorrectionPipeline

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Telugu Text Correction",
    layout="wide"
)

# -----------------------------------------------------------------------------
# Cached Pipeline Loading
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading dictionary and models...")
def get_pipeline():
    return TeluguTextCorrectionPipeline(mode="hybrid")

pipeline = get_pipeline()

# -----------------------------------------------------------------------------
# Sidebar: Configuration & Details
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("Project Details")
    st.markdown("""
    **Project:** Automatic Telugu Text Correction  
    **Institution:** IIIT Nagpur (CSE Dept)  
    **Course:** 5th Sem Mini Project  
    
    **Team Members:**
    - Leela Venkata Sai Nerella (BT24CSA008)
    - Parthasaradhi Guda (BT24CSA061)
    - Dineswara Kumar Mangali (BT24CSA062)
    
    **Supervisors:**
    - Ms. Dipti Pawade
    - Ms. Jaya Pathak
    """)
    
    st.divider()
    st.subheader("Model Configuration")
    
    selected_mode = st.selectbox(
        "Correction Strategy",
        options=[
            "Hybrid (Rule-Based + Edit Distance)",
            "Rule-Based Corrector",
            "Dictionary + Edit Distance",
            "IndicBART / mT5 (Colab GPU Training)"
        ],
        index=0
    )
    
    mode_keys = {
        "Hybrid (Rule-Based + Edit Distance)": "hybrid",
        "Rule-Based Corrector": "rule_based",
        "Dictionary + Edit Distance": "edit_distance",
        "IndicBART / mT5 (Colab GPU Training)": "hybrid"
    }
    active_mode = mode_keys[selected_mode]
    
    auto_translit = st.checkbox("Auto-transliterate English to Telugu (Tenglish)", value=True)

# -----------------------------------------------------------------------------
# Main Header
# -----------------------------------------------------------------------------
st.title("Automatic Text Correction for Telugu")
st.caption("Department of Computer Science & Engineering, IIIT Nagpur")

tab_demo, tab_diagnostics, tab_benchmarks, tab_taxonomy, tab_batch = st.tabs([
    "Correction Demo",
    "Token Diagnostics",
    "Benchmark Results",
    "Error Taxonomy",
    "Batch Evaluation"
])

# -----------------------------------------------------------------------------
# TAB 1: Correction Demo
# -----------------------------------------------------------------------------
with tab_demo:
    st.subheader("Interactive Sentence Correction")
    
    st.markdown("**Sample Inputs:**")
    col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)
    
    samples = [
        ("Matra Error", "మేము దన్ని సాధిస్తాము మరియు ఆయన అదృష్టమెనని తెలిపారు"),
        ("Conjunct Swap", "శాశ్వత ప్చచిక ప్రాంతాలు మరియు వి్గలను తయారు చేసాము"),
        ("Consonant Voicing", "సెంట్రల్ మార్కెడ్ విలువ 9 డ్రిలియన్లకు చేరుకుంది"),
        ("Sandhi / Space", "ఇస్లామ్ మతానికిమారక ముందు మాల్దీవులలో బౌద్ధం విలసిల్లింది"),
        ("Tenglish Input", "meeru ela unnaru nenu telugu baasha nerchukuntunnanu")
    ]
    
    if "current_input" not in st.session_state:
        st.session_state["current_input"] = samples[0][1]
        
    if col_p1.button("Sample 1: Matra"):
        st.session_state["current_input"] = samples[0][1]
        st.rerun()
    if col_p2.button("Sample 2: Conjunct"):
        st.session_state["current_input"] = samples[1][1]
        st.rerun()
    if col_p3.button("Sample 3: Voicing"):
        st.session_state["current_input"] = samples[2][1]
        st.rerun()
    if col_p4.button("Sample 4: Sandhi"):
        st.session_state["current_input"] = samples[3][1]
        st.rerun()
    if col_p5.button("Sample 5: Tenglish"):
        st.session_state["current_input"] = samples[4][1]
        st.rerun()
        
    user_text = st.text_area(
        "Input Text (Telugu or Tenglish):",
        value=st.session_state["current_input"],
        height=100
    )
    
    col_btn1, col_btn2 = st.columns([1, 5])
    submit = col_btn1.button("Correct Text", type="primary")
    
    if user_text.strip():
        t0 = time.perf_counter()
        res = pipeline.correct(user_text, mode=active_mode)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        
        orig_norm = res["normalized"]
        corrected = res["corrected"]
        errors = res.get("errors_detected", [])
        
        st.divider()
        st.subheader("Results")
        
        col_out1, col_out2 = st.columns(2)
        with col_out1:
            st.markdown("**Original / Normalized Input:**")
            st.write(orig_norm)
            if res.get("was_transliterated"):
                st.caption(f"(Transliterated from Roman input: {res['transliterated']})")
                
        with col_out2:
            st.markdown(f"**Corrected Output ({selected_mode}):**")
            st.write(corrected)
            
        st.markdown("**Token Changes:**")
        orig_tokens = orig_norm.split()
        corr_tokens = corrected.split()
        
        diff_rows = []
        max_tokens = max(len(orig_tokens), len(corr_tokens))
        num_changed = 0
        
        for idx in range(max_tokens):
            w_orig = orig_tokens[idx] if idx < len(orig_tokens) else ""
            w_corr = corr_tokens[idx] if idx < len(corr_tokens) else ""
            status = "Unchanged" if w_orig == w_corr else "Corrected"
            if status == "Corrected":
                num_changed += 1
            diff_rows.append({
                "Position": idx + 1,
                "Original Word": w_orig,
                "Corrected Word": w_corr,
                "Status": status
            })
            
        st.dataframe(pd.DataFrame(diff_rows))
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Latency", f"{elapsed_ms:.1f} ms")
        m2.metric("Total Tokens", len(orig_tokens))
        m3.metric("Errors Detected", len(errors))
        m4.metric("Words Changed", num_changed)
        
        if selected_mode == "IndicBART / mT5 (Colab GPU Training)":
            st.info("Note: IndicBART / mT5 are currently training on Colab GPU in Notebook 04. Displaying output from the Phase 1 Hybrid baseline.")

# -----------------------------------------------------------------------------
# TAB 2: Token Diagnostics
# -----------------------------------------------------------------------------
with tab_diagnostics:
    st.subheader("Dictionary Lookup & Rule Diagnostics")
    st.caption("Checks each word against the 100,000-word Telugu lexicon and candidate generation modules.")
    
    diag_sentence = st.text_input("Sentence to analyze:", value=user_text if user_text else samples[0][1])
    
    if diag_sentence.strip():
        norm_s = pipeline.preprocessor.normalize(diag_sentence)
        tokens = norm_s.split()
        
        diag_rows = []
        for idx, t in enumerate(tokens):
            clean_t = pipeline.detector.clean_token(t)
            is_err = pipeline.detector.is_word_error(t)
            rule_cands = pipeline.rule_corrector.generate_rule_candidates(clean_t)
            ed_cands = pipeline.edit_corrector.get_candidates(clean_t, top_k=3)
            final_w = pipeline.edit_corrector.correct_word(
                pipeline.rule_corrector.correct_word(clean_t)
            )
            
            diag_rows.append({
                "Pos": idx + 1,
                "Token": t,
                "In Vocab": "No (Error)" if is_err else "Yes",
                "Rule Fix": rule_cands[0] if rule_cands else "-",
                "Edit-Distance Candidates": ", ".join(ed_cands) if ed_cands else "-",
                "Final Fix": final_w
            })
            
        st.dataframe(pd.DataFrame(diag_rows))

# -----------------------------------------------------------------------------
# TAB 3: Benchmark Results
# -----------------------------------------------------------------------------
with tab_benchmarks:
    st.subheader("Phase 1 Evaluation Benchmark Results")
    st.markdown("Evaluated on 1,000 synthetic test sentences from the IndicCorp Telugu corpus (Notebook 03).")
    
    bench_data = pd.DataFrame([
        {
            "Model / Approach": "Uncorrected Baseline",
            "WER (↓)": 0.1838,
            "CER (↓)": 0.0270,
            "Exact Match (↑)": "18.60%",
            "BLEU (↑)": 64.75,
            "F1 Score (↑)": "82.02%",
            "Speed (sent/s)": "N/A"
        },
        {
            "Model / Approach": "Rule-Based Corrector",
            "WER (↓)": 0.1128,
            "CER (↓)": 0.0180,
            "Exact Match (↑)": "33.90%",
            "BLEU (↑)": 77.53,
            "F1 Score (↑)": "89.15%",
            "Speed (sent/s)": "28,175"
        },
        {
            "Model / Approach": "Dictionary + Edit Distance",
            "WER (↓)": 0.1266,
            "CER (↓)": 0.0222,
            "Exact Match (↑)": "35.30%",
            "BLEU (↑)": 75.49,
            "F1 Score (↑)": "87.76%",
            "Speed (sent/s)": "66.0"
        },
        {
            "Model / Approach": "Two-Pass Hybrid (Current Best)",
            "WER (↓)": 0.1210,
            "CER (↓)": 0.0214,
            "Exact Match (↑)": "37.60%",
            "BLEU (↑)": 76.60,
            "F1 Score (↑)": "88.33%",
            "Speed (sent/s)": "103.2"
        },
        {
            "Model / Approach": "Fine-Tuned IndicBART (Target)",
            "WER (↓)": 0.0520,
            "CER (↓)": 0.0095,
            "Exact Match (↑)": "68.40%",
            "BLEU (↑)": 89.20,
            "F1 Score (↑)": "95.10%",
            "Speed (sent/s)": "~25 (GPU)"
        },
        {
            "Model / Approach": "Fine-Tuned mT5-Small (Target)",
            "WER (↓)": 0.0610,
            "CER (↓)": 0.0118,
            "Exact Match (↑)": "64.10%",
            "BLEU (↑)": 87.50,
            "F1 Score (↑)": "94.20%",
            "Speed (sent/s)": "~22 (GPU)"
        }
    ])
    
    st.dataframe(bench_data)
    
    st.markdown("**Metric Comparison Chart:**")
    chart_df = pd.DataFrame({
        "Model": ["Uncorrected", "Rule-Based", "Edit-Distance", "Hybrid", "IndicBART (Target)", "mT5 (Target)"],
        "WER": [0.1838, 0.1128, 0.1266, 0.1210, 0.0520, 0.0610],
        "BLEU": [64.75, 77.53, 75.49, 76.60, 89.20, 87.50]
    }).set_index("Model")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("*Word Error Rate (Lower is Better)*")
        st.bar_chart(chart_df[["WER"]])
    with c2:
        st.markdown("*BLEU Score (Higher is Better)*")
        st.bar_chart(chart_df[["BLEU"]])

# -----------------------------------------------------------------------------
# TAB 4: Error Taxonomy
# -----------------------------------------------------------------------------
with tab_taxonomy:
    st.subheader("Telugu Linguistic Error Taxonomy")
    st.markdown("Classification of errors based on Telugu phonological rules and orthography:")
    
    tax_df = pd.DataFrame([
        {"Type": "E-01", "Category": "Matra Length", "Description": "Short vs long vowel diacritic confusion", "Corrupted": "దన్ని", "Cleaned": "దీన్ని"},
        {"Type": "E-02", "Category": "Matra Quality", "Description": "Phonetically similar vowel substitution", "Corrupted": "అదృష్టమెనని", "Cleaned": "అదృష్టమేనని"},
        {"Type": "E-03", "Category": "Consonant Voicing", "Description": "Voiced vs unvoiced stop interchange", "Corrupted": "మార్కెడ్", "Cleaned": "మార్కెట్"},
        {"Type": "E-04", "Category": "Mahaprana Aspiration", "Description": "Aspirated vs unaspirated stop confusion", "Corrupted": "బాష", "Cleaned": "భాష"},
        {"Type": "E-05", "Category": "Nasal / Anusvara", "Description": "Anusvara vs dental/retroflex nasal", "Corrupted": "అందమైణది", "Cleaned": "అందమైనది"},
        {"Type": "E-06", "Category": "Sibilant Confusion", "Description": "Interchange of Sha / Sa / Sha (శ / ష / స)", "Corrupted": "విస్వాసం", "Cleaned": "విశ్వాసం"},
        {"Type": "E-07", "Category": "Conjunct Swap", "Description": "Transposition of subscript consonant ligatures", "Corrupted": "ప్చచిక", "Cleaned": "పచ్చిక"},
        {"Type": "E-08", "Category": "Sandhi Space Merging", "Description": "Missing space merging two separate words", "Corrupted": "మతానికిమారక", "Cleaned": "మతానికి మారక"},
        {"Type": "E-09", "Category": "Sandhi Over-splitting", "Description": "Unnecessary space inside compound noun", "Corrupted": "శంభు దాసుడు", "Cleaned": "శంభుదాసుడు"},
        {"Type": "E-10", "Category": "Loanword Spelling", "Description": "Colloquial transcription of English borrowings", "Corrupted": "డ్రిలియన్ల", "Cleaned": "ట్రిలియన్ల"},
        {"Type": "E-11", "Category": "Romanized Tenglish", "Description": "Phonetic Latin script typing", "Corrupted": "baasha", "Cleaned": "భాష"}
    ])
    st.dataframe(tax_df)

# -----------------------------------------------------------------------------
# TAB 5: Batch Evaluation
# -----------------------------------------------------------------------------
with tab_batch:
    st.subheader("Batch Test Evaluation")
    st.markdown("Run batch inference on a sample from `data/synthetic/test.json`:")
    
    test_path = PROJECT_ROOT / "data" / "synthetic" / "test.json"
    if test_path.exists():
        batch_size = st.slider("Number of Test Samples:", 10, 100, 30, step=10)
        if st.button("Run Batch Test"):
            with open(test_path, "r", encoding="utf-8") as f:
                samples_data = json.load(f)[:batch_size]
                
            progress = st.progress(0)
            preds = []
            targets = [s["target"] for s in samples_data]
            inputs = [s["input"] for s in samples_data]
            
            t_start = time.perf_counter()
            for idx, item in enumerate(samples_data):
                res = pipeline.correct(item["input"], mode=active_mode)
                preds.append(res["corrected"])
                progress.progress((idx + 1) / len(samples_data))
            t_total = time.perf_counter() - t_start
            
            exact_matches = sum(1 for p, r in zip(preds, targets) if p.strip() == r.strip())
            acc = (exact_matches / len(preds)) * 100.0
            
            st.success(f"Evaluated {len(preds)} samples in {t_total:.2f} s ({len(preds)/t_total:.1f} sent/s)")
            
            b_col1, b_col2 = st.columns(2)
            b_col1.metric("Exact Match %", f"{acc:.1f}%")
            b_col2.metric("Throughput", f"{len(preds)/t_total:.1f} sent/s")
            
            preview_rows = []
            for i in range(min(8, len(preds))):
                preview_rows.append({
                    "Input": inputs[i],
                    "Target Ground Truth": targets[i],
                    "Model Output": preds[i],
                    "Match": "Exact Match" if preds[i].strip() == targets[i].strip() else "Mismatch"
                })
            st.dataframe(pd.DataFrame(preview_rows))
    else:
        st.warning("Test dataset not found at `data/synthetic/test.json`.")
