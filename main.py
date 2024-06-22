import json
import pprint

import Logic.Intents as Intents
import Logic.Named_Entities as Named_entitiesCLF
import Logic.DataBase.PostgreSQL as PgDataBase
import Logic.Modules as Modules
import DataTransformer as DTransform
from Trainee.Logic.Intents import IntentProcessor


class JsonWorker:
    def read_json(self, file_path) -> dict:
        with open(file_path, 'r', encoding='UTF-8') as file:
            data = json.load(file)

        return data



class OutputConstructor:
    def __init__(self,
                 message_id: str,
                 user_message: str,
                 extracted_entities: list,
                 classified_intents: list,
                 answer):
        self.message_id = message_id
        self.message = user_message
        self.extracted_entities = extracted_entities
        self.classified_intents = classified_intents
        self.answer = answer

    def get_json_output(self):
        output_json = {
            "message_id": self.message_id,
            "message": self.message,
            "extracted_entities": self.extracted_entities,
            "intents": self.classified_intents,
            "answer": self.answer}

        return output_json

    def save_into_json_file(self, path, filename):
        received_json = self.get_json_output()

        with open(f'{path}//{filename}', 'w', encoding='utf-8') as file:
            json.dump(received_json, file, ensure_ascii=False, indent=2)


def main():
    worker = JsonWorker()
    intent_clf = Intents.IntentClassifier()
    named_entity_clf = Named_entitiesCLF.NamedEntityClassifier()
    data_transformer = DTransform.DataTransformer()  # Приводит данные к некоторому формату
    postgres = PgDataBase.PostgresDB()

    # Структура jdata: {message_id: str, message: str}
    jdata: dict = worker.read_json('Files/Input/Example_json1.json')

    # Определение интентов и именованных сущностей
    determine_intents: list = intent_clf.classify(jdata['message'])
    determine_named_entities: list = named_entity_clf.classify(jdata['message'])

    # Сохранение в память приложения
    local_intents = Modules.LocalStorage()
    local_intents.save(postgres.select_data(table_name='Intents'))
    local_intents.save(data_transformer.add_prefix(prefix='INTENT_', data=local_intents.get_data()))

    # Передаём выгруженные данные из БД данные
    intent_proc = IntentProcessor(local_intents.get_data())

    processed_answer = intent_proc.process_intents(user_message=jdata['message'], entities=determine_named_entities,
                                                   intents=determine_intents)

    output = OutputConstructor(
        message_id=jdata['messageId'],
        user_message=jdata['message'],
        extracted_entities=determine_named_entities,
        classified_intents=determine_intents,
        answer=processed_answer)

    pprint.pprint(output.get_json_output())
    output.save_into_json_file(path='Files/output', filename='main_test.json')


if __name__ == '__main__':
    main()
