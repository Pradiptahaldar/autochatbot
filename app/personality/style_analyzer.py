import re
class StyleAnalyzer:
    def analyze_messages(self, messages):
        if not messages:
            return {
                "average_message_length": 0.0,
                "emoji_frequency": 0.0,
                "punctuation_frequency": 0.0,
                "response_length": "short",
                "common_words": []
            }
        total_length = sum(
            len(message)
            for message in messages
        )
        average_length = total_length / len(messages)
        response_length = self.classify_response_length(
            average_length
        )
        emoji_count = sum(
            self._count_emojis(message)
            for message in messages
        )
        emoji_frequency = emoji_count / len(messages)
        punctuation_count = sum(
            self._count_punctuation(message)
            for message in messages
        )
        punctuation_frequency = punctuation_count / len(messages)
        word_counts = self.find_common_words(messages)
        common_words = self.get_common_words(
            word_counts
        )
        return {
            "average_message_length": average_length,
            "emoji_frequency": emoji_frequency,
            "punctuation_frequency": punctuation_frequency,
            "response_length": response_length,
            "common_words": common_words
            }
    def _count_emojis(self, message):
        return sum(
            1
            for character in message
            if ord(character) > 127
        )
    def _count_punctuation(self, message):
        return sum(
            1
            for character in message
            if character in "!?.,"
        )
    def classify_response_length(self, average_length):
        if average_length < 30:
            return "short"
        if average_length <= 80:
            return "medium"
        return "long"
    def find_common_words(self, messages):
        word_counts = {}
        for message in messages:
            words = re.findall(
                r"\b[a-zA-Z]+\b",
                message.lower()
            )
            for word in words:
                word_counts[word] = (
                    word_counts.get(word, 0) + 1
                )
        return word_counts
    def get_common_words(
        self,
        word_counts,
        limit=10
    ):
        sorted_words = sorted(
            word_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )
        return [
            word
            for word, count in sorted_words[:limit]
        ]