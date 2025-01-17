from django.db.utils import IntegrityError
from django.db import transaction
from django.core.exceptions import ValidationError

from decimal import InvalidOperation

from ComSemApp.models import *
from ComSemApp.libs.factories import BaseTestCase

class TestSpeakingPracticeAttempt(BaseTestCase):
    """
        Test class for the SpeakingPracticeAttempt database model
        Inherits from a custom BaseTestCase class with extra methods for easy database manipulation
    """
    def setUp(self) -> None:
        """
            Implementation of standard setUp function.
            Creates one instance of Expression for the SpeakingPracticeAttempts to reference
        """
        self.expression = self.db_create_expression()
    
    def test_exception_on_null_fields(self) -> None:
        """
            Tests that an exception is thrown when any Not Null field is undefined
        """
        with transaction.atomic():
            self.assertRaises(IntegrityError, SpeakingPracticeAttempt.objects.create)
        with transaction.atomic():
            self.assertRaises(IntegrityError, SpeakingPracticeAttempt.objects.create, expression=self.expression)
        with transaction.atomic():
            self.assertRaises(IntegrityError, SpeakingPracticeAttempt.objects.create, expression=self.expression, correct=90)
        with transaction.atomic():
            self.assertRaises(IntegrityError, SpeakingPracticeAttempt.objects.create, expression=self.expression, wpm=100)
        with transaction.atomic():
            self.assertRaises(IntegrityError, SpeakingPracticeAttempt.objects.create, correct=90)
        with transaction.atomic():
            self.assertRaises(IntegrityError, SpeakingPracticeAttempt.objects.create, correct=90, wpm=100)
        with transaction.atomic():
            self.assertRaises(IntegrityError, SpeakingPracticeAttempt.objects.create, wpm=100)

    def test_no_error_with_allowed_fields_null(self) -> None:
        """
            Tests that an exception is not thrown when fields which are allowed to be null are undefined
        """
        self.assertIsNotNone(SpeakingPracticeAttempt.objects.create(expression=self.expression, correct=90, wpm=100))

    def test_exception_on_out_of_range_values(self) -> None:
        """
            Tests that exceptions are thrown when validating values that are out of range
        """
        # wpm too high
        with transaction.atomic():
            self.assertRaises(InvalidOperation, SpeakingPracticeAttempt.objects.create, expression=self.expression, correct=90, wpm=1000)
        # wpm too low (negative)
        with transaction.atomic():
            self.assertRaises(ValidationError, SpeakingPracticeAttempt.objects.create(expression=self.expression, correct=90, wpm=-1).full_clean)
        # correct too high
        with transaction.atomic():
            self.assertRaises(ValidationError, SpeakingPracticeAttempt.objects.create(expression=self.expression, correct=500, wpm=100).full_clean)
        # correct too low (negative)
        with transaction.atomic():
            self.assertRaises(ValidationError, SpeakingPracticeAttempt.objects.create(expression=self.expression, correct=-1, wpm=100).full_clean)

    def test_multiple_attempts_on_same_expression_are_unique(self) -> None:
        """
            Tests that attempts for the same expression are created as separate objects
        """
        attempt1 : SpeakingPracticeAttempt = SpeakingPracticeAttempt.objects.create(expression=self.expression, correct=90, wpm=100)
        attempt2 : SpeakingPracticeAttempt = SpeakingPracticeAttempt.objects.create(expression=self.expression, correct=50, wpm=123)
        self.assertNotEqual(attempt1, attempt2)

    def test_values_read_from_object_equal_those_assigned(self) -> None:
        """
            Tests that the object created has values identical to those assigned
        """
        attempt : SpeakingPracticeAttempt = SpeakingPracticeAttempt.objects.create(expression=self.expression, correct=90, wpm=100)
        self.assertEqual(self.expression, attempt.expression)
        self.assertEqual(90, attempt.correct)
        self.assertEqual(100, attempt.wpm)