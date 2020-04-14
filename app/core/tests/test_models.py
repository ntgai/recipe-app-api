from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user():
	"""Create a sample user"""
	return get_user_model().objects.create_user("test@ntg.ai", 'passwordntgai')

class ModelTests(TestCase):

	def test_create_user_with_email_successful(self):
		""" Test creating a new user with email is successful """
		email = 'test@ntg.ai'
		password = 'passntgai'
		user = get_user_model().objects.create_user(
			email=email,
			password=password
		)

		self.assertEqual(user.email, email)
		self.assertTrue(user.check_password(password))

	def test_new_user_email_normalized(self):
		"""Test email if it is normalized"""
		email = 'test@NTG.ai'
		user = get_user_model().objects.create_user(email, 'passntgai')

		self.assertEqual(user.email, email.lower())

	def test_new_user_invalid_email(self):
		"""Test creating user with invalid or empty email"""
		with self.assertRaises(ValueError):
			get_user_model().objects.create_user(None, 'test123')

	def test_create_new_superuser(self):
		"""Test creating superuser"""
		user = get_user_model().objects.create_superuser(
			'test@ntg.ai',
			'passntgai'
		)

		self.assertTrue(user.is_staff)
		self.assertTrue(user.is_superuser)

	def test_tag_str(self):
		"""Test the tag string representation"""
		tag = models.Tag.objects.create(
			user = sample_user(),
			name = 'Vegan'
		)

		self.assertEqual(str(tag), tag.name)

	def test_ingredient_str(self):
		ingredient = models.Ingredient.objects.create(
			user = sample_user(),
			name = 'Cucumber'
		)

		self.assertEqual(str(ingredient), ingredient.name)




