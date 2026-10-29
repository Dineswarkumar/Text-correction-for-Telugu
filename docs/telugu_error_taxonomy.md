# Telugu Error Taxonomy

This document outlines a comprehensive taxonomy of errors commonly found in Telugu digital text. This taxonomy serves as the foundational guideline for dataset annotation and synthetic error generation in our text correction pipeline.

## 1. Error Classification Hierarchy

### 1.1 Spelling Errors

#### Matra (Vowel Sign) Confusion
*   **Definition:** Incorrect usage of vowel diacritics (matras) that attach to consonants. Often caused by phonetic similarity or typing errors on digital keyboards.
*   **Examples:**
    *   ి (short 'i') vs ీ (long 'ee'): `చిన్న` (correct) vs `చీన్న` (incorrect)
    *   ు (short 'u') vs ూ (long 'oo'): `పుస్తకం` (correct) vs `పూస్తకం` (incorrect)
    *   ె (short 'e') vs ే (long 'ae'): `తెలుగు` (correct) vs `తేలుగు` (incorrect)
    *   ొ (short 'o') vs ో (long 'oa'): `కొత్త` (correct) vs `కోత్త` (incorrect)
*   **Why it occurs:** Visual similarity on keyboards; phonetic indistinguishability in rapid speech.
*   **Frequency:** Very High
*   **Detection Difficulty:** Easy (often results in non-words) to Medium (if it forms a real but incorrect word).

#### Consonant Confusion
*   **Definition:** Substituting one consonant for another that sounds similar but changes the meaning or correctness of the word.
*   **Examples:**
    *   ణ (ṇa) vs న (na): `కారణం` (correct) vs `కారణo/కారనం` (incorrect)
    *   శ (sha), ష (ṣa), స (sa): `ఆకాశం` (correct) vs `ఆకాసం` (incorrect)
    *   ట (ṭa) vs డ (ḍa): `పాట` (correct) vs `పాడ` (incorrect, changes meaning)
    *   బ (ba) vs వ (va): Context-dependent regional variations sometimes incorrectly written.
*   **Why it occurs:** Phonetic similarity and regional pronunciation variations.
*   **Frequency:** High
*   **Detection Difficulty:** Medium.

#### Halant (Virama) Errors
*   **Definition:** Missing the virama (్) which is required to form conjunct consonants (vattulu), resulting in separate full consonants instead of a combined syllable.
*   **Examples:**
    *   `అమ్మ` (correct) vs `అమమ` (incorrect - missing virama between మ and మ)
    *   `విద్య` (correct) vs `విదయ` (incorrect)
*   **Why it occurs:** Typing errors; unfamiliarity with digital input methods for Indic scripts.
*   **Frequency:** Medium
*   **Detection Difficulty:** Easy.

#### Anusvara / Visarga Errors
*   **Definition:** Incorrect usage of the nasal Anusvara (ం) or Visarga (ః).
*   **Examples:**
    *   ం vs ను: `అతను` (correct) vs `అతం` (incorrect in formal context)
    *   Missing Visarga: `దుఃఖం` (correct) vs `దుఖం` (incorrect)
*   **Why it occurs:** Pronunciation shortcuts translating to text.
*   **Frequency:** Low to Medium
*   **Detection Difficulty:** Easy.

---

### 1.2 Morphological Errors

#### Sandhi (Word Junction) Errors
*   **Definition:** Incorrect splitting or merging of words. Telugu extensively uses Sandhi, where adjacent words morphophonemically combine.
*   **Examples:**
    *   Incorrect split: `రామాలయం` (correct) vs `రామ ఆలయం` (grammatically awkward if not properly spaced/contextualized)
    *   Incorrect merge: `అతను వచ్చాడు` (correct) vs `అతనువచ్చాడు` (incorrect)
*   **Why it occurs:** Misunderstanding of grammatical rules; typing fast without spaces.
*   **Frequency:** High
*   **Detection Difficulty:** Hard (requires semantic and syntactic context).

#### Suffix/Vibhakti Errors
*   **Definition:** Incorrect use of postpositions/case markers (vibhakti) attached to nouns.
*   **Examples:**
    *   `రాముడికి` (correct: to Ramu) vs `రాముడిని` (incorrect if the context implies "to Ramu", implies "Ramu (object)")
*   **Why it occurs:** Poor grammatical grasp; literal translation from other languages.
*   **Frequency:** Medium
*   **Detection Difficulty:** Hard (requires deep contextual understanding).

---

