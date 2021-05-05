class TranslationError(Exception):
    pass


class NaturalToLeanError(TranslationError):
    pass


class LeanToNaturalError(TranslationError):
    pass
