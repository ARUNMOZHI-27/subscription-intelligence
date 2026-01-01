class ConversationMemory:
    def __init__(self, max_turns: int = 10):
        self.history = []
        self.max_turns = max_turns

    def add(self, user_msg: str, assistant_msg: str):
        self.history.append({
            "user": user_msg,
            "assistant": assistant_msg
        })

        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def context(self,limit=6 )-> str:
        """
        Return short conversation context for LLM grounding
        """
        lines = []
        for h in self.history[-5:]:
            lines.append(f"User: {h['user']}")
            lines.append(f"Assistant: {h['assistant']}")
        return "\n".join(lines)