### 1.3 Word Boundary Errors
*   **Definition:** Incorrect insertion or deletion of spaces between words (unrelated to Sandhi rules).
*   **Examples:**
    *   Space insertion: `నమస్కారం` (correct) vs `నమస్ కారం` (incorrect)
    *   Space deletion: `నేను వెళ్తున్నాను` (correct) vs `నేనువెళ్తున్నాను` (incorrect)
*   **Why it occurs:** Typographical errors.
*   **Frequency:** Medium
*   **Detection Difficulty:** Medium.

---

### 1.4 Transliteration Errors
*   **Definition:** Errors arising when users type in English (Roman script) and an IME (Input Method Editor) converts it incorrectly to Telugu.
*   **Examples:**
    *   Ambiguous mapping: Typing "nenu" might map to `నేను` (correct) or `నెను` (incorrect).
    *   Inconsistent Tenglish spelling: Typing "baagundhi" vs "bagundi" leading to different phonetic mappings.
*   **Why it occurs:** Lack of standardized Roman-to-Telugu mapping rules.
*   **Frequency:** Very High (in user-generated content).
*   **Detection Difficulty:** Medium.

---

### 1.5 Code-Mixing Errors
*   **Definition:** Incorrect grammatical structures resulting from mixing Telugu and English in the same sentence.
*   **Examples:**
    *   `నేను school కి వెళ్తున్నాను` (Acceptable Tenglish) vs `నేను school వెళ్తున్నాను` (Missing postposition 'కి')
*   **Why it occurs:** Casual digital communication habits.
*   **Frequency:** High.
*   **Detection Difficulty:** Hard.

---

### 1.6 Dialectal Variations
*   **Definition:** Using regional dialect words in a context that requires formal/Standard Telugu, or mixing registers.
*   **Examples:**
    *   Andhra vs Telangana: `బాగుంది` (Standard/Andhra - Good) vs `మస్తు ఉంది` (Telangana informal).
    *   Formal vs Informal: `భోజనం చేసారా?` (Formal) vs `తిన్నావా?` (Informal).
*   **Why it occurs:** Regional background of the writer.
*   **Frequency:** Medium (Context-dependent).
*   **Detection Difficulty:** Hard (Requires style/register classification).

---

## 2. Summary Table

| Error Category | Sub-type | Frequency | Detection Difficulty | Example (Incorrect → Correct) |
| :--- | :--- | :--- | :--- | :--- |
| **Spelling** | Matra Confusion | Very High | Easy-Medium | చీన్న → చిన్న |
| **Spelling** | Consonant Confusion | High | Medium | ఆకాసం → ఆకాశం |
| **Spelling** | Halant/Virama missing | Medium | Easy | అమమ → అమ్మ |
| **Spelling** | Anusvara/Visarga | Low-Medium| Easy | దుఖం → దుఃఖం |
| **Morphological**| Sandhi Errors | High | Hard | రామ ఆలయం → రామాలయం |
| **Morphological**| Suffix Errors | Medium | Hard | రాముడిని → రాముడికి (contextual)|
| **Word Boundary**| Space Issues | Medium | Medium | నేనువెళ్తున్నాను → నేను వెళ్తున్నాను |
| **Transliteration**| IME Mapping | Very High | Medium | నెను → నేను |
| **Code-Mixing** | Syntax mismatches | High | Hard | నేను school వెళ్తున్నాను → నేను school కి వెళ్తున్నాను |
| **Dialectal** | Register mixing | Medium | Hard | మస్తు ఉంది → బాగుంది (in formal text) |

---

## 3. Annotation Guidelines

When annotating data or generating synthetic errors for the dataset, annotators must adhere to the following rules:
1.  **Tagging:** Every identified error must be tagged with its corresponding category from the hierarchy (e.g., `<ERR_SPELL_MATRA>`, `<ERR_MORPH_SANDHI>`).
2.  **Minimal Edit Distance:** Provide the correction that requires the minimum number of character edits to fix the word, while preserving the original meaning.
3.  **Context is King:** For morphological and dialectal errors, the entire sentence must be read to determine the correct fix. Do not correct dialectal variations unless the target domain strictly requires "Standard Formal Telugu".
4.  **Code-Mixing Handling:** If a sentence contains an English word, ensure the attached Telugu suffix (vibhakti) is grammatically correct. Do not translate the English word to Telugu unless specified by the task.
5.  **Multi-Error Words:** If a single word contains multiple errors (e.g., a matra error AND a missing virama), apply both corrections and tag it with `<ERR_MULTI>`.
