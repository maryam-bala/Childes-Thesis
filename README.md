# Analysing Patterns of Repetition in Child-Adult Dialogues

## Project Overview

The interactions between caregivers and children play a pivotal role in shaping linguistic competencies of children. One intriguing aspect of this exchange is the feedback provided by caregivers during dialogues, wherein repetition serves as a powerful mechanism for language acquisition. The primary goal of this project is to study patterns of repetition in child-adult dialogues, focusing on the diverse feedback strategies employed by caregivers. These strategies encompass positive repetitions that affirm correct language constructions or corrected versions of the child's attempts.

## Objectives

The primary objectives of this project are:
- Automatic detection of different feedback strategies used by caregivers in child-adult dialogues.
- Deploy LLMs to generate corrective feedback that is both useful and human like.
- Automatic and Human Evaluation to assess correctness and contextual relevance.

## Methodology

### Dataset 
- The [Talkbank CHILDES Corpora](https://childes.talkbank.org/access/) will be used for the project.
- The project will focus on age-specific criteria to ensure relevance to the study of child-adult dialogues.
- The data selection procedure will center around ages 1-4, aligning with the critical developmental period for language acquisition.

### Recognising Types of Feedback
- The emphasis will primarily be on positive feedback, this is typically thought of as implicit.
- Positive feedback manifests in the form of modelling examples or corrective feedback.
- To ensure the effectiveness of the approach used, annotations of feedback will be sourced from linguistic experts.

### Generating feedback
- Large Language Models (LLMs) will be used to generate feedback
- To ensure precision in feedback generation, the project will define a small set of contexts.
- These contexts will serve as the foundation for generating contextually appropriate feedback within the interactions between children and adults.

### Automatic metrics: Bleu score and BERTscore 
- To quantitatively evaluate the performance of the feedback generation models, the project will employ two widely recognized automatic metrics: Bleu score and BERTscore.

### Human Evaluation
- In addition to automated metrics, human evaluators will assess the generated feedback for correctness, appropriateness, and contextual relevance.
- This qualitative assessment ensures a comprehensive understanding of the generated feedback's effectiveness in real-world conversational contexts.

## Expected Outcomes
The outcomes of this project are expected to:
- Shed light on how children exploit caregiver feedback to advance their conversational skills.
- Provide insights into the types of repetitions and interactions that can positively influence child language development.
- Have implications for the design of future conversational agents and human-computer interactions.
