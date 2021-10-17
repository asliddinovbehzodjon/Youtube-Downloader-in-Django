from django.shortcuts import render,redirect
from pytube import YouTube
from django.http import FileResponse
from io import BytesIO
# Create your views here.
def home(request):
    if request.method == "POST":
        request.session['link'] = request.POST['url']
        try:
            url = YouTube(request.session['link'])
            url.check_availability()
            
            streams=url.streams.filter(progressive=True)
        except:
            return render(request,"error.html")
        return render(request,"download.html",{'streams':streams,'url':url})
    return render(request,"main.html")
def download(request):
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(request.session['link'])
        itag = request.POST["itag"]
        if itag=='audio':
            audio=url.streams.get_audio_only()
            audio.stream_to_buffer(buffer)
            buffer.seek(0)
            filename=url.title+'.mp3'
            return FileResponse(buffer,filename=filename, as_attachment=True,content_type="audio/mp3")
        else:

          video = url.streams.get_by_itag(itag)
          video.stream_to_buffer(buffer)
          buffer.seek(0)
          filename=url.title+".mp4"
          return FileResponse(buffer,filename=filename, as_attachment=True,content_type="video/mp4")
    return redirect("/home")

