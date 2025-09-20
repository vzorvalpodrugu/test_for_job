#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Test.settings")
    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    # Запускаем все тесты из папки tests
    failures = test_runner.run_tests(["tests"])

    sys.exit(bool(failures))