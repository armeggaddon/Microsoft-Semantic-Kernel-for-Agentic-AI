from config import CONSTS
from typing import Annotated
from GitHubPlugin.github import GitHubPlugin
from utils.utility import _create_kernel_with_chat_completion
from semantic_kernel.contents import AuthorRole, ChatMessageContent
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies import KernelFunctionSelectionStrategy
from semantic_kernel.functions import KernelFunctionFromPrompt, kernel_function
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.agents.strategies.termination.termination_strategy import TerminationStrategy


def get_tc_manager():

    ORGANISER_NAME = "Co-Ordinator"
    ORGANISER_INSTRUCTIONS = """
        
        As a Coordinator, your role involves gathering requirements from end users to create test cases (TC). Keep in mind to politely redirect any out-of-context questions back to the relevant discussion. Follow these steps:
        1. Begin by greeting the user and asking for the github username. 
        2. Locate all the project with the given username using the GitHub plugin and present the projects to pick one from the list.       
        3. Once the project is selected, retrieve the list of files associated with it and prompt the user to specify the file they wish to work on.
        4. Ask the user to identify specific entities (e.g., classes, methods, functions, etc.) in the chosen file for which the test cases should be generated.
        5. Inquire if the user has any particular test case conditions in mind, but refrain from suggesting any conditions yourself.
        6. Continue engaging with the user to ensure their requirements are clear and fully understood.
        7. Seek confirmation from the user before proceeding further.
        8. Once the plugin generates the test cases, summarize them in concise bullet points and ask the user the following:
        
            Would you like to:
            a. Display the code for approval (Note: Only show the code if the user explicitly requests it.)
            b. Save it in a file (Save the generated test case(s) in a runnable format.)
            If the user chooses option (a), present the generated test case to them.
            If the user selects option (b), save the file in the appropriate format, ensuring the correct file extension based on the code content. Prompt the user for the desired file name.
        """
        
    service_id = "tc_organiser"
    organiser_kernel = _create_kernel_with_chat_completion(service_id)
    
    organiser_kernel.add_plugin(GitHubPlugin(), plugin_name="github")
    organiser_kernel.add_plugin(GroupChatPlugin(), plugin_name="TaskAgent")
    settings = organiser_kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    
    agent_tc_organiser = ChatCompletionAgent(
        service_id=service_id,
        kernel=organiser_kernel,
        name=ORGANISER_NAME,
        instructions=ORGANISER_INSTRUCTIONS,
        arguments=KernelArguments(settings=settings),
    )
    return agent_tc_organiser


def get_developer():
    
    service_id = "testcase_developer"
    
    DEVELOPER_NAME = "Developer"
    DEVELOPER_INSTRUCTIONS = """
        You are a Test Case (TC) developer responsible for creating test cases based on the provided code. 
        Your primary role is to design detailed, accurate, and well-structured test scenarios that align with the given requirements and specifications. 
        Ensure comprehensive coverage, including both functional and edge cases, to validate the system's behavior effectively. 
        The objective is to develop test cases (code) that fulfill user requirements.

        An ideal unit test follows this format:

        Arrange: Prepare the inputs and set up the testing environment.
        Act: Execute the method or function being tested.
        Assert: Verify whether the actual outcome matches the expected results.

        Once your test cases are completed, submit the code for review and communicate any assumptions or clarifications that may be necessary. 
        If feedback indicates that the TC code requires improvement, revise the code thoughtfully and resubmit the updated version.
    """
    agent_tc_developer = ChatCompletionAgent(
        service_id=service_id,
        kernel=_create_kernel_with_chat_completion(service_id),
        name=DEVELOPER_NAME,
        instructions=DEVELOPER_INSTRUCTIONS,
    )    
    return agent_tc_developer, DEVELOPER_NAME


def get_reviewer():
    service_id = "testcase_reviewer"
    
    REVIEWER_NAME = "Reviewer"
    REVIEWER_INSTRUCTIONS = """

    NOTE: DONT GENERATE ANY CODE
    You are a TestCase(TC) reviewer, you review the test case and approve if it satisfies the below conditions
    * you need to ensure that it must have one negative TC as mandatory along with other user requirements
    * Validate that the test cases align with the requirements and are feasible to execute.
    * Once the review is complete, approve the test cases or return them to the developer for revisions with clear instructions.
    once the conditions are satisfied, respond as "Reviewed" also Populate the entire reviewed code in a clean and complete format, ready for use
    IMPORTANT NOTE: Reviewed keyword should accompany with entire reviewed code 
    
    """
    agent_tc_reviewer = ChatCompletionAgent(
        service_id=service_id,
        kernel=_create_kernel_with_chat_completion(service_id),
        name=REVIEWER_NAME,
        instructions=REVIEWER_INSTRUCTIONS,
    )    
    return agent_tc_reviewer, REVIEWER_NAME


def get_group_agent():
    
    developer_agent, DEVELOPER_NAME = get_developer()
    reviewer_agent, REVIEWER_NAME, = get_reviewer()
    
    selection_function = KernelFunctionFromPrompt(
        function_name="selection",
        prompt=f"""
            Determine which participant takes the next turn in a conversation based on the the most recent participant.
            State only the name of the participant to take the next turn.
            No participant should take more than one turn in a row.
    
            Choose only from these participants:
            - {DEVELOPER_NAME}
            - {REVIEWER_NAME}
    
            Always follow these rules when selecting the next participant:
            - After user input, it is {DEVELOPER_NAME}'s turn.
            - After {DEVELOPER_NAME} develops testcase code, it is {REVIEWER_NAME}'s turn
            - If the {REVIEWER_NAME} provides feedback as the code cannot be approved due to the given reasons, it is {DEVELOPER_NAME}'s turn
            - After {DEVELOPER_NAME} rewrites the code it is {REVIEWER_NAME}'s turn
            - Repeat above two steps until the code gets reviewed.
                        
            History:
            {{{{$history}}}}
            """,
    )
    
    group_chat = AgentGroupChat(
        agents=[
            developer_agent,
            reviewer_agent,
        ],
        termination_strategy=ApprovalTerminationStrategy(
            agents=[reviewer_agent],
            maximum_iterations=10,
        ),
        selection_strategy=KernelFunctionSelectionStrategy(
            function=selection_function,
            kernel=_create_kernel_with_chat_completion("selection"),
            result_parser=lambda result: str(result.value[0]) if result.value is not None else developer_agent,
            agent_variable_name="agents",
            history_variable_name="history",
        ),
    )
    return group_chat


class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        if "reviewed" in history[-1].content.lower():
            return True
        else:
            return False


class GroupChatPlugin:
    """A GroupChatPlugin used to provide output based on user input"""

    @kernel_function(description="Provide output on user confirmation with the requirement on test case using the entire chat")
    async def invoke_group_chat(self, content, source_code) -> Annotated[str, "Returns the final output to user"]:
        print("plugin::Group chat invoked")
        print(content)
        
        group_chat = get_group_agent()
        await group_chat.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=str(f"content:{content}, source_code:{source_code}")))
        
        async for content in group_chat.invoke():
            print(f"# Agent - {content.name or '*'}: '{content.content}'")
        
        print(f"# IS COMPLETE: {group_chat.is_complete}")
        # group_chat.is_complete=False
        return content.content
    
    @kernel_function(description="Save all the generated test case code contents to a file with filename")
    async def invoke_save(self, all_test_cases, file_name: Annotated[str, "Name of the file"]) -> Annotated[str, "save the test case code contents to a file"]:
        print("plugin::Save invoked")
        
        with open(f"{CONSTS.local_repo}/{file_name}", 'w') as file:
            file.write(all_test_cases)
            
        return {"all_test_cases":all_test_cases, "file_name":file_name}

