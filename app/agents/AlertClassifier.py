from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableSequence
from langchain_core.language_models.llms import BaseLLM
from .Agent import BaseLangChainAgent
from ..services.PromptManager import PromptManager
from pathlib import Path
from config import settings

class AlertClassifier(BaseLangChainAgent):
    """
    Agent specialized in classifying alerts into categories.
    """

    def __init__(self, model_name: str = "llama3.2:3b"):
        """
        Initializes the AlertClassifier agent.

        :param model_name: Name of the Ollama model to use (default: "llama3.2:3b").
        """
        # Initialize the Ollama language model
        llm = Ollama(model=model_name,
                     base_url=settings.OLLAMA)
        super().__init__(llm)

    def _initialize_chain(self) -> RunnableSequence:
        """
        Initializes the LangChain chain for the AlertClassifier agent using RunnableSequence.

        Returns:
            RunnableSequence: A sequence that processes input using the prompt and LLM.
        """
     
        prompt_template = self.get_prompt_template()
        
        prompt = PromptTemplate(
            input_variables=["input"],
            template=prompt_template
        )
        
        chain = prompt | self.llm
        
        return chain

    def get_prompt_template(self, file_name: str = "alert_classifier.txt") -> str:
        try:
        
            current_dir = Path(__file__).resolve().parent
            prompt_path = current_dir.parent / "prompts" / file_name

            if not prompt_path.exists():
                return f"Error: El archivo {prompt_path} no existe."

            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()

        except Exception as e:
            return f"Error al obtener el template: {str(e)}"

        
    def process_input(self, alert_description: str) -> str:
        """
        Classifies an alert into a category.

        :param alert_description: Description of the alert.
        :return: Category of the alert (e.g., "Critical", "High", "Medium", "Low").
        """
        chain = self._initialize_chain()
        
        category = chain.invoke({"input": alert_description})
        
        return category.strip()  

    def classify(self, alert_description: str) -> str:
        """
        Public method to classify an alert. Calls process_input internally.

        :param alert_description: Alert text to classify.
        :return: Classification result.
        """
        return self.process_input(alert_description)