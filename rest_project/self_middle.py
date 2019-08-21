from django.utils.deprecation import MiddlewareMixin

class Testmiddle(MiddlewareMixin):
    def process_request(self,request,*args,**kwargs):
        print("process_request method")

    def process_response(self,request,response,*args,**kwargs):
        print("This is process_response method")
        return response

    # def process_view(self,request,response,view_func,view_args,view_kwargs):
    #     print("This is process_view method")
    #     return response

    def process_template_response(self,request,response):
        print("This is template_response method")
        return response

    def process_exception(self, request, exception):
        print("This is process_exception method")