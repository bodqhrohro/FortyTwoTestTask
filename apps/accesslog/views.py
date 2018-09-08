from django.shortcuts import render


def accesslog(request):
    timestamp = request.GET.get('from', None)

    if timestamp is None:
        new_requests_count = 0
    else:
        new_requests_count = int(request.GET.get('new', 10))

    visited_links = [
        '/',
        '/admin/',
    ]

    return render(request, 'accesslog/requests.html', {
        "visited_links": visited_links,
        "new_requests_count": new_requests_count,
    })
