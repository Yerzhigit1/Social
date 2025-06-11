import factory 
from ..models import User, Profile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        
    email = factory.Sequence(lambda n: f'user{n}@gmail.com')
    full_name = factory.faker('word')
    password = factory.PostGenerationMethodCall('set_password', 'password.1234')
    

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        
    user = factory.SubFactory(UserFactory)
    bio = factory.faker('sentence')