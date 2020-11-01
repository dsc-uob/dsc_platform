from django.shortcuts import render


def coming_soon(request):
    """Return the coming soon page!"""
    return render(request, 'core/index.html')
