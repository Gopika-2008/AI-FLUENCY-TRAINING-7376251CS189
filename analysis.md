# Day 1 Analysis: Plain Chatbot vs Rule-Based Workflow vs AI Agent

## 1. Scenario Overview

For this task, I selected a college course fee assistant as my private-data scenario.

The scenario uses a small private course-fee dataset containing the following information:

| Course Code | Course Fee |
|------------|------------:|
| CS101 | ₹12,000 |
| AI202 | ₹18,000 |
| DS303 | ₹15,000 |

The system should answer questions related to course fees, calculate totals and discounts, compare course fees, and also respond to a general request such as writing a welcome message for new AI students.

I implemented the same scenario using three different approaches:

1. Plain Chatbot
2. Rule-Based Workflow
3. AI Agent with Tools

The purpose was to observe how the three approaches differ in terms of private-data access, flexibility, decision-making, tool usage, multi-step task handling, automation, and reliability.

---

# 2. Plain Chatbot

## 2.1 What the Plain Chatbot Uses

The plain chatbot uses an LLM to generate responses to user questions.

In my implementation, the chatbot is connected to the Groq API using the `openai/gpt-oss-20b` model. The chatbot receives the user's question and sends it to the LLM with a system instruction that it is a helpful college assistant.

The chatbot does not use any external tools or programmed fee lookup functions.

The course fee information exists in my project, but the plain chatbot does not directly retrieve that private data when answering the questions.

---

## 2.2 How It Handles a Request

The process is simple:

```text
User Question
      ↓
LLM
      ↓
Generated Response
