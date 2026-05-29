from django.http import HttpResponse
from django.db import connection

def health_check(request):
    try:
        # Perform a minimal query to verify database status
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
            if row is None:
                raise Exception("Database returned no results")
    except Exception as e:
        return HttpResponse(f"Unhealthy: {str(e)}", status=500, content_type="text/plain")
    
    return HttpResponse("OK", status=200, content_type="text/plain")
