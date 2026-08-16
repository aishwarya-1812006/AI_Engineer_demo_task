# AI Engineer Demo Task

## Overview

This project implements a data collection and processing pipeline for AI ecosystem intelligence.

The pipeline collects information about startups, AI products, research papers, AI/ML jobs and AI news. It also performs entity resolution and provides an LLM extraction layer with handling for large payloads and API rate limits.

## Project Objectives

The main objectives are:

- Collect 1,000+ startup records.
- Collect 1,000+ AI product records.
- Collect 1,000 research-paper records.
- Collect fresh AI/ML job listings.
- Collect fresh AI news from the last 24 hours.
- Normalize and resolve duplicate entity names.
- Convert unstructured information into structured records.
- Handle API rate limits and large LLM payloads.
- Design an architecture capable of scaling to 500k+ records.

## Project Structure

```text
AI_Engineer_demo_task/
│
├── main.py
├── product.py
├── research_papers.py
├── jobs.py
├── news.py
├── entity_resolution.py
├── llm_extraction.py
│
├── startup_data.csv
├── product_data.csv
├── research_papers.csv
├── jobs.csv
├── news.csv
├── entity_mapping_log.csv
│
├── architecture.pdf
├── README.md
└── .gitignore