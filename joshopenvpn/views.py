from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, FileResponse
from django.utils.encoding import smart_str
from subprocess import Popen, PIPE, STDOUT
import json,requests
import os



def create_vpn_file(user, password, email):
        
        command = ["bash","../generate_ovpn_client.sh", user, password, email]
        try:
                process = Popen(command, stdout=PIPE, stderr=STDOUT)
                output = process.stdout.read()
                exitstatus = process.poll()
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                filepath = '/home/ubuntu/client-configs/files/'+user+'.ovpn'
                if (exitstatus==0):
                        return {"status": "Success", "filepath":str(filepath)}
                else:
                        return {"status": "Failed", "output":str(output)}
        except Exception as e:
                return {"status": "failed", "output":str(e)}


def revoke_client(user):

        command = ["bash","../revoke_client_cert.sh", user]
        try:
                process = Popen(command, stdout=PIPE, stderr=STDOUT)
                output = process.stdout.read()
                exitstatus = process.poll()
                if (exitstatus==0):
                        return {"status": "Success", "output":str(output)}
                else:
                        return {"status": "Failed", "output":str(output)}
        except Exception as e:
                return {"status": "failed", "output":str(e)}



def download(file_path):
    try:
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.basename(file_path))
        response['Content-Length'] = os.path.getsize(file_path)
        return response
    except Exception as e:
        return error(e) 

@csrf_exempt
def create(request):

        if request.method == 'POST':
                request_data=json.loads(request.body.decode('utf-8'))
                
                user=request_data.get('user')
                password=request_data.get('password')
                email=request_data.get('email')

                data = create_vpn_file(user, password, email)
                

                #response = HttpResponse(content_type='application/force-download', status=200) # mimetype is replaced by content_type for django 1.7
                #response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.basename(data["filepath"]))
                #response['X-Sendfile'] = smart_str(data["filepath"])
                # It's usually a good idea to set the 'Content-Length' header too.
                # You can also set any other required headers: Cache-Control, etc.
                #return response

                #response = HttpResponse(json.dumps(data) , content_type='application/json', status=200)
                #response = HttpResponse(download(data["filepath"]), content_type='application/', status=200)
                #return response

                return download(data["filepath"]) if data['status'] == "Success" else HttpResponse(
                        json.dumps(data), content_type='application/json', status=200)

@csrf_exempt
def revoke(request):

        if request.method == 'POST':
                request_data=json.loads(request.body.decode('utf-8'))

                user=request_data.get('user')
                
                data = revoke_client(user)


                #response = HttpResponse(content_type='application/force-download', status=200) # mimetype is replaced by content_type for django 1.7
                #response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.basename(data["filepath"]))
                #response['X-Sendfile'] = smart_str(data["filepath"])
                # It's usually a good idea to set the 'Content-Length' header too.
                # You can also set any other required headers: Cache-Control, etc.
                #return response

                #response = HttpResponse(json.dumps(data) , content_type='application/json', status=200)
                response = HttpResponse(json.dumps(data), content_type='application/json', status=200)
                return response

