# Выделение именованных сущностей
from transformers import pipeline


class NamedEntityClassifier:
    def __init__(self):
        self.classifier = pipeline(
            task="token-classification",
            model="mdarhri00/named-entity-recognition")

    def classify(self, user_message):
        """Превращает response вида [{'entity': 'Person_Name', 'score': 0.7019974, 'index': 4, 'word': 'Wolfgang',
         'start': 11, 'end': 19}, {...}, {...}] в список [{'some_entity': 'some_word'}, ..., {}]"""
        response = self.classifier(user_message)

        named_entities = []
        for elem in response:
            entity, value = elem['entity'].upper(), elem['word'].upper()
            named_entities.append({entity: value})

        return named_entities
