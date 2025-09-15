<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Development Log: A Collaborative AI Agent Project

## Project Overview

This document provides a chronological log of the development process for the **Action Item Extractor AI agent**, a project undertaken to fulfill the requirements of an internship assignment. The project was developed through a collaborative methodology, wherein a developer directed the project's course while leveraging an AI assistant (Gemini) for code generation, debugging support, and strategic consultation.

***

## Day 1: Project Scaffolding, Data Generation, and Initial Hurdles

### Objective

To establish the project environment, create a baseline for performance comparison, and generate a custom dataset for the subsequent fine-tuning phase.

### Interaction Summary

#### Initial Setup and API Selection

- **Developer**: The initial project plan and assignment requirements were provided.
- **AI Assistant**: The provided documents were analyzed, and the proposed plan was validated. A constraint was identified regarding the unavailability of OpenAI API keys.
- **Resolution**: As a solution, the utilization of the **Groq API** was proposed, offering a high-performance, cost-effective alternative. An initial baseline script was subsequently modified to use `groq` in place of `openai`.


#### LLM-Assisted Data Generation

- **Developer**: The primary objective of creating a bespoke dataset for fine-tuning was articulated.
- **AI Assistant**: A strategy of **"LLM-assisted labeling"** was proposed. A Python script (`1_create_finetuning_dataset.py`) was generated to automate this process. The script was designed to:
    - Filter the source dataset for relevant conversations
    - Employ the `llama3-70b-8192` model via the Groq API
    - Generate structured JSON outputs


#### Data Cleaning and Validation

- **Developer**: The manual curation of the generated `prepared_data.jsonl` file was identified as a laborious and potentially inconsistent process.
- **AI Assistant**: To address this challenge, a dedicated data-cleaning script (`2_clean_and_validate_dataset.py`) was developed. This script automated critical tasks, including:
    - ✅ Validation of JSON structures
    - ✅ Normalization of date formats
    - ✅ Isolation of entries that could not be programmatically corrected

This transformed a time-intensive manual task into an efficient, streamlined review process.


### Day 1 Outcome

🎯 **Success**: The foundational stage of the project was successfully concluded, resulting in a high-quality, clean dataset and an initial draft of the system architecture document. All initial obstacles were systematically addressed and overcome.

***

## Day 2: The Fine-Tuning Process on Cloud Platform

### Objective

To fine-tune a language model on the custom dataset utilizing a cloud-based GPU and subsequently integrate the resulting model locally.

### Interaction Summary

#### Transition to Cloud Infrastructure (Kaggle)

- **Developer**: The absence of a local GPU necessitated the use of a cloud platform for model training.
- **AI Assistant**: A modified fine-tuning script (`3_finetuning_t5_lora.py`) was provided, specifically adapted for the Kaggle environment, which included the integration of **Kaggle Secrets** for secure management of the `GROQ_API_KEY`.


#### Resolution of Dependency Conflicts

##### Problem 1: Network Restrictions

- **Initial Problem**: The `pip install` command failed due to the default network restrictions within the Kaggle notebook environment.
- **Solution**: The AI identified the specific setting that required modification.


##### Problem 2: ImportError

- **Issue**: Following the initial installations, the script encountered an `ImportError`, indicating a dependency conflict among the installed versions of `transformers`, `peft`, and `torch`.
- **Iterative Solution**: This initiated a systematic, multi-step debugging process:

1. Developer executed the script and provided screenshots of resulting errors
2. AI analyzed the tracebacks to propose more stable library versions
3. This iterative feedback loop proved crucial for establishing a compatible and functional environment


##### Problem 3: AttributeError

- **Critical Error**: `AttributeError: 'MatmulLtState' object has no attribute 'memory_efficient_backward'` was encountered.
- **Definitive Solution**:
    - Diagnosed as a critical incompatibility between the `peft` and `bitsandbytes` libraries
    - A final, well-researched set of compatible library versions was provided
    - Notebook was restructured into a **two-cell workflow**:
        - Cell 1: Installation
        - Cell 2: Main script (separated by mandatory kernel restart)
    - This is a standard practice for resolving such conflicts


#### Model Upgrade and Performance Enhancement

- **Developer**: An evaluation of the initial `t5-small` model indicated performance limitations.
- **AI Assistant**:
    - Analysis determined that the model's limited capacity and lack of instruction-tuning were probable causes for suboptimal performance
    - Recommended upgrade to the `google/flan-t5-base` model
    - Explained that this would require re-executing the fine-tuning process but was anticipated to yield substantially improved results


