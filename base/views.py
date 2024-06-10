from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = "base/home.html"
    
home_view = HomeView.as_view()
