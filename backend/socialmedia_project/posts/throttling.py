from rest_framework.throttling import UserRateThrottle

class PostCreateThrottlle(UserRateThrottle):
    scope = 'post_create'