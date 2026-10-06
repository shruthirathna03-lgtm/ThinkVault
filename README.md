# ThinkVault

### An AI-Powered Knowledge Intelligence and Productivity Assistant

> Think smarter. Work better. Discover more.

## About the Project

ThinkVault is an AI-powered knowledge management and productivity application that helps users interact with their uploaded documents and images.

Users can upload PDF, DOCX, PNG, JPG, and JPEG files and ask questions about their content. ThinkVault uses Retrieval-Augmented Generation (RAG), ChromaDB, embeddings, and locally hosted AI models through Ollama to provide relevant responses.

## Features

- Upload PDF and DOCX documents
- Upload and analyse images
- Extract text from documents
- Store document information using ChromaDB
- Retrieve relevant information using RAG
- Ask questions about uploaded content
- Summarize and explain content
- Identify missing information
- Suggest improvements and additional information
- Local AI processing using Ollama
- No external API key required
- Streamlit-based user interface

## Supported File Types

- PDF (`.pdf`)
- Word Document (`.docx`)
- PNG Image (`.png`)
- JPEG Image (`.jpg`)
- JPEG Image (`.jpeg`)

## Technologies Used

- Python
- Streamlit
- ChromaDB
- Sentence Transformers
- Ollama
- Llama 3.2
- Gemma 3
- pypdf
- python-docx
- Pillow

## System Architecture

```text
User
  ↓
ThinkVault Streamlit Interface
  ↓
PDF / DOCX / Image
  ↓
Document & Image Processing
  ↓
ChromaDB + Embeddings
  ↓
RAG
  ↓
Ollama
  ↓
Local AI Model
  ↓
ThinkVault AI Assistant