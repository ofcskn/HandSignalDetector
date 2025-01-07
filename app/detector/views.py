from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from .forms import PhotoUploadForm
from .camera.streaming import gen
from .camera.video_camera import VideoCamera
from .models import Photo

def index(request):
    """Default view for the app."""
    return render(request, 'detector/index.html')

def emotion_detector(request):
    return StreamingHttpResponse(gen(VideoCamera(), 1), content_type='multipart/x-mixed-replace; boundary=frame')

def hand_gesture_detector(request):
    return StreamingHttpResponse(gen(VideoCamera(), 2), content_type='multipart/x-mixed-replace; boundary=frame')

def upload_photo(request):
    """Uplaod photos to the folder."""
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = PhotoUploadForm()
    uploaded_photos = Photo.objects.all() 
    return render(request, 'detector/upload_photo.html', {'form': form, "uploaded_photos": uploaded_photos})

def upload_success(request):
    return HttpResponse('Photo uploaded successfully!')