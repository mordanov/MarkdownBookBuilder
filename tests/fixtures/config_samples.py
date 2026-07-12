"""Sample configuration data for testing."""

MINIMAL_VALID_TOML = """title = "Test Book"
author = "Test Author"
"""

FULL_VALID_TOML = """title = "Test Book"
author = "Test Author"
version = "1.0.0"
source_dir = "content"

[output]
format = "pdf"
path = "dist/output.pdf"

[openai]
api_key = "sk-test-key"
model = "gpt-4o"
"""

INVALID_TOML = """title = "Test Book"
author = "Test Author
[incomplete section
"""

MISSING_REQUIRED_TOML = """version = "1.0.0"
source_dir = "content"
"""

TOML_WITH_EXTRA_FIELDS = """title = "Test Book"
author = "Test Author"
extra_field = "ignored"
another_field = 123
"""

TOML_WITH_DEFAULTS = """title = "Simple Book"
author = "Simple Author"
"""

MINIMAL_VALID_CONFIG_DICT = {
    "title": "Test Book",
    "author": "Test Author",
}

FULL_VALID_CONFIG_DICT = {
    "title": "Test Book",
    "author": "Test Author",
    "version": "1.0.0",
    "source_dir": "content",
    "output": {
        "format": "pdf",
        "path": "dist/output.pdf",
    },
    "openai": {
        "api_key": "sk-test-key",
        "model": "gpt-4o",
    },
}

SAMPLE_ENV_OVERRIDES = {
    "BOOK_TITLE": "Override Title",
    "BOOK_OUTPUT__FORMAT": "html",
    "OPENAI_API_KEY": "sk-env-override",
}

ENV_OVERRIDES_NESTED = {
    "BOOK_TITLE": "From Env",
    "BOOK_OUTPUT__FORMAT": "epub",
    "BOOK_OUTPUT__PATH": "custom/output.epub",
    "OPENAI_API_KEY": "sk-from-env",
}
