from sentence_transformers import SentenceTransformer


class Embeddings:

    def __init__(self, model = "intfloat/multilingual-e5-large-instruct"):

        self.model = SentenceTransformer('intfloat/multilingual-e5-large-instruct')

    def generateEmbeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generates embeddings for a list of texts and returns them as a list of numerical vectors.

        Args:
            texts (list[str]): List of input texts to be converted into embeddings.

        Returns:
            list[list[float]]: List of embeddings, where each embedding is a list of float values.
        """

        if not texts:
            raise ValueError("La lista de textos no puede estar vacía")
        
        if not hasattr(self, "model") or self.model is None:
            raise RuntimeError("El modelo de embeddings no está inicializado")

        embeddings = self.model.encode(
            texts,
            convert_to_tensor=True,  
            normalize_embeddings=True 
        )

        
        return embeddings.cpu().numpy().tolist()  