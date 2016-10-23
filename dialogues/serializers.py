from rest_framework import serializers
from dialogues.models import Dialogue 


class DialogueSerializer(serializers.ModelSerializer):
	class Meta:
		model = Dialogue 
