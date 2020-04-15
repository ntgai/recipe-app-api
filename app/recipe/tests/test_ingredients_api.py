from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsAPITests(TestCase):
	"""Tests for publicly available ingredients API"""

	def setUp(self):
		"""Api client for public API"""
		self.client = APIClient()

	def test_login_required(self):
		"""Only authorized users can request to ingredients API"""
		res = self.client.get(INGREDIENTS_URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
	"""Tests for private ingredients API"""

	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			'test@ntg.ai',
			'testpassword'
		)
		self.client.force_authenticate(self.user)

	def test_retrieve_ingredient_list(self):
		"""Test retrieving a list of ingredients"""
		Ingredient.objects.create(user=self.user, name="Kartof")
		Ingredient.objects.create(user=self.user, name="Pamador")

		res = self.client.get(INGREDIENTS_URL)

		ingredients = Ingredient.objects.all().order_by('-name')
		serializer = IngredientSerializer(ingredients, many=True)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_ingredients_limited_to_user(self):
		"""Test that ingredients for the authenticated user are returned"""
		user2 = get_user_model().objects.create_user(
			'other@ntg.ai',
			'testpass'
		)

		Ingredient.objects.create(user=user2, name="Kartof")
		ingredient = Ingredient.objects.create(user=self.user, name="Pamador")

		res = self.client.get(INGREDIENTS_URL)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		self.assertEqual(res.data[0]['name'], ingredient.name)

	def test_create_ingredient_successful(self):
		"""Test create a new ingredient"""
		payload = {'name': 'Cabbage'}
		self.client.post(INGREDIENTS_URL, payload)

		exists = Ingredient.objects.filter(
			user = self.user,
			name = payload['name']
		).exists()

		self.assertTrue(exists)

	def test_create_ingredient_invalid(self):
		"""Test creating invalid ingredient fails"""
		payload = {'name': ''}
		res = self.client.post(INGREDIENTS_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

