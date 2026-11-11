import re


class QueryRouter:

    CHAT_PATTERNS = [

        r"^hi$",
        r"^hello$",
        r"^hey$",
        r"^thanks$",
        r"^thank you$",
        r"^good morning$",
        r"^good evening$",
        r"^how are you$",
        r"^who are you$",
        r"^help$",
        r"^what can you do\??$"
    ]

    @staticmethod
    def classify(query):

        message = query.strip().lower()

        # -----------------------
        # Cheap deterministic check
        # -----------------------

        for pattern in QueryRouter.CHAT_PATTERNS:

            if re.match(
                pattern,
                message
            ):
                return "CHAT"

        # -----------------------
        # Search-like indicators
        # -----------------------

        search_keywords = [

            "error",
            "issue",
            "problem",
            "dashboard",
            "billing",
            "invoice",
            "charge",
            "login",
            "authentication",
            "password",
            "api",
            "export",
            "report",
            "customer",
            "ticket",
            "latency",
            "timeout",
            "integration",
            "failed",
            "failure"
        ]

        for keyword in search_keywords:

            if keyword in message:

                return "SEARCH"

        # -----------------------
        # Default
        # -----------------------

        return "CHAT"