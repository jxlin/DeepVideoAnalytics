from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import requests
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from django.utils.decorators import method_decorator
from .forms import UploadFileForm
from .models import Video,Frame,Detection


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'],form.cleaned_data['name'])
        else:
            raise ValueError
    else:
        form = UploadFileForm()
    context = { 'form' : form }
    context['video_count'] = Video.objects.count()
    context['frame_count'] = Frame.objects.count()
    context['detection_count'] = Detection.objects.count()
    return render(request, 'dashboard.html', context)


def handle_uploaded_file(f,name):
    video = Video()
    video.name = name
    video.save()
    with open('temp_data/{}.mp4'.format(video.pk), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    video.uploaded = True
    video.save()

class VideoList(ListView):
    model = Video


class VideoDetail(DetailView):
    model = Video

    def get_context_data(self, **kwargs):
        context = super(VideoDetail, self).get_context_data(**kwargs)
        context['frame_list'] = Frame.objects.all().filter(video=self.object)
        # url = boto_client.generate_presigned_url('get_object',Params={'Bucket': context['object'].bucket,'Key': context['object'].key},ExpiresIn=600)
        url = ""
        context['url'] = url
        return context


class FrameList(ListView):
    model = Frame


class FrameDetail(DetailView):
    model = Frame

    def get_context_data(self, **kwargs):
        context = super(FrameDetail, self).get_context_data(**kwargs)
        context['detection_list'] = Detection.objects.all().filter(frame=self.object)
        # url = boto_client.generate_presigned_url('get_object',Params={'Bucket': context['object'].video.bucket,'Key': context['object'].key},ExpiresIn=600)
        url = ""
        context['url'] = url
        return context
