
import time


def calculate_request_time(get_response):
    def middleware(request):
        start_time = time.time()
        response = get_response(request)
        end_time = time.time()
        print(f"{round(end_time-start_time, 3)} секунд")
        return response
    return middleware
