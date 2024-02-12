from rest_framework.test import APITestCase
from mixer.backend.django import Mixer, GenFactory
mixer = Mixer(factory=GenFactory)