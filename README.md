# Analysing Patterns of Repetition in Child-Adult Dialogues

## Project Overview

The Child Language Feedback Analysis project aims to explore the influence of caregiver feedback on child language development, particularly focusing on various strategies such as repetition, elaboration, corrective feedback, and modeling adult conversation. The project investigates the role of positive and negative feedback in predicting the rapidity of child competency in specific language constructions during child-adult dialogues.

## Objectives

The primary objectives of this project are:
- Automatic detection of different feedback strategies used by caregivers in child-adult dialogues.
- Analyse the capacity of LLMs to generate corrective feedback that is both useful and human like.
- Automatic and Human Evaluation to assess correctness and contextual relevance.

## Methodology

### Dataset 
- The [Talkbank CHILDES Corpora] (https://childes.talkbank.org/access/) will be used for the project.
- The project will focus on age-specific criteria to ensure relevance to the study of child-adult dialogues.
- The data selection procedure will center around ages 1-4, aligning with the critical developmental period for language acquisition.

### Recognising Types of Feedback
- The emphasis will primarily be on positive feedback, this is typically thought of as implicit.
- Positive feedback manifests in the form of modelling examples or corrective feedback.
- To ensure the effectiveness of the approach used, annotations of modelling feedback will be sourced from linguistic experts.

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