### Day 2 Outcome

🚀 **Achievement**: Following a rigorous and methodical debugging process, a powerful `google/flan-t5-base` model was successfully fine-tuned on the custom-prepared dataset.

***

## Day 3: System Integration, UI Development, and Final Deliverables

### Objective

To integrate the trained model into a local agent pipeline, develop a user interface, and prepare the final project reports.

### Interaction Summary

#### Local Integration

- **Developer**: Upon completion of the training and subsequent download of the model adapter, the next phase involved its integration into the local agent pipeline.
- **AI Assistant**: A complete local script (`5_run_agent_pipeline.py`) was provided. This script demonstrated how to:
    - Load the model adapter
    - Apply the full agent logic (Planner, Extractor, Validator, Executor)
    - Process a sample chat from end to end


#### UI Development

- **Developer**: Asked how to create a UI for the functional agent.
- **AI Assistant**:
    - Recommended **Gradio** as the ideal tool
    - Provided a complete, self-contained `app.py` script
    - The script wrapped the agent pipeline into an interactive web interface with:
        - 📝 Input text boxes
        - 📊 Output tables
        - 🔘 Example buttons


### Day 3 Outcome

✨ **Final Success**: Complete integration of the fine-tuned model into a functional, user-friendly web interface ready for demonstration and deployment.

***

## Technical Stack Summary

| Component | Technology | Purpose |
| :-- | :-- | :-- |
| **Base Model** | `google/flan-t5-base` | Pre-trained language model |
| **Fine-tuning** | LoRA (Low-Rank Adaptation) | Efficient parameter-efficient training |
| **API Service** | Groq API (`llama3-70b-8192`) | Data generation and labeling |
| **Cloud Platform** | Kaggle | GPU-accelerated model training |
| **UI Framework** | Gradio | Interactive web interface |
| **Agent Architecture** | Multi-stage Pipeline | Planner → Extractor → Validator → Executor |


***

## Key Learnings and Best Practices

### 🔧 Technical Insights

1. **Dependency Management**: Library version compatibility is critical in ML environments
2. **Cloud Integration**: Kaggle Secrets provide secure API key management
3. **Model Selection**: Instruction-tuned models (`flan-t5`) significantly outperform base models for structured tasks
4. **Data Quality**: LLM-assisted labeling with human validation creates high-quality training data

### 🤝 Collaborative Development

1. **Iterative Problem Solving**: Screenshot-based debugging accelerated issue resolution
2. **Strategic Planning**: AI assistant provided valuable architectural recommendations
3. **Code Generation**: Automated script creation significantly reduced development time
4. **Quality Assurance**: Systematic validation prevented downstream issues

***

## Project Metrics

- **📊 Dataset Size**: 300+ high-quality action item examples
- **⏱️ Training Time**: ~2 hours on Kaggle GPU
- **🎯 Model Performance**: Significant improvement over baseline
- **🚀 Deployment**: Fully functional web interface
- **📅 Timeline**: 3-day rapid development cycle

***

## Conclusion

This collaborative AI-assisted development project demonstrates the effectiveness of human-AI partnership in rapid prototyping and system development. The systematic approach to problem-solving, combined with iterative feedback and strategic AI consultation, resulted in a successful, production-ready action item extraction system within a compressed timeline.

The project showcases modern AI development practices including parameter-efficient fine-tuning, cloud-based training, and user-friendly interface design, making it a comprehensive example of contemporary AI application development.
<span style="display:none">[^1][^2][^3][^4][^5][^6][^7][^8][^9]</span>

<div style="text-align: center">⁂</div>

[^1]: https://noteplan.co/templates/ai-project-planning-tracking-template

[^2]: https://www.visor.us/templates/project-tracker-templates/

[^3]: https://www.notion.com/templates/category/projects

[^4]: https://bit.ai/templates/project-management-template

[^5]: https://clickup.com/templates/project-plan/ai

[^6]: https://www.smartsheet.com/content/google-sheets-project-management-templates

[^7]: https://www.taskade.com/templates/design/design-project-log

[^8]: https://technology.berkeley.edu/TPO/toolkit/templates-all

[^9]: https://www.yoroflow.com/project-management-templates

