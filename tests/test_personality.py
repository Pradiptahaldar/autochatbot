from app.personality.global_profile import GlobalProfile
from app.personality.person_profile import PersonProfile
from app.personality.style_analyzer import StyleAnalyzer
def test_global_profile():
    profile = GlobalProfile(
        tone="casual",
        formality="low",
        response_length="short",
        emoji_usage="occasional",
        punctuation_style="informal",
        common_phrases=["bro", "yeah", "okay"]
        )
    assert profile.tone == "casual"
    assert profile.formality == "low"
    assert profile.response_length == "short"
    assert profile.emoji_usage == "occasional"
    assert profile.punctuation_style == "informal"
    assert "bro" in profile.common_phrases
def test_person_profile():
    profile = PersonProfile(
        person_id="person_001",
        tone="casual",
        formality="low",
        response_length="short",
        emoji_usage="occasional",
        common_phrases=["bro", "yeah"],
        relationship="college_friend"
    )
    assert profile.person_id == "person_001"
    assert profile.tone == "casual"
    assert profile.formality == "low"
    assert profile.response_length == "short"
    assert profile.emoji_usage == "occasional"
    assert "bro" in profile.common_phrases
    assert profile.relationship == "college_friend"
def test_style_analyzer():
    analyzer = StyleAnalyzer()
    messages = [
        "hi",
        "how are you",
        "I am good"
    ]
    result = analyzer.analyze_messages(messages)
    assert isinstance(result, dict)
    assert result["average_message_length"]== 22/3
    assert result["response_length"] == "short"
    assert "hi" in result["common_words"]
def test_style_analyzer_empty_messages():
    analyzer = StyleAnalyzer()
    result = analyzer.analyze_messages([])
    assert result["average_message_length"] == 0.0
    assert result["response_length"] == "short"
    assert result["common_words"]==[]
def test_style_analyzer_emoji_frequency():
    analyzer = StyleAnalyzer()
    messages = [
        "hello",
        "hello 😊",
        "great 😂"
    ]
    result = analyzer.analyze_messages(messages)
    assert result["emoji_frequency"] == 2 / 3
def test_style_analyzer_punctuation_frequency():
    analyzer = StyleAnalyzer()
    messages = [
        "hello!",
        "how are you?",
        "I am fine"
    ]
    result = analyzer.analyze_messages(messages)
    assert result["punctuation_frequency"] == 2 / 3
def test_classify_response_length():
    analyzer = StyleAnalyzer()
    assert analyzer.classify_response_length(10) == "short"
    assert analyzer.classify_response_length(50) == "medium"
    assert analyzer.classify_response_length(100) == "long"
def test_find_common_words():
    analyzer = StyleAnalyzer()
    messages = [
        "hello bro",
        "bro how are you",
        "hello bro"
    ]
    result = analyzer.find_common_words(messages)
    assert result["bro"] == 3
    assert result["hello"] == 2
    assert result["how"] == 1
    assert result["are"] == 1
    assert result["you"] == 1
def test_find_common_words_ignores_punctuation():
    analyzer = StyleAnalyzer()
    messages = [
        "hello!",
        "hello.",
        "hello?"
    ]
    result = analyzer.find_common_words(messages)
    assert result["hello"] == 3
def test_get_common_words():
    analyzer = StyleAnalyzer()
    word_counts = {
        "hello": 5,
        "bro": 10,
        "yeah": 7,
        "okay": 3
    }
    result = analyzer.get_common_words(
        word_counts,
        limit=2
    )
    assert result == ["bro", "yeah"]