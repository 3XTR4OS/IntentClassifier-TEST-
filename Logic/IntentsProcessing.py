class Intent:
    def process(self, user_message: str, extracted_entities: list):
        pass


class IntentAlarmSet(Intent):
    def process(self, user_message: str, extracted_entities: list):
        # Некая логика
        return 'Будильник успешно поставлен'


class IntentMusicLikeness(Intent):
    def process(self, user_message: str, extracted_entities: list):
        # Некая логика
        return 'Играет приятная музыка'


class IntentProcessor:
    def __init__(self):
        self.intents = {
            'INTENT_ALARM_SET': IntentAlarmSet(),
            'INTENT_MUSIC_LIKENESS': IntentMusicLikeness()
        }

    def process_intent(self, user_message: str, extracted_entities: list):
        for intent, intent_processor in self.intents.items():
            if intent_processor.process(user_message, extracted_entities):
                return intent_processor.process(user_message, extracted_entities)
        return "Извините, мы не можем обработать ваш запрос"


def main():
    intent_processor = IntentProcessor()
    user_message = "Set alarm for 8:00 AM"
    extracted_entities = ['INTENT_ALARM_SET', 'INTENT_MUSIC_LIKENESS']
    for i in extracted_entities:
        response = intent_processor.process_intent(user_message, i)
        print(response)


if __name__ == "__main__":
    main()
