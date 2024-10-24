from django.urls import path
from chats.views import CreateUserView,UploadDocument, User_group, CreateGroup, GetGroupParticipants,RemoveUserFromGroup,AddParticipantInGroup, GetSingleUser, UpdatedGroupAdmin, UpdateGroupImage,UpdateUserImage,GetCurrentUser, DeleteGroup


urlpatterns =[
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('documentUpload/',UploadDocument.as_view(), name='documentUpload'),
    path('UserGroup/',User_group.as_view(), name='User_group'),
    path('CreateGroup/',CreateGroup.as_view(), name='CreateGroup'),
    path('GetGroupParticipants/<str:group_name>/',GetGroupParticipants.as_view(), name='GetGroupParticipants'),
    path('RemoveUserFromGroup/',RemoveUserFromGroup.as_view(), name='RemoveUserFromGroup'),
    path('AddParticipantInGroup/',AddParticipantInGroup.as_view(), name='addParticipantInGroup'),
    path('GetSingleUser/<str:username>',GetSingleUser.as_view(), name='GetSingleUser'),
    path('UpdatedGroupAdmin/',UpdatedGroupAdmin.as_view(), name='UpdatedGroupAdmin'),
    path('UpdateGroupImage/<str:group_name>',UpdateGroupImage.as_view(), name='UpdateGroupImage'),
    path('UpdateUserImage/<str:username>',UpdateUserImage.as_view(), name='UpdateGroupImage'),
    path('GetCurrentUser/',GetCurrentUser.as_view(), name='GetCurrentUser'),
    path('DeleteGroup/<group_name>',DeleteGroup.as_view(), name='DeleteGroup')
]