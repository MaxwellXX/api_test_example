#coding:utf-8
import  requests
requests.packages.urllib3.disable_warnings()


class Request:
   def request(self,url,method,**kwargs):
      if method=='get':
         return requests.request(url=url,method=method,**kwargs)
      elif method=='post':
         return requests.request(url=url,method=method,**kwargs)
      elif method=='put':
         return requests.request(url=url,method=method,**kwargs)
      elif method=='delete':
         return requests.request(url=url,method=method,**kwargs)

   def get(self,url,**kwargs):
      return self.request(url=url,method='get', **kwargs)

   def post(self,url,**kwargs):
      return self.request(url=url,method='post', **kwargs)

   def put(self,url,**kwargs):
      return self.request(url=url,method='put',**kwargs)

   def delete(self,url,**kwargs):
      return self.request(url=url,method='delete',**kwargs)
