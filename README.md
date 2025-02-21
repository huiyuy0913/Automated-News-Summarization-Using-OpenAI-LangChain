# Automated News Summarization Using OpenAI & LangChain

This project automates the **summarization of news articles** using **LangChain** and **OpenAI’s GPT model**. It processes `.docx` news files, extracts key themes in **Chinese**, and generates structured summaries in **English**.

---

## 🚀 **Features**
- ✅ Reads `.docx` news articles and processes multiple files in batches.
- ✅ Uses **LangChain’s MapReduceDocumentsChain** to extract key themes in **Chinese** and generate structured **English summaries**.
- ✅ Splits long text into smaller chunks using **CharacterTextSplitter** for better accuracy.
- ✅ Automates text extraction, summarization, and structured output generation.

---

## 🔹 **Codes**
- ✅ [summarize_newspaper.py](https://github.com/huiyuy0913/Automated-News-Summarization-Using-OpenAI-LangChain/blob/main/summarize_newspaper.py) automates summarization of news articles stored as .docx files using OpenAI’s GPT model. It reads text from documents, breaks it into smaller chunks, generates summaries in Chinese, translates them into English, and further refines them into a structured five-point summary.
- ✅ [langchain_summarize_newspaper.py](https://github.com/huiyuy0913/Automated-News-Summarization-Using-OpenAI-LangChain/blob/main/langchain_summarize_newspaper.py) automates news summarization from .docx files using LangChain and OpenAI’s GPT model. It extracts key themes in Chinese, then refines them into five structured points in English. The process follows a Map-Reduce approach for efficient text processing.
