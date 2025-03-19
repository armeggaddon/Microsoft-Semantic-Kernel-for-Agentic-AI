# 🚀 Microsoft Semantic Kernel for Agentic AI  
   
Welcome to the **Microsoft Semantic Kernel for Agentic AI** repository! This resource is designed to help beginners leverage Semantic Kernel for building powerful AI agents.   
  
---  
   
## 🧰 Pre-requisites  
   
To get started, you'll need the following:  
   
- **FastAPI Framework**    
   FastAPI is used to host Semantic Kernel components as a service, enabling interaction with the chatbot seamlessly.    
  
- **Gradio**    
   Gradio helps in building a stunning and interactive chatbot interface.    
  
- **Azure OpenAI Compatibility**    
   This project is crafted exclusively for **Azure OpenAI** subscribers. Semantic Kernel features used here strictly adhere to classes compatible with Azure OpenAI.  
   
---  
   
📚 **Learn More**    
Curious to dive deeper? Explore the official documentation for the tools used in this project:    
- [FastAPI Documentation](https://fastapi.tiangolo.com/)    
- [Gradio Documentation](https://gradio.app/)    
  

# Test Case Management System 🚀    
With **Semantic Kernel Components**  
   
Welcome to the **Test Case Management System**, powered by **Semantic Kernel**! This framework combines cutting-edge AI capabilities with structured workflows, making it easy to create, review, and manage test cases collaboratively. Below, we break down the system's components and structure, showcasing how Semantic Kernel plays a pivotal role in enabling intelligent and dynamic behavior.  
   
---  
   
## ✨ Highlights of Semantic Kernel Components  
   
This project leverages **Semantic Kernel**'s modular and extensible components, such as **Kernel Functions**, **Agents**, **Plugins**, and **Strategies**, to create an intelligent test case lifecycle management system.  
   
Here’s how the main Semantic Kernel components are utilized:  
   
---  
   
### 🛠️ **Kernel Functions**  
   
#### **1. Chat Completion**  
The backbone of the system is built on **Chat Completion Agents**, which enable dynamic and intelligent behavior. Each agent is instantiated with a **service_id**, specified instructions, and configurations (**KernelArguments**) to simulate specialized roles:  
- **Coordinator Kernel**: Initializes the Coordinator with the ability to interact with the user and retrieve project details from GitHub.  
- **Developer Kernel**: Focuses on the task of creating detailed test cases from requirements.  
- **Reviewer Kernel**: Ensures validation and approval of test cases based on stringent criteria.  
   
#### **2. Kernel Function Execution**  
Kernel functions enable the execution of dynamic prompts and decisions:  
- **_create_kernel_with_chat_completion()**: Generates a kernel instance that connects agents to AI-backed completion strategies.  
- **FunctionChoiceBehavior.Auto()**: Automatically selects the most relevant agent to fulfill the next action.  
   
---  
   
### 🕵️ **Agents**  
   
The system operates through three key **ChatCompletionAgents**:  
#### **1. Coordinator Agent**  
The Coordinator orchestrates initial interactions with the user by:  
- Collecting requirements via structured conversation.  
- Leveraging **GitHubPlugin** to fetch projects, files, and entities.  
- Summarizing and presenting test cases for user review.  
   
#### **2. Developer Agent**  
The Developer agent creates functional test case code:  
- Uses the **Arrange**, **Act**, **Assert** methodology.  
- Refines test cases iteratively based on Reviewer feedback.  
   
#### **3. Reviewer Agent**  
The Reviewer agent is responsible for strict validation:  
- Enforces mandatory inclusion of at least one negative test case.  
- Approves or rejects test cases and provides feedback for refinement.  
   
---  
   
### 🔌 **Plugins**    
Plugins in Semantic Kernel enable external integrations and efficient task execution.  
   
#### **GitHub Plugin**  
- Integrated to analyze and retrieve projects, files, and entities directly from GitHub.    
- Facilitates interaction between user inputs and real-world repositories.  
   
#### **GroupChat Plugin**  
- Handles final output summaries through collaboration among multiple agents, pulling insights from the entire agent-driven conversation.  
   
#### **File Save Plugin**  
- Saves approved test case code in the desired format using the appropriate file extension.  
   
---  
   
### 🎯 **Strategies**  
   
#### **1. Selection Strategy**  
The **KernelFunctionSelectionStrategy** dynamically chooses which agent takes the next turn based on the conversational history:  
- User interactions initiate the Developer agent.  
- Feedback cycles alternate between Developer and Reviewer until the test case code is approved.  
   
#### **2. Termination Strategy**  
The **ApprovalTerminationStrategy** determines when the workflow completes:  
- Ends the loop once the Reviewer evaluates the test case and marks it as "Reviewed."  
- Prevents infinite iterations by limiting the maximum number of cycles.  
   
#### **3. Behavior Execution**  
The **FunctionChoiceBehavior** ensures agents execute their roles autonomously using AI-powered decision-making.  
   
---  
   
### 🤝 **Agent Collaboration: Group Chat**  
   
The **AgentGroupChat** facilitates dynamic collaboration among the three agents:  
1. User requirements are gathered by the Coordinator.  
2. The Developer creates test case code based on these requirements.  
3. The Reviewer validates and approves the test cases.  
4. Iterative cycles continue until the test case code is finalized, approved by the Reviewer, and saved.  
   
The **selection rules** embedded in the Kernel Function ensure an organized turn-based conversation flow between agents based on the semantic history of their interactions.  
   
---  
   
## ➿ Test Case Lifecycle Flow  
   
### **Interactive Workflow**  

<img src="https://github.com/armeggaddon/Microsoft-Semantic-Kernel-for-Agentic-AI/blob/main/sk_flow_diagram.png" alt="Microsoft Semantic Kernel Agentic AI" width="600" height="400">
   
### **Agent Termination**  
The process intelligently terminates once the Reviewer approves the test case and outputs the finalized code.  
   
---  
   
## 🔍 How Does It Work?  
   
### 1. **Coordinator Initialization**  
   - Use `get_tc_manager()` to launch the Coordinator agent.  
   - Captures user requirements via structured conversation.  
   - Interacts with GitHub repositories using **GitHub Plugin**.  
   
### 2. **Collaborative Multi-Agent Workflow**  
   - Instantiate Developer and Reviewer agents (`get_developer()` and `get_reviewer()`).  
   - Generate dynamic group chat (`get_group_agent()`) to execute turn-based collaboration.  
   
### 3. **Saving the Test Cases**  
   - Use the `invoke_save()` function in the `GroupChatPlugin` to persist approved test case code in desired formats and filenames.  
   
---  
   
## 🏋️ Semantic Kernel Components in Action  
   
### **Dynamic Prompt Construction**  
Agents use prompt-based instructions embedded in the kernel. For instance, the Developer prompt illustrates constructing test cases using the **Arrange-Act-Assert** structure.  
   
### **Efficient Functionality**  
Each agent behaves intelligently based on its specific design:  
- Developer produces code aligned with user requirements.  
- Reviewer enforces constraints such as mandatory negative tests.  
- Coordinator organizes user feedback into actionable insights.  
   
### **Modular Plugins**  
Plugins, such as the GitHub Plugin and Save Plugin, extend functionality by enabling rich repositories integration and seamless file export.  
   
---  
   
## 🚦 Extensibility and Future Directions  
   
This system is designed for modularity and extensibility:  
- Add additional agents for specialized roles (e.g., Security test creation).  
- Enhance Reviewer criteria for more stringent validations.  
- Integrate CI/CD pipelines to automatically execute saved test cases.  
- Expand plugins for tools like **JIRA**, **Slack**, or **Azure DevOps**.  
   
---  
   
## 🧠 Technologies Used  
   
- **Semantic Kernel**:  
   Enables prompt engineering, function selection, agent orchestration, and dynamic AI-backed workflows.  
- **GitHub Plugin**:  
   Integrates with GitHub APIs for repository analysis.  
- **Python Async Framework**:  
   FastAPI Ensures efficient and scalable asynchronous execution.  
- **Gradio Chatbot**:  
   Helps user to interact with the Agents.     
  
   
---  

## ▶️ Quick Start

Clone the repo, pip install the requirements and refer the video to progress

https://www.youtube.com/watch?v=OwgAvdYUArA

```
<iframe width="560" height="315" src="[https://www.youtube.com/embed/<VIDEO_ID>](https://www.youtube.com/watch?v=OwgAvdYUArA)" title="Microsoft Semantic Kernel Agentic AI" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
```
---
   
This system demonstrates the power of **Semantic Kernel** in enabling intelligent multi-agent collaboration for complex tasks like test case creation and management. Join us in making software testing smarter, faster, and more collaborative! 🎉
