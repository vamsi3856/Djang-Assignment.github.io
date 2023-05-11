from django.shortcuts import get_object_or_404,render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import student
from .serializers import studentSerializer
from rest_framework import serializers
from rest_framework import status
from myapp.forms import StudentForm

@api_view(['GET'])
def ApiOverview(request):
	api_urls = {
		# 'all_students': '/',
		# 'Search by name': '/?name=student_name',
		# 'Search by department': '/?department=department_name',
		'Add': '/create',
		'Update': '/update/pk',
		'Delete': '/student/pk/delete'
	}

	return Response(api_urls)

@api_view(['POST','GET'])
def add_items(request):
    if request.method == 'POST':
        data=request.data.copy()
        data.pop('csrfmiddlewaretoken', None)
        item = studentSerializer(data=data)

        # validating for already existing data
        if student.objects.filter(**data).exists(): # use the modified `data` dictionary here
            raise serializers.ValidationError('This data already exists')
        
        if item.is_valid():
            item.save()
            return redirect('view_items')
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        form=StudentForm()
        return render(request,'createform.html',{'form':form,'st':'create'})



@api_view(['GET'])
def view_items(request):
    # checking for the parameters from the URL
    if request.query_params:
        items = student.objects.filter(**request.query_params.dict())
    else:
        items = student.objects.all()
        print(items)
    # if there is something in items else raise error
    if items:
        serializer = studentSerializer(items, many=True)
        # print(serializer)
        data=serializer.data
        return render(request,'students.html',{'data':data})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST','GET'])
def update_items(request, pk):
    if request.method=='POST':
        item = student.objects.get(pk=pk)
        data = studentSerializer(instance=item, data=request.data)
    
        if data.is_valid():
            data.save()
            return redirect('view_items')
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        item = student.objects.get(pk=pk)
        print(item)
        form=StudentForm(instance=item)
        return render(request,'createform.html',{'form':form,'st':'update'})
    
@api_view(['DELETE','GET',"POST"])
def delete_items(request, pk):
    if request.method=='POST':
        item = get_object_or_404(student, id=pk)
        item.delete()
        return redirect('view_items')
    else:
        item = student.objects.get(id=pk)
        serializer = studentSerializer(item)
        item=serializer.data
        return render(request,'delete-template.html',{'data':item})

@api_view(['GET'])
def profile(request,pk):
    item = student.objects.get(id=pk)
    serializer = studentSerializer(item)
    item=serializer.data
    print("---------------------------------------    ---------------------------------")
    print(item,serializer,item)
    return render(request,"student_detailed_view.html",{'data':item})