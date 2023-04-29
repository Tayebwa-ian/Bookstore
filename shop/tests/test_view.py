from ..views import *
from rest_framework.test import APITestCase, APIClient
from model_bakery import baker
import json
from rest_framework import status
from django.urls import reverse
from ..serializers import CategoriesSerializer

client=APIClient()

"""
 -Must turn off the global pagination settings in bookshop.settings.py
  before you run these tests
 -Only then can these tests pass
"""

class TestCategories(APITestCase):
    def setUp(self) -> None:
        # creating the different users
        self.customer=User.objects.create(username="ruth", email="ruth@gmail.com", 
                             password="ruth@123", telephone=785857000)
        self.seller=User.objects.create(username="dan", email="dan@gmail.com", is_seller=True, 
                           password="dan@123", telephone=782569168)
        self.admin=User.objects.create(username="mark", email="mark@gmail.com", is_staff=True, 
                 password="mark@123", telephone=777859168)
        
        self.cat1=baker.make('Categories')
        self.cat2=baker.make('Categories')
        self.cat3=baker.make('Categories')
        self.payloads=[
        {
            "name": "Technology",
            "description": "books concerning tech things"
        },

        {
            "name": "Environment",
            "description": "books environmental conservation"
        },

        {
            "name": "Physics",
            "description": "Study physics with books in this section"
        }
        ]
    
    def test_list(self):
        """
        testing if all categories can be retrieved
    
        """
        client.force_authenticate(user=self.customer)
        response=client.get(reverse('categories-list'))
        categories=Categories.objects.all()
        cat=Categories.objects.filter(name=self.cat1.name).first()
        cat6={"count": 5}
        serializer=CategoriesSerializer(categories, many=True)
        print(cat)
        print(cat6)
        print(categories)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        """
        testing if asingle cat can be retrieved
    
        """
        client.force_authenticate(user=self.customer)
        response=client.get(reverse('categories-detail', kwargs={'pk': self.cat1.id}))
        category=Categories.objects.get(id=self.cat1.id)
        serializer=CategoriesSerializer(category)

        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        """
        testing if an admin user can create category
    
        """
        client.force_authenticate(user=self.admin)
        response=client.post(reverse('categories-list'), 
                             data=json.dumps(self.payloads[0]), 
                             content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

