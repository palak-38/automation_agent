 # **PALAK | MECHANICAL ENGINEERING | IIT JAMMU**
# **AI AGENT FOR ACTION ITEMS EXTRACTION FROM CHAT DIALOGUE** 

## **1. Problem Statement:**

In any collaborative environment, from student group projects to professional teams, important action items are often scattered throughout long and unstructured chat logs on platforms like WhatsApp, Discord, or Telegram. Manually sifting through hundreds of messages to identify tasks, owners, and deadlines is a time-consuming, tedious, and error-prone process. This inefficiency frequently leads to missed commitments and a lack of clarity on team responsibilities.

## **2. Solution Overview**

This project introduces an intelligent AI agent designed to automate the process of action item extraction. The agent ingests raw, unstructured chat dialogues and outputs a clean, structured list of tasks in JSON format. Each extracted item includes the core components of an actionable task: the task description, the assigned owner, and the specified due date.

Please find Model Architecture, Fine Tuning Setup and Interaction Logs with the LLM in the **`info`**  folder.


-----
Below are the screenshots of the UI created via gradio, where we paste the chat and extract actionable items, with deadline and assignee.

<img width="1919" height="908" alt="Screenshot 2025-09-16 001157" src="https://github.com/user-attachments/assets/f524d10d-6535-40b2-a102-0b218b90aecb" />
<img width="1919" height="908" alt="IMG-20250916-WA0019 1" src="https://github.com/user-attachments/assets/b13a609f-e31b-4aaf-aac3-a34008eed81b" />


----
## 🚀 How to Use
1. *Fork the repository.*
2. *Clone the forked repository*
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>

3. *Create and activate a new Conda environment*
    ```bash
    conda create -n chatapp python=3.10 -y
    conda activate chatapp

4. *Install the dependencies*
    ```bash
    pip install -r requirements.txt

5. **Run the application**
    ```bash
    python app.py

6. *Open the app in your browser*
    ```bash
    http://127.0.0.1:8000
