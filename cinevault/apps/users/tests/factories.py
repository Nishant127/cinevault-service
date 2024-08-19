import factory
from django.contrib.auth import get_user_model

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
    
    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword123')

    @factory.post_generation
    def create_user(self, create, extracted, **kwargs):
        if create:
            self.save()
