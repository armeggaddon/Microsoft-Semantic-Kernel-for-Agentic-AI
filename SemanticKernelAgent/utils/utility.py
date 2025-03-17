import logging
from config import CONSTS
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
 
logger = logging.getLogger(__name__)

def _create_kernel_with_chat_completion(service_id: str) -> Kernel:
    kernel = Kernel()

    kernel.add_service(
        AzureChatCompletion(
            service_id=service_id,
            deployment_name=CONSTS.engine_name,
            endpoint=CONSTS.api_endpoint,
            api_key=CONSTS.api_key,
            api_version=CONSTS.api_version
        ),
    )        
    return kernel
