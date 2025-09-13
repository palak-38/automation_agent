
# **AI Agent for Action Item Extraction from Chat Dialogues** 

**1. Problem Statement:**

In any collaborative environment, from student group projects to professional teams, important action items are often scattered throughout long and unstructured chat logs on platforms like WhatsApp, Discord, or Telegram. Manually sifting through hundreds of messages to identify tasks, owners, and deadlines is a time-consuming, tedious, and error-prone process. This inefficiency frequently leads to missed commitments and a lack of clarity on team responsibilities.

**2. Solution Overview**

This project introduces an intelligent AI agent designed to automate the process of action item extraction. The agent ingests raw, unstructured chat dialogues and outputs a clean, structured list of tasks in JSON format. Each extracted item includes the core components of an actionable task: the task description, the assigned owner, and the specified due date.

This tool transforms messy conversations into organized to-do lists, ensuring that no commitment is ever lost in the noise of a busy group chat.

**3. Core Architecture & Key Features**

The agent is built on a multi-component architecture, where each part has a specialized role:

**Planner (LLM):** A general-purpose LLM that first analyzes the chat to determine the overall context and strategy.

**Extractor (Fine-Tuned Model):** The core of the agent. This is a t5-small model that has been specifically fine-tuned using LoRA (Low-Rank Adaptation) for the single, critical task of generating reliable, schema-compliant JSON. By specializing the model, we achieve a much higher degree of accuracy and structural consistency than is possible with general-purpose prompting.

**Validator & Executor:** Simple, rule-based modules that clean the generated JSON and format the final output.

This project directly implements the core requirements of the assignment by building and integrating a custom fine-tuned model to solve a real-world automation problem.
