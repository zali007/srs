from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
# from django.utils import timezone
from .models import Student
# from .forms import MessageForm, SearchForm, StudentForm
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Count, Sum, Q, Case, Value, When, IntegerField

# Create your views here.

def home(request):
	return render(request,'base.html')

def home_json(request):
    return render(request, 'student/home_json.html')


# Student JSON list filtering
class student_list_json(BaseDatatableView):
    order_columns = ['icnum','name','course', 'pk','link']

    def get_initial_queryset(self):
        # icnum = self.request.GET.get(u'icnum', '')
        # return Student.objects.filter(icnum=icnum)
        return Student.objects.all().order_by('icnum')

    def filter_queryset(self, qs):

        # Getting advanced filtering indicators for dataTables 1.10.13
        search = self.request.GET.get(u'search[value]', "")
        iSortCol_0 = self.request.GET.get(u'order[0][column]', "") # Column number 0,1,2,3,4
        sSortDir_0 = self.request.GET.get(u'order[0][dir]', "") # asc, desc
        
        # Choose which column to sort
        if iSortCol_0 == '1':
          sortcol = 'name'
        elif iSortCol_0 == '2':
          sortcol = 'course'
        else:
          sortcol = 'icnum'


        # Choose which sorting direction : asc or desc
        if sSortDir_0 == 'asc':
          sortdir = ''
        else:
          sortdir = '-'

        # Filtering if search value is key-in
        if search:
          # Initial Q parameter value
          qs_params = None

          # Filtering Course category
          course_list = dict(Student.COURSE_CHOICES)
          # print access_list
          course_search = ''
          for key in course_list:
            # print key, access_list[key]
            if search in course_list[key]:
              course_search = str(key)
              q = Q(course__icontains=course_search)
              qs_params = qs_params | q if qs_params else q

          # Filtering other fields
          q = Q(name__icontains=search)|Q(icnum__icontains=search)
          qs_params = qs_params | q if qs_params else q
   
          # Completed Q queryset
          # print qs_params
          qs = qs.filter(qs_params)
          # print 'qs :' + str(qs)
          # print 'qs :'

        # print 'sortdir + sortcol : ' + sortdir + sortcol
        return qs.order_by(sortdir + sortcol)
        # return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        # json_data = {}
        json_data = []

        for item in qs:
            json_data.append([
                item.icnum,
                item.name,
                # item.course,
                item.get_course_display(),
                str(item.pk),
                # reverse_lazy('student_detail',kwargs={'pk': str(item.pk)})
                reverse_lazy('student_home'),
            ])
            # print(json_data)
        return json_data
