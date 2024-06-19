import json
import pprint
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline, pipeline


# Входные данные (json)
def read_json(json_path):
    with open(json_path, 'r', encoding='UTF-8') as file:
        json_string = json.load(file)

        return json_string


# Классификация интентов
def intent_classificator(user_message):
    model_name = 'qanastek/XLMRoberta-Alexa-Intents-Classification'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    classifier = TextClassificationPipeline(model=model, tokenizer=tokenizer)

    # response example: [{'label': 'alarm_set', 'score': 0.9998685121536255}]
    response = classifier(user_message)

    intent_classes = []
    for elem in response:
        intent_classes.append('INTENT_' + elem['label'].upper())

    return intent_classes


# Выделение именованных сущностей
def named_entity_classification(user_message):
    # output example: [{'entity': 'Person_Name', 'score': 0.7019974, 'index': 4, 'word': 'Wolfgang', 'start': 11, 'end': 19},
    # {'entity': 'location', 'score': 0.6971302, 'index': 9, 'word': 'Berlin', 'start': 34, 'end': 40}]
    classifier = pipeline(task="token-classification",
                          model="mdarhri00/named-entity-recognition")

    response = classifier(user_message)

    named_entities = []
    for elem in response:
        entity = elem['entity'].upper()
        value = elem['word'].upper()
        named_entities.append({entity: value})

    return named_entities


# --------------- МОДУЛИ -------------------------
def alarm_module():
    # // Какая-то логика
    return 'Будильник успешно установлен!'


def hotel_module():
    # // Какая-то логика
    return 'Билеты забронированы!'


def music_module():
    # // Какая-то логика
    return 'Играет приятная музыка'


# ------------------------------------------------

# ОБРАБОТЧИК ИНТЕНТОВ
def process_intent(intents: list):
    intents_modules = {
        'INTENT_ALARM_SET': alarm_module,
        'INTENT_BOOK_HOTEL': hotel_module,
        'INTENT_PLAY_MUSIC': music_module
    }

    processed_intents = []

    for intent in intents:
        can_work_with_intent = intent in intents_modules

        if not can_work_with_intent:
            processed_intents.append('Извините, мы не можем обработать ваш запрос')
        else:
            # Вызов функции
            intent_module = intents_modules[intent]
            processed_intents.append(intent_module())

    return processed_intents


if __name__ == '__main__':
    for i in range(1, 5):
        data = read_json(f'Files/Example_json{i}.json')
        classified_intents = intent_classificator(data['message'])
        entities = named_entity_classification(data['message'])
        answer = process_intent(classified_intents)

        output_json = {
            "message_id": data['messageId'],
            "message": data['message'],
            "extracted_entities": entities,
            "intents": classified_intents,
            "answer": answer
        }

        with open(f'output{i}.json', 'w', encoding='utf-8') as file:
            json.dump(output_json, file, ensure_ascii=False, indent=2)

        pprint.pprint(output_json)
