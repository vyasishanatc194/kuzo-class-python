
from .user import (
    IndexView,
    UserAjaxPagination,
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserPasswordView,
    UserUpdateView,
 
)


from .testmail import send_test_mail

from .subscription_plan import (
    SubscriptionPlanListView,
    SubscriptionPlanCreateView,
    SubscriptionPlanUpdateView,
    SubscriptionPlanDeleteView,
    SubscriptionPlanAjaxPagination,
)

from .offer import (
    OfferListView,
    OfferCreateView,
    OfferUpdateView,
    OfferDeleteView,
    OfferAjaxPagination,
)

from .banner import (
    BannerListView,
    BannerCreateView,
    BannerUpdateView,
    BannerDeleteView,
    BannerAjaxPagination,
)


