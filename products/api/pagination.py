from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class for Bhavani Cashews API.
    Provides a default page size of 12, allowing clients to override
    via the 'page_size' query parameter up to a maximum of 100.
    """
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100
