from chats.models import Conversation
from rest_framework import serializers
from cryptography.fernet import Fernet
from rest_framework.response import Response
from chats.models import Message, Media, Participants, Group_content, Groups, User_Image
from django.contrib.auth.models import User
from datetime import date



class UserSerializer(serializers.ModelSerializer):
    user_picture = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["username", "user_picture"]
    def get_user_picture(self, instance):
        try:
            user_image = instance.user_image
            return str(user_image.image)
        except:
            return ''



class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Image
        fields = ['image']
    def to_representation(self, instance):
        image =  instance.image        
        return image





class UploadDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["file"]
       



class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()
    decode_key = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ("__all__")

    def get_decode_key(self, obj):
        try:            
            binary_data = Message.objects.get(id=obj.id)
        except Message.DoesNotExist:
            return Response(status=404)
        serializer = BinaryDataSerializer(binary_data)
        return serializer.data['decode_key']
    
    def get_content(self, obj):
        key = obj.decode_key
        cipher = Fernet(key)
        decrypted_text = cipher.decrypt(obj.content).decode()
        return decrypted_text

    def get_conversation(self, obj):
        return str(obj.conversation.id)

    def get_from_user(self, obj):
        return UserSerializer(obj.from_user).data

    def get_to_user(self, obj):
        return UserSerializer(obj.to_user).data



class BinaryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['decode_key']


class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("id", "name", "other_user", "last_message")

    def get_last_message(self, obj):
        messages = obj.messages.all().order_by("-timestamp")
        if not messages.exists():
            return None
        message = messages[0]
        return MessageSerializer(message).data

    def get_other_user(self, obj):
        usernames = obj.name.split("__")
        context = {}
        for username in usernames:
            if username != self.context["user"].username:
                # This is the other participant
                other_user = User.objects.get(username=username)
                return UserSerializer(other_user, context=context).data


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']  

    def create(self, validated_data):
        user_picture_data = validated_data.pop('user_picture', None)

        user = User.objects.create(**validated_data)

        if user_picture_data:
            User_Image.objects.create(user=user, image=user_picture_data)

        return user


class ParticipantSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    group_admin = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    class Meta:
        model = Participants
        fields = ['group', 'user', 'username', 'group_name', "group_admin" ,'user_image']

    def get_username(self, instance):
        user_instance = instance.user
        username = user_instance.username
        return username
    
    def get_group_name(self, instance):
        group_instance = instance.group
        group_name = group_instance.name 
        return group_name
    
    def get_group_admin(self, instance):
        groupName = self.get_group_name(instance)
        admin = Groups.objects.filter(name = groupName).values('Admin_id__username').first()
        return admin['Admin_id__username']
    

    def get_user_image(self, instance):
        userId = instance.user.id
        image = User_Image.objects.get(user = userId)
        return (str(image.image))
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation





class Group_content_serializer(serializers.ModelSerializer):
    from_user_id = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    class Meta:
        model = Group_content
        fields = ["group_id", "content", 'from_user_id', "timestamp", "file"]
    
    def get_from_user_id(self, obj):
        user_id = obj['from_user_id']
        user = User.objects.get(id=user_id)
        username = user.username
        return username
    
    def get_file(self, obj):
        return obj['file']
    
    
class Groups_serializers(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['name', 'Created_by', 'Created_on', 'Admin', "image"]
        



    


