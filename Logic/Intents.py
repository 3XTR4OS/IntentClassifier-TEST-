# Классификация интентов
from abc import ABC, abstractmethod

from transformers import AutoTokenizer, TextClassificationPipeline, AutoModelForSequenceClassification


# Классификация интентов
class IntentClassifier:
    def __init__(self):
        self.__model_name = 'qanastek/XLMRoberta-Alexa-Intents-Classification'
        self.__tokenizer = AutoTokenizer.from_pretrained(self.__model_name)
        self.__model = AutoModelForSequenceClassification.from_pretrained(self.__model_name)
        self.__classifier = TextClassificationPipeline(model=self.__model, tokenizer=self.__tokenizer)

    def classify(self, user_message):
        # response: [{'label': 'alarm_set', 'score': 0.9}]
        response = self.__classifier(user_message)

        classified_intents = []

        for elem in response:
            classified_intents.append('INTENT_' + elem['label'].upper())

        # -> [INTENT_ALARM_SET, ..., INTENT_NAME_N]
        return classified_intents


class IntentModules:
    def alarm_module(self, user_message: str, named_entities: list):
        # // Какая-то логика
        return 'Будильник успешно установлен!'

    def hotel_module(self, user_message: str, named_entities: list):
        # // Какая-то логика
        return 'Билеты забронированы!'

    def music_module(self, user_message: str, named_entities: list):
        # // Какая-то логика
        return 'Играет приятная музыка'


class IntentProcessor:
    def __init__(self, local_intents: list):
        self.intents_modules = {
            'INTENT_ALARM_SET': lambda user_message, entities: IntentModules().alarm_module(user_message, entities),
            'INTENT_MUSIC_LIKENESS': lambda user_message, entities: IntentModules().music_module(user_message,
                                                                                                 entities),
        }
        self.available_intents: list = local_intents

    # Проверка на предмет наличия данного интента в БД(Локальное хранилище)
    def __check_to_available_to_process(self, intent, available_intents) -> bool:
        print(intent in available_intents)
        return intent in available_intents

    def process_intents(self, user_message: str, entities: list, intents: list) -> list:
        unknown_text = 'Извините, неизвестное содержимое'
        error_text = 'Извините, мы не можем обработать ваш запрос'
        processed_intents = []

        for intent in intents:
            # Наличие INTENT_NAME в бд
            if not self.__check_to_available_to_process(intent=intent, available_intents=self.available_intents):
                processed_intents.append(unknown_text)
                continue

            # Наличие модуля по обработке INTENT_NAME
            have_a_process_module: bool = intent in self.intents_modules

            if not have_a_process_module:
                processed_intents.append(error_text)
            else:
                # Передача управления
                intent_module = self.intents_modules[intent]
                processed_intents.append(intent_module(user_message, entities))

        return processed_intents
