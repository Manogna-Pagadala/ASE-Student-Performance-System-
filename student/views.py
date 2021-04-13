from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.db import connection,transaction
from django.contrib.auth import login,logout
from django.core.mail import send_mail
from django.contrib import messages

from operator import itemgetter

import datetime


cursor=connection.cursor()
# Create your views here

# open SPS main page
def Main_page(request):
    return render(request,'student/Main_page.html')
    
def facultyhome(request):
	return render(request,'student/facultyhome.html')
	
def add_achievements(request):
	li=request.POST.get('li')
	lp=request.POST.get('lp')
	return render(request,'student/add_achievements.html',{'li':li,'lp':lp})
	
# open student home page
def student(request):
    return render(request,'student/student.html')
    
def test(request):
	return render(request,'student/test.html')
	
# open login page
def sign(request):
	return render(request,'student/sign.html')
def ser(request):
	return render(request,'student/ser.html')
def Acad(request):
	return render(request,'student/Acad.html')
	
# add achievements	
def mach(request):
	li=request.POST.get('li')
	lp=request.POST.get('lp')
	if request.POST.get('rollno') and request.POST.get('achievement'):
		achieve=Achievements()
		achieve.Student_Achievement= request.POST.get('achievement')
		achieve.Student_Id_id = request.POST.get('rollno')
		achieve.save()
		return render(request, 'student/add_achievements.html',{'li':li,'lp':lp})  
	else:
		return render(request, 'student/add_achievements.html',{'li':li,'lp':lp})  

#open marks upload,edit,add grade schema,add grade weightage page
def subject(request):
	if request.method == 'POST':
		w=request.POST.get('cid')
		li=request.POST.get('lid')
		
		lp=request.POST.get('lpwd')
		x=request.POST.get('xid')
		print("in subject",w,li,lp,x)
		cursor.execute("select Facultycourse_Id from student_faculty where Faculty_Id='%s' and Academic_Course_Id_id='%s'"%(li,w))
		fc=cursor.fetchall()
		print("fcid",fc)
		g=fc[0][0]
		cursor.execute("select Exam_Type from student_gradeweightage where Facultycourse_Id_id='%s'"%(g))
		fc1=cursor.fetchall()
		print("examtype",fc1)
		return render(request,'student/course.html',{'w':w,'li':li,'lp':lp,'x':x,'fc':fc[0][0],'fc1':fc1})
	return render(request,'student/student.html')
   


# validate login id,password
def login1(request):
	if request.method == 'POST':
		flag=0
		q=request.POST.get('pwd')
		p=request.POST.get('id')
		#q1='S'
		#q1+=p
		f=[]
		f1=[]
		f2=[]
		f3=[]
		b=[]
		objects=[]
		cursor.execute("select User_Id,Password from student_credentials")
		o=cursor.fetchall()
		for i in o:
			if i[0]==p and i[1]==q:
				objects.append(i)	
		#for i in objects:
		#	print(i.User_Id,i.Password)
		if len(objects)!=0 and p[0]=='2':
			cursor.execute("select Club_President,Club_Vicepresident from student_student where Student_Id='%s'"%(p))
			res=cursor.fetchall()
			if res[0][0] and res[0][1]:
				flag=1
			else:
				flag=0
			return render(request,'student/student.html',{'p':p,'lp':q,'flag':flag})
		elif len(objects)!=0 and p[0]=='F':
			cursor.execute("select Academic_Course_Id_id from student_faculty where Status='1' and Faculty_Id='%s'"%(p))
			g=cursor.fetchall()
			for i in g:
				f.append(list(i))
			cursor.execute("select Academic_Course_Id_id from student_faculty where Status='2' and Faculty_Id='%s'"%(p))
			for i in cursor.fetchall():
				f1.append(list(i))
				
			f2=[k for k in f if "-" in k[0]]
			f4=[k for k in f if "-" not in k[0]]
			f3=[k for k in f1 if "-" in k[0]]
			f5=[k for k in f1 if "-" not in k[0]]
			return render(request,'student/facultyhome.html',{'a':f4,'b':f5,'c':f2,'d':f3,'e':p,'f':q})
		elif len(objects)!=0 and p[0]=='A':
			cursor.execute("select distinct Academic_Course_Id_id from student_faculty where status='1'")
			h=cursor.fetchall()
			f=[]
			for i in h:
				if "-" not in i[0]:
					f.append(i)
			#return render(request,'student/facultyhome.html')
			return render(request,'student/adminhome.html',{'p':p,'q':q,'f':f})
		elif len(objects)==0:
			p="PLEASE ENTER A VALID USER ID/PASSWORD"
			return render(request, 'student/sign.html',{'t':p})
		#return render(request,'student/sign.html')
	#return render(request,'student/sign.html')
def clubach(request):
	return render(request,'student/clubach.html')
	
# add club achievements	
def add_ach(request):
	p=request.POST.get('id')
	lp=request.POST.get('pwd')
	club=request.POST.get('club')
	ach=request.POST.get('ach')
	cursor.execute("insert into student_club(Club_name,session1,Student_Id_id) values('%s','%s','%s')"%(club,ach,p))
	return render(request,'student/clubach.html',{'p':p,'lp':lp})

# signup inserting 	
def insac(request):
	if request.method=='GET':
		fn=request.GET.get('fn')	
		mn=request.GET.get('mn')
		ln=request.GET.get('ln')
		id1=request.GET.get('id')
		pwd=request.GET.get('pwd')
		em=request.GET.get('email')
		cpwd=request.GET.get('cpwd')
		gen=request.GET.get('gen')
		date=request.GET.get('date')
		
		ry=id1.split('00')[0]
		print(fn,mn,ln,id1,pwd,em,cpwd,gen,date,ry)
		cursor.execute("insert into student_credentials(User_Id,First_Name,Middle_Name,Last_Name,Password,Confirm_Password) values('%s','%s','%s','%s','%s','%s')"%(id1,fn,mn,ln,pwd,cpwd))
		if id1[0]=='2':
			cursor.execute("insert into student_student(Student_Id,Student_First_Name,Student_Middle_Name,Student_Last_Name,Student_DOB,Student_Gender,Student_Email,Student_Registered_Year) values('%s','%s','%s','%s','%s','%s','%s','%s')"%(id1,fn,mn,ln,date,gen,em,ry))
		return render(request, 'student/Main_page.html')


# insert/update gradeweightage	
def addgradeweightage(request):
	if request.method == 'POST':
		w = request.POST.get('cid')
		x = request.POST.get('xid')
		li=request.POST.get('lid')
		lp=request.POST.get('lpwd')
		now = datetime.datetime.now()
		y=str(now.year)
		a1=['01','02','03','04','05']
		b1=['08','09','10','11','12']
		if str(now.month) in a1:
			q='S_'+y
		elif str(now.month) in b1:
			q='M_'+y
		fcid = request.POST.get('fcid')
		D = (request.POST.get('D'))
		#print(sem,cid,fcid,type(D))
		
		cursor.execute("update student_gradeweightage set wmarks='%s' where Facultycourse_Id_id='%s' and semester='%s' and Exam_type='%s'"%(D,fcid,q,w))	
		
		cursor.execute("select Exam_Type from student_gradeweightage where Facultycourse_Id_id='%s'"%(fcid))
		fc1=cursor.fetchall()
		return render(request,'student/course.html',{'w':w,'li':li,'lp':lp,'x':x,'fc':fcid,'fc1':fc1})
		
# insert/update gradeschema
def addgradeschema(request):
	if request.method == 'POST':
		li=request.POST.get('lid')
		lp=request.POST.get('lpwd')
		fcid = request.POST.get('fcid')
		w = request.POST.get('cid')
		x = request.POST.get('xid')
		
		A = request.POST.get('A')
		a = request.POST.get('a')
		
		x1=str(A)+"-"+str(a)
		
		A2 = request.POST.get('A2')
		a2 = request.POST.get('a2')
		
		y=str(A2)+"-"+str(a2)
		
		B = request.POST.get('B')
		b = request.POST.get('b')
		
		z=str(B)+"-"+str(b)
		
		B2 = request.POST.get('B2')
		b2 = request.POST.get('b2')
		
		e=str(B2)+"-"+str(b2)
		
		C = request.POST.get('C')
		c = request.POST.get('c')
		
		f=str(C)+"-"+str(c)
		
		C2 = request.POST.get('C2')
		c2 = request.POST.get('c2')
		
		q=str(C2)+"-"+str(c2)
		
		D = request.POST.get('D')
		d = request.POST.get('d')
		
		r=str(D)+"-"+str(d)
		
		sem=request.POST.get('sem')
		
		cursor.execute("update student_gradeschema set A='%s',A2='%s',B='%s',B2='%s',C='%s',C2='%s',D='%s',Semester='%s',Facultycourse_Id_id='%s'"%(x1,y,z,e,f,q,r,sem,fcid))
		
		cursor.execute("select Exam_Type from student_gradeweightage where Facultycourse_Id_id='%s'"%(fcid))
		fc1=cursor.fetchall()
		print(x,w,li,lp,fc1,fcid)
		return render(request,'student/course.html',{'w':w,'li':li,'lp':lp,'x':x,'fc':fcid,'fc1':fc1})
def adminhome(request):
	return render(request,'student/adminhome.html')
def test(request):
	return render(request,'student/test.html')

# add student achievements usecase	
"""def add_achievements(request):
	if request.method == 'POST':
		if request.POST.get('rollno') and request.POST.get('achievement'):
			achieve=Achievements()
			achieve.Student_Achievement= request.POST.get('achievement')
			achieve.Student_Id_id = request.POST.get('rollno')
			achieve.save()
			return render(request, 'student/add_achievements.html')  
		else:
			return render(request, 'student/add_achievements.html')  """
def edit(request):
	return render(request,'student/edit.html')
def viewatten(request):
	return render(request,'student/viewatten.html')

def f1(request):
	return render(request,'student/f1.html')
"""def dim(request):
	if request.method == 'POST':
		if request.POST.get('id'):
			r = request.POST.get('id')
			cursor.execute("select student_image from student_student where Student_Id='%s'"%(r))
			p=cursor.fetchall()
			q=[]
			for i in p:
				q.append(list(i))
			return render(request,'student/test.html',{'q':q})"""

# update attendance
def attedit(request):
	if request.method=='POST':
		count=0
		d=request.POST.get('d')
		e=d.split('-')
		lt=request.POST.get('lt')
		a=[]
		b=[]
		a1=['01','02','03','04','05']
		b1=['08','09','10','11','12']
		for i in range(int(lt)):
			b.append(str(i))
		for i in range(int(lt)):
			if request.POST.get(b[i])==None:
				count=count+1		
		if(count==int(lt)):
			cursor.execute("select distinct Academic_Course_Id_id from student_faculty where status='1'")
			h=cursor.fetchall()
			f=[]
			for i in h:
				if "-" not in i[0]:
					f.append(i)
			return render(request,'student/adminhome.html',{'f':f})
		for i in range(int(lt)):
			a.append(request.POST.get(b[i]))
		#ns=request.POST.get('ns')
		
		if e[1]==a1[0] or e[1]==b1[0]:
			for i in a:
				if i!=None:
					cursor.execute("update student_attendance set M1_"+e[2]+" = 'P' where student_Id_id='%s'"%(i))
		elif e[1]==a1[1] or e[1]==b1[1]:
			for i in a:
				if i!=None:
					cursor.execute("update student_attendance set M2_"+e[2]+" = 'P' where student_Id_id='%s'"%(i))
		elif e[1]==a1[2] or e[1]==b1[2]:
			for i in a:
				if i!=None:
					cursor.execute("update student_attendance set M3_"+e[2]+" = 'P' where student_Id_id='%s'"%(i))
		elif e[1]==a1[3] or e[1]==b1[3]:
			for i in a:
				if i!=None:
					cursor.execute("update student_attendance set M4_"+e[2]+" = 'P' where student_Id_id='%s'"%(i))
		elif e[1]==a1[4] or e[1]==b1[4]:
			for i in a:
				if i!=None:
					cursor.execute("update student_attendance set M5_"+e[2]+" = 'P' where student_Id_id='%s'"%(i))
		cursor.execute("select distinct Academic_Course_Id_id from student_faculty where status='1'")
		h=cursor.fetchall()
		f=[]
		for i in h:
			if "-" not in i[0]:
				f.append(i)
		a1=['01','02','03','04','05']
		b1=['08','09','10','11','12']
		j = request.POST.get('cid')
		if e[1]==a1[0] or e[1]==b1[0]:
			cursor.execute("select Student_Id_id,M1_"+e[2]+" from student_attendance where Academic_Course_Id_id='%s'"%(j))
		elif e[1]==a1[1] or e[1]==b1[1]:
			cursor.execute("select Student_Id_id,M2_"+e[2]+" from student_attendance where Academic_Course_Id_id='%s'"%(j))
		elif e[1]==a1[2] or e[1]==b1[2]:
			cursor.execute("select Student_Id_id,M3_"+e[2]+" from student_attendance where Academic_Course_Id_id='%s'"%(j))
		elif e[1]==a1[3] or e[1]==b1[3]:
			cursor.execute("select Student_Id_id,M4_"+e[2]+" from student_attendance where Academic_Course_Id_id='%s'"%(j))
		elif e[1]==a1[4] or e[1]==b1[4]:
			cursor.execute("select Student_Id_id,M5_"+e[2]+" from student_attendance where Academic_Course_Id_id='%s'"%(j))	
		#return render(request,'student/adminhome.html',{'f':f})
		qw=cursor.fetchall()
		count=0
		for i in qw:
			if i[1]=='':
				count=count+1
		if len(qw)!=0 and count==0:
			return render(request, 'student/edit.html',{'d':d,'l':len(qw),'qw':qw,'f':f,'cid':j})
		elif count==len(qw):
			return render(request, 'student/edit.html',{'d':d,'l':len(qw),'qw':qw,'p':"No classes / Holiday",'f':f,'cid':j}) 

# 1st attendance display (edit attendance) 
def openedit(request):
	if request.method == 'POST':
		
		cursor.execute("select distinct Academic_Course_Id_id from student_faculty where status='1'")
		h=cursor.fetchall()
		f=[]
		for i in h:
			if "-" not in i[0]:
				f.append(i)
		if request.POST.get('date'):
			d=request.POST.get('date')
			e=d.split('-')
		else:
			return render(request,'student/adminhome.html',{'f':f,'msg':"Select date"})
		q=''
		a1=['01','02','03','04','05']
		b1=['08','09','10','11','12']
		j = request.POST.get('cid')
		if e[1]==a1[0] or e[1]==b1[0]:
			cursor.execute("select Student_Id_id,M1_"+e[2]+" from student_attendance where Academic_Course_Id_id='%s'"%(j))
		elif e[1]==a1[1] or e[1]==b1[1]:
			cursor.execute("select Student_Id_id,M2_"+e[2]+" from student_attendance where Academic_Course_Id_id='%s'"%(j))
		elif e[1]==a1[2] or e[1]==b1[2]:
			cursor.execute("select Student_Id_id,M3_"+e[2]+" from student_attendance where Academic_Course_Id_id='%s'"%(j))
		elif e[1]==a1[3] or e[1]==b1[3]:
			cursor.execute("select Student_Id_id,M4_"+e[2]+" from student_attendance where Academic_Course_Id_id='%s'"%(j))
		elif e[1]==a1[4] or e[1]==b1[4]:
			cursor.execute("select Student_Id_id,M5_"+e[2]+" from student_attendance where Academic_Course_Id_id='%s'"%(j))
		l=0
		#objects= Attendance.objects.filter(Student_Id=r,Academic_Course_Id=j)
		#query = "update student_attendance set M3_{e}={f} where Academic_Course_Id_id={j}".format(e=e, f=f, j=j)
		#cursor.execute(query)
		#for i in objects:
			#print(i.Student_Id)
		#cursor.execute("update student_attendance set M3_{e}={f} where Student_Id_id=i.Student_Id ".format(e=e,f=f))
		qw=cursor.fetchall()
		count=0
		for i in qw:
			if i[1]=='':
				count=count+1
		if len(qw)!=0 and count==0:
			return render(request, 'student/edit.html',{'d':d,'l':len(qw),'qw':qw,'f':f,'cid':j})
		elif count==len(qw):
			return render(request, 'student/edit.html',{'d':d,'l':len(qw),'qw':qw,'p':"No classes / Holiday",'f':f,'cid':j}) 

			
# upload attendance usecase
def upload_attendance(request):
	if request.method == 'POST':
		if (request.POST.get('file').split(".")[1])=="csv":
			g=request.POST.get('file')
			cursor.execute("delete from student_attendance")
			cursor.execute("load data local infile '/home/manu/{g}' into table student_attendance fields terminated by ','".format(g=g))
			cursor.execute("select distinct Academic_Course_Id_id from student_faculty where status='1'")
			h=cursor.fetchall()
			f=[]
			for i in h:
				if "-" not in i[0]:
					f.append(i)
			return render(request, 'student/adminhome.html',{'f':f})
		else:
			cursor.execute("select distinct Academic_Course_Id_id from student_faculty where status='1'")
			h=cursor.fetchall()
			f=[]
			for i in h:
				if "-" not in i[0]:
					f.append(i)
			errmsg="Only .csv files can be uploaded."
			return render(request, 'student/adminhome.html',{'errmsg':errmsg,'f':f})
			
# view attendance
def updated_attendance(request):
	if request.method == 'POST':
		if request.POST.get('fcid') and request.POST.get('sid') and request.POST.get('date'):
			g=request.POST.get('fcid')
			h=request.POST.get('sid')
			d=request.POST.get('date')
			e=d.split('-')
			if e[1]=='01' or e[1]=='08':
				cursor.execute("select M1_"+e[2]+" from student_attendance where student_Id_id='%s' and Academic_Course_Id_id='%s'"%(h,g))
			elif e[1]=='02' or e[1]=='09':
				cursor.execute("select M1_"+e[2]+" from student_attendance where student_Id_id='%s' and Academic_Course_Id_id='%s'"%(h,g))
			elif e[1]=='03' or e[1]=='10':
				cursor.execute("select M1_"+e[2]+" from student_attendance where student_Id_id='%s' and Academic_Course_Id_id='%s'"%(h,g))
			elif e[1]=='04' or e[1]=='11':
				cursor.execute("select M1_"+e[2]+" from student_attendance where student_Id_id='%s' and Academic_Course_Id_id='%s'"%(h,g))
			elif e[1]=='05' or e[1]=='12':
				cursor.execute("select M1_"+e[2]+" from student_attendance where student_Id_id='%s' and Academic_Course_Id_id='%s'"%(h,g))
			a=cursor.fetchall()
			b=[]
			for i in a:
				b.append(list(i))
			return render(request, 'student/viewatten.html',{'b':b})
	else:
		return render(request, 'student/f1.html')

def facultyhome(request):
	return render(request, 'student/facultyhome.html')
def student_attendance(request):
	return render(request, 'student/student_attendance.html')
def yu(request):
	return render(request, 'student/yu.html')

def EditMarks(request):
	return render(request, 'student/EditMarks.html')

def course(request):
	return render(request, 'student/course.html')
def PreCourse(request):
	return render(request, 'student/PreCourse.html')

def ty(request):
	return render(request, 'student/ty.html')
	
# view previous courses marks,percentage,grade for student
def ase(request):
	if request.method == 'POST':
			s=request.POST.get('id') 
			lp=request.POST.get('pwd') 
			now = datetime.datetime.now()
			y=str(now.year)
			a1=['01','02','03','04','05']
			b1=['08','09','10','11','12']
			if str(now.month) in a1:
				q='S_'+y
			elif str(now.month) in b1:
				q='M_'+y
			r2=Academic_score.function(q,s)
			#cursor.execute("select Academic_Course_Id_id,Exam_Type,Marks,Marks_perc from student_academic_score where semester!='%s' and student_Id_id='%s'"%(q,s))
			#r2=cursor.fetchall()
			print(r2)
			cursor.execute("select Academic_Course_Id_id,Exam_Type,Marks,Marks_perc,Facultycourse_Id_id from student_academic_score where semester!='%s' and student_Id_id='%s'"%(q,s))
			r=cursor.fetchall()
			grade=[]
			list1=[]
			list2=[]
			list3=[]
			tperc=0
			if len(r)!=0:
				x=r[0][0]
				y=r[0][4]
				for i in range(len(r)):
					if i==0 and r[i][0] not in list1:
						x=r[0][0]
						list1.append(x)
					if i!=0 and r[i][0] not in list1:
						list1.append(r[i][0])
						list2.append(x)
						list2.append(tperc)
						list2.append(y)
						list3.append(list2)
						list2=[]
						x=r[i][0]
						tperc=0
					y=r[i][4]
					tperc+=r[i][3]	
				list2.append(x)
				list2.append(tperc)
				list2.append(y)
				list3.append(list2)
				print("list3",list3)
				cursor.execute("select student_faculty.Academic_course_Id_id, student_gradeschema.A,student_gradeschema.A2,student_gradeschema.B,student_gradeschema.B2,student_gradeschema.C,student_gradeschema.C2,student_gradeschema.D,student_faculty.Facultycourse_Id from student_gradeschema join student_faculty where student_gradeschema.Facultycourse_Id_id=student_faculty.Facultycourse_Id")
				r1=cursor.fetchall()
				grade=[]
				grade1=[]
				for n in range(len(list3)):
					mcid=list3[n][0]
					mperc=list3[n][1]
					print("mperc",mperc)
					grade.append(mcid)
					for m in range(len(r1)):
						if r1[m][0]==mcid and r1[m][8]==list3[n][2]:
							A=r1[m][1].split("-")
							A2=r1[m][2].split("-")
							B=r1[m][3].split("-")
							B2=r1[m][4].split("-")
							C=r1[m][5].split("-")
							C2=r1[m][6].split("-")
							D=r1[m][7].split("-")
							if mperc>=int(A[0]) and mperc<=int(A[1]):
								grade.append('A')
							elif mperc>=int(A2[0]) and mperc<=int(A2[1]):
								grade.append('A-')
							elif mperc>=int(B[0]) and mperc<=int(B[1]):
								grade.append('B')
							elif mperc>=int(B2[0]) and mperc<=int(B2[1]):
								grade.append('B-')
							elif mperc>=int(C[0]) and mperc<=int(C2[1]):
								grade.append('C')
							elif mperc>=int(C2[0]) and mperc<=int(C2[1]):
								grade.append('C-')
							elif mperc>=int(D[0]) and mperc<=int(D[1]):
								grade.append('D')
							else:
								grade.append('F')
					grade1.append(grade)
					grade=[]
				cursor.execute("select student_image from student_student where Student_Id='%s'"%(s))
				v=cursor.fetchall()
				v1=[]
				for i in v:
					v1.append(list(i))
				print("grade",grade1)
				return render(request, 'student/PreCourse.html',{'t':r2,'v':v1[0][0],'s':s,'lp':lp,'g':grade1})
			else:
				cursor.execute("select student_image from student_student where Student_Id='%s'"%(s))
				v=cursor.fetchall()
				v1=[]
				for i in v:
					v1.append(list(i))
				return render(request, 'student/PreCourse.html',{'v':v1[0][0],'s':s,'lp':lp})	
	return render(request, 'student/PreCourse.html')
	
# view present semester courses,marks for student	
def func(request):
	if request.method == 'POST':
		flag=0
		s=request.POST.get('id')
		print("id",s)
		lp= request.POST.get('pwd')
		now = datetime.datetime.now()
		y=str(now.year)
		a1=['01','02','03','04','05']
		b1=['08','09','10','11','12']
		grade=[]
		grade1=[]
		list1=[]
		list2=[]
		list3=[]
		tperc=0
			#cursor.execute("select student_academic_score.Academic_course_Id_id,Exam_Type,Marks from student_faculty join student_academic_score where student_academic_score.Facultycourse_Id_id=student_faculty.Facultycourse_Id and student_academic_score.Student_Id_id='%s' and student_faculty.status='%s' and semester="%(s,x))
		if str(now.month) in a1:
			w='S_'+y
			
			cursor.execute("select Academic_Course_Id_id,Exam_Type,Marks,Marks_perc,Facultycourse_Id_id from student_academic_score where semester='%s' and student_Id_id='%s' order by Academic_Course_Id_id"%(w,s))
			r=cursor.fetchall()
			cursor.execute("select Academic_Course_Id_id,Exam_Type,Marks,Marks_perc from student_academic_score where semester='%s' and student_Id_id='%s' order by Academic_Course_Id_id"%(w,s))
			r2=cursor.fetchall()

		elif str(now.month) in b1:
			w='M_'+y
			cursor.execute("select Academic_Course_Id_id,Exam_Type,Marks,Marks_perc,Facultycourse_Id_id from student_academic_score where semester='%s' and student_Id_id='%s' order by Academic_Course_Id_id"%(w,s))
			r=cursor.fetchall()
			cursor.execute("select Academic_Course_Id_id,Exam_Type,Marks,Marks_perc from student_academic_score where semester='%s' and student_Id_id='%s' order by Academic_Course_Id_id"%(w,s))
			r2=cursor.fetchall()

		if (str(now.month)=='12' and str(now.day)=='25') or (str(now.month)=='5' and str(now.day)=='25'):
			flag=1
			x=r[0][0]
			y=r[0][4]
			for i in range(len(r)):
				if i==0 and r[i][0] not in list1:
					x=r[0][0]
					list1.append(x)
				if i!=0 and r[i][0] not in list1:
					list1.append(r[i][0])
					list2.append(x)
					list2.append(tperc)
					list2.append(y)
					list3.append(list2)
					list2=[]
					x=r[i][0]
					tperc=0
				y=r[i][4]
				tperc+=r[i][3]	
			list2.append(x)
			list2.append(tperc)
			list2.append(y)
			list3.append(list2)
			cursor.execute("select student_faculty.Academic_course_Id_id, student_gradeschema.A,student_gradeschema.A2,student_gradeschema.B,student_gradeschema.B2,student_gradeschema.C,student_gradeschema.C2,student_gradeschema.D,student_faculty.Facultycourse_Id from student_gradeschema join student_faculty where student_gradeschema.Facultycourse_Id_id=student_faculty.Facultycourse_Id")
			r1=cursor.fetchall()
			grade=[]
			for n in range(len(list3)):
				mcid=list3[n][0]
				mperc=list3[n][1]
				grade.append(mcid)
				for m in range(len(r1)):
					if r1[m][0]==mcid and r1[m][8]==list3[n][2]:
						A=r1[m][1].split("-")
						A2=r1[m][2].split("-")
						B=r1[m][3].split("-")
						B2=r1[m][4].split("-")
						C=r1[m][5].split("-")
						C2=r1[m][6].split("-")
						D=r1[m][7].split("-")
						if mperc>=int(A[0]) and mperc<=int(A[1]):
							grade.append('A')
						elif mperc>=int(A2[0]) and mperc<=int(A2[1]):
							grade.append('A-')
						elif mperc>=int(B[0]) and mperc<=int(B[1]):
							grade.append('B')
						elif mperc>=int(B2[0]) and mperc<=int(B2[1]):
							grade.append('B-')
						elif mperc>=int(C[0]) and mperc<=int(C2[1]):
							grade.append('C')
						elif mperc>=int(C2[0]) and mperc<=int(C2[1]):
							grade.append('C-')
						elif mperc>=int(D[0]) and mperc<=int(D[1]):
							grade.append('D')
						else:
							grade.append('F')	
				grade1.append(grade)
				grade=[]		
		cursor.execute("select student_image from student_student where Student_Id='%s'"%(s))
		v=cursor.fetchall()
		v1=[]
		for i in v:
			v1.append(list(i))
		cursor.execute("select student_Achievement from student_achievements where Student_Id_id='%s'"%(s))
		kl=cursor.fetchall()
		cursor.execute("select Club_President,Club_Vicepresident from student_student where Student_Id='%s'"%(s))
		ui=cursor.fetchall()
		cl=''
		vcl=''
		if ui[0][0] and len(ui)!=0:
			cl=ui[0][0].split('_')
			if len(r)!=0:
				if flag==0:
			 		return render(request, 'student/Acad.html',{'cl':cl,'kl':kl,'t':r2,'v':v1[0][0],'s':s,'lp':lp,'flag':flag})
				else:
					return render(request, 'student/Acad.html',{'cl':cl,'kl':kl,'t':r2,'v':v1[0][0],'s':s,'lp':lp,'g':grade1,'flag':flag})
		if ui[0][1] and len(ui)!=0:
			vcl=ui[0][1].split('_')
			if len(r)!=0:
				if flag==0:
			 		return render(request, 'student/Acad.html',{'vcl':vcl,'kl':kl,'t':r2,'v':v1[0][0],'s':s,'lp':lp,'flag':flag})
				else:
					return render(request, 'student/Acad.html',{'vcl':vcl,'kl':kl,'t':r2,'v':v1[0][0],'s':s,'lp':lp,'g':grade1,'flag':flag})
		if len(r)!=0:
			if flag==0:
			 	return render(request, 'student/Acad.html',{'cl':cl,'vcl':vcl,'kl':kl,'t':r2,'v':v1[0][0],'s':s,'lp':lp,'flag':flag})
			else:
				return render(request, 'student/Acad.html',{'cl':cl,'vcl':vcl,'kl':kl,'t':r2,'v':v1[0][0],'s':s,'lp':lp,'g':grade1,'flag':flag})
		else:
			p="Marks are not updated.Please try after some time!!!"
			#v2=v1[0][0].decode('utf-8')
			return render(request, 'student/Acad.html',{'kl':kl,'p':p,'v':v1[0][0],'s':s,'lp':lp})
				
	



# upload marks for present courses/BTP/Honors projects
def loadmarks(request):
	if request.method == 'POST':
		g=request.POST.get('file')
		v=request.POST.get('examtype')
		u=request.POST.get('cid')
		q=request.POST.get('sem')
		li=request.POST.get('s')
		lp=request.POST.get('pwd')
		x=request.POST.get('xid')
		if (request.POST.get('file').split(".")[1])=="csv":
			
			cursor.execute("load data local infile '/home/manu/{g}' into table student_academic_score fields terminated by ','".format(g=g))
			#cursor.execute("select Facultycourse_Id from student_faculty where Academic_Course_Id_id='%s'and Status='1'"%(u))	
			#r=cursor.fetchall()	
			r=student_faculty.function2(u)
			u1=[]	
			for i in r:
				u1.append(list(i))
			#print("u1",u1)
			cursor.execute("select tmarks,wmarks from student_gradeweightage where Exam_Type='%s' and Facultycourse_Id_id='%s' and Semester='%s'"%(v,u1[0][0],q))
			h=cursor.fetchall()
			u2=[]
			for i in h:
				u2.append(list(i))
			#print("u2",u2)
			cursor.execute("select count(*) from student_academic_score where Exam_Type='%s' and Academic_Course_Id_id='%s' and Semester='%s'"%(v,u,q))
			u3=cursor.fetchall()
			u4=[]
			for i in u3:
				u4.append(list(i))
			#print("u4",u4)
			cursor.execute("select Marks,Student_Id_id from student_academic_score where Exam_Type='%s' and Academic_Course_Id_id='%s' and Semester='%s'"%(v,u,q))
			u5=cursor.fetchall()
			u6=[]
			
			for i in u5:
				u6.append(list(i))
			#print("u6",u6)
			for i in range(u4[0][0]):	
				perc =round((float(u6[i][0])/float(u2[0][0]))*float(u2[0][1]),2)
				cursor.execute("update student_academic_score set Marks_perc='%f' where Exam_type='%s' and Semester='%s' and Academic_Course_Id_id='%s' and Student_Id_id='%s'"%(perc,v,q,u,u6[i][1]))			
			return render(request,'student/course.html',{'w':u,'li':li,'lp':lp,'x':x})
		else:
			return render(request,'student/course.html',{'w':u,'li':li,'lp':lp,'x':x,'msg1':"Only .csv files can be uploaded."})
	#return render(request, 'student/facultyhome.html')

# upload project marks
"""def aloadpro(request):
	if request.method == 'POST':
		if request.POST.get('file'):
			g=request.POST.get('file')
			cursor.execute("load data local infile '/home/vasu/{g}' into table student_academic_score fields terminated by ','".format(g=g))
			return render(request, 'student/facultyhome.html')
	else:
		return render(request, 'student/facultyhome.html')"""


# edit courses marks
def emarks(request):
	if request.method == 'POST':
		len1=request.POST.get('len')
		w=request.POST.get('cid')
		li=request.POST.get('lid')
		lp=request.POST.get('lpwd')
		x=request.POST.get('xid')
		exty=request.POST.get('exty')
		print("in emarks",w,li,lp,x,exty)
		cursor.execute("select FacultyCourse_Id from student_faculty where Faculty_Id='%s' and Academic_Course_Id_id='%s'"%(li,w))
		fcid=cursor.fetchall()
		print("fcid in emarks",fcid)
		u=[]
		cursor.execute("select tmarks,wmarks from student_gradeweightage where Facultycourse_Id_id='%s' and Exam_Type='%s'"%(fcid[0][0],exty))
		h=cursor.fetchall()
		for i in h:
			u.append(list(i))
		b=[]
		z=[]
		for i in range(int(len1)):
			b.append(str(i))
		for i in range(int(len1)):
			z.append("ns"+str(i))
		for i in range(int(len1)):
			
			if request.POST.get(b[i]) != None and request.POST.get(z[i])!= None:
				c=request.POST.get(z[i])
				perc = (float(c)/float(u[0][0]))*float(u[0][1])
				cursor.execute("update student_academic_score set Marks='%s',Marks_perc='%f' where Student_Id_id='%s' and Facultycourse_Id_id='%s' and Exam_Type='%s'"%(c,perc,request.POST.get(b[i]),fcid[0][0],exty))
		now = datetime.datetime.now()
		y=str(now.year)
		q=''
		a1=[1,2,3,4,5]
		b1=[8,9,10,11,12]
		if now.month in a1:
			q='S_'+y
		elif now.month in b1:
			q='M_'+y
		cursor.execute("select Student_Id_id,Marks,Marks_perc from student_academic_score where semester='%s' and Academic_Course_Id_id='%s' and Exam_Type='%s' order by Marks desc"%(q,w,exty))
		t=cursor.fetchall()
		if len(t)!=0:
			return render(request, 'student/EditMarks.html',{'w':w,'li':li,'lp':lp,'x':x,'t':t,'exty':exty,'len':len(t)})
		else:
			return render(request, 'student/EditMarks.html',{'p':"Marks aren't updated yet!!!"})
		#return render(request, 'student/EditMarks.html',{'w':w,'li':li,'lp':lp,'x':x})
				
		"""a=request.POST.get('roll')
		b=request.POST.get('type')
		c=request.POST.get('mar')
		w=request.POST.get('cid')
		li=request.POST.get('lid')
		lp=request.POST.get('lpwd')
		x=request.POST.get('xid')
		#objects=Faculty.objects.filter(Academic_Course_Id_id=par,Status=1)
		cursor.execute("select Facultycourse_Id from student_faculty where Academic_Course_Id_id='%s' and Status='1'"%(w))
		e=cursor.fetchall()
		o=[]
		for i in e:
			o.append(list(i))
		u=[]
		cursor.execute("select tmarks,wmarks from student_gradeweightage where Facultycourse_Id_id='%s' and Exam_Type='%s'"%(o[0][0],b))
		h=cursor.fetchall()
		for i in h:
			u.append(list(i))
		perc = (float(c)/float(u[0][0]))*float(u[0][1])
		cursor.execute("update student_academic_score set Marks='%s',Marks_perc='%f' where Student_Id_id='%s' and Facultycourse_Id_id='%s' and Exam_Type='%s'"%(c,perc,a,o[0][0],b))
		return render(request, 'student/EditMarks.html',{'w':w,'li':li,'lp':lp,'x':x})"""
		#return render(request,'student/sign.html')
		
"""def fun(request):
	if request.method == 'POST':
		d=request.POST.get('fcid')
		return render(request, 'student/test.html',{'d':d})
		#emarks(d)"""

#edit project marks
def pmarks(request):
	if request.method == 'POST':
		a=request.POST.get('roll')
		c=request.POST.get('marks')
		par=request.POST.get('pid')
		#objects=Faculty.objects.filter(Academic_Course_Id_id=par,Status=1)
		#cursor.execute("select Facultycourse_Id from student_faculty where Academic_Course_Id_id='%s' and Status='1'"%(par))
		#e=cursor.fetchall()
		#o=[]
		#for i in e:
		#	o.append(list(i))
		u=[]
		cursor.execute("select tmarks,wmarks from student_gradeweightage where Facultycourse_Id_id='%s' and Exam_Type='%s'"%(par,b))
		h=cursor.fetchall()
		for i in h:
			u.append(list(i))
		perc = (float(c)/float(u[0][0]))*float(u[0][1])
		cursor.execute("update student_academic_score set Marks='%s',Marks_perc='%f' where Student_Id_id='%s' and Facultycourse_Id_id='%s'"%(c,perc,a,par))
		return render(request, 'student/project.html')
		
	else:
		return render(request, 'student/project.html')

def marks(request):
	return render(request, 'student/marks.html')
def ghmarks(request):
	return render(request, 'student/ghmarks.html')
def editm(request):
	w=request.POST.get('cid')
	li=request.POST.get('id')
	lp=request.POST.get('pwd')
	x=request.POST.get('xid')
	exty=request.POST.get('exty')
	now = datetime.datetime.now()
	y=str(now.year)
	q=''
	a1=[1,2,3,4,5]
	b1=[8,9,10,11,12]
	if now.month in a1:
		q='S_'+y
	elif now.month in b1:
		q='M_'+y
	cursor.execute("select Student_Id_id,Marks,Marks_perc from student_academic_score where semester='%s' and Academic_Course_Id_id='%s' and Exam_Type='%s' order by Marks"%(q,w,exty))
	t=cursor.fetchall()
	if len(t)!=0:
		return render(request, 'student/EditMarks.html',{'w':w,'li':li,'lp':lp,'x':x,'t':t,'exty':exty,'len':len(t)})
	else:
		return render(request, 'student/EditMarks.html',{'p':"Marks aren't updated yet!!!"})
#def sendmail(request):

# ordered marks onclick
def ordermarks(request):
	if request.method == 'POST':
		
		flag=0
		s=request.POST.get('s')
		lp= request.POST.get('lp')
		print("cred",s,lp)
		now = datetime.datetime.now()
		y=str(now.year)
		a1=['01','02','03','04','05']
		b1=['08','09','10','11','12']
		grade=[]
		grade1=[]
		list1=[]
		list2=[]
		list3=[]
		tperc=0
			#cursor.execute("select student_academic_score.Academic_course_Id_id,Exam_Type,Marks from student_faculty join student_academic_score where student_academic_score.Facultycourse_Id_id=student_faculty.Facultycourse_Id and student_academic_score.Student_Id_id='%s' and student_faculty.status='%s' and semester="%(s,x))
		if str(now.month) in a1:
			w='S_'+y
			
			cursor.execute("select Academic_Course_Id_id,Exam_Type,Marks,Marks_perc,Facultycourse_Id_id from student_academic_score where semester='%s' and student_Id_id='%s' order by Marks"%(w,s))
			r=cursor.fetchall()
			cursor.execute("select Academic_Course_Id_id,Exam_Type,Marks,Marks_perc from student_academic_score where semester='%s' and student_Id_id='%s' order by Marks"%(w,s))
			r2=cursor.fetchall()

		elif str(now.month) in b1:
			w='M_'+y
			cursor.execute("select Academic_Course_Id_id,Exam_Type,Marks,Marks_perc,Facultycourse_Id_id from student_academic_score where semester='%s' and student_Id_id='%s' order by Marks"%(w,s))
			r=cursor.fetchall()
			print("in order",r)
			cursor.execute("select Academic_Course_Id_id,Exam_Type,Marks,Marks_perc from student_academic_score where semester='%s' and student_Id_id='%s' order by Marks"%(w,s))
			r2=cursor.fetchall()

		if (str(now.month)=='12' and str(now.day)=='25') or (str(now.month)=='5' and str(now.day)=='25'):
			flag=1
			x=r[0][0]
			y=r[0][4]
			for i in range(len(r)):
				if i==0 and r[i][0] not in list1:
					x=r[0][0]
					list1.append(x)
				if i!=0 and r[i][0] not in list1:
					list1.append(r[i][0])
					list2.append(x)
					list2.append(tperc)
					list2.append(y)
					list3.append(list2)
					list2=[]
					x=r[i][0]
					tperc=0
				y=r[i][4]
				tperc+=r[i][3]	
			list2.append(x)
			list2.append(tperc)
			list2.append(y)
			list3.append(list2)
			cursor.execute("select student_faculty.Academic_course_Id_id, student_gradeschema.A,student_gradeschema.A2,student_gradeschema.B,student_gradeschema.B2,student_gradeschema.C,student_gradeschema.C2,student_gradeschema.D,student_faculty.Facultycourse_Id from student_gradeschema join student_faculty where student_gradeschema.Facultycourse_Id_id=student_faculty.Facultycourse_Id")
			r1=cursor.fetchall()
			grade=[]
			for n in range(len(list3)):
				mcid=list3[n][0]
				mperc=list3[n][1]
				grade.append(mcid)
				for m in range(len(r1)):
					if r1[m][0]==mcid and r1[m][8]==list3[n][2]:
						A=r1[m][1].split("-")
						A2=r1[m][2].split("-")
						B=r1[m][3].split("-")
						B2=r1[m][4].split("-")
						C=r1[m][5].split("-")
						C2=r1[m][6].split("-")
						D=r1[m][7].split("-")
						if mperc>=int(A[0]) and mperc<=int(A[1]):
							grade.append('A')
						elif mperc>=int(A2[0]) and mperc<=int(A2[1]):
							grade.append('A-')
						elif mperc>=int(B[0]) and mperc<=int(B[1]):
							grade.append('B')
						elif mperc>=int(B2[0]) and mperc<=int(B2[1]):
							grade.append('B-')
						elif mperc>=int(C[0]) and mperc<=int(C2[1]):
							grade.append('C')
						elif mperc>=int(C2[0]) and mperc<=int(C2[1]):
							grade.append('C-')
						elif mperc>=int(D[0]) and mperc<=int(D[1]):
							grade.append('D')
						else:
							grade.append('F')	
				grade1.append(grade)
				grade=[]		
		cursor.execute("select student_image from student_student where Student_Id='%s'"%(s))
		v=cursor.fetchall()
		v1=[]
		for i in v:
			v1.append(list(i))
		#cursor.execute("select student_Achievement from student_club where Student_Id_id='%s'"%(s))
		#kl=cursor.fetchall()
		if len(r)!=0:
			if flag==0:
			 	return render(request, 'student/Acad.html',{'t':r2,'v':v1[0][0],'s':s,'lp':lp,'flag':flag})
			else:
				return render(request, 'student/Acad.html',{'t':r2,'v':v1[0][0],'s':s,'lp':lp,'g':grade1,'flag':flag})
		else:
			p="Marks are not updated.Please try after some time!!!"
			#v2=v1[0][0].decode('utf-8')
			return render(request, 'student/Acad.html',{'p':p,'s':s,'lp':lp})
				
	
# view marks by faculty for present semester courses
def hjmarks(request):
	if request.method == 'POST':
		
		a=request.POST.get('cid')
		x=request.POST.get('xid')
		li=request.POST.get('id')
		lp=request.POST.get('pwd')
		now = datetime.datetime.now()
		grade=[]
		flag=0
		if x=='1' or x=='3':
			cursor.execute("select Facultycourse_Id from student_faculty where Academic_Course_Id_id='%s' and Status='1'"%(a))
		elif x=='2' or x=='4':
			cursor.execute("select Facultycourse_Id from student_faculty where Academic_Course_Id_id='%s' and Status='2'"%(a))
		b=cursor.fetchall()
		c=[]
		for i in b:
			c.append(list(i))
		#cursor.execute("select Student_Id_id,Exam_Type,Marks,Marks_perc,Semester,Facultycourse_Id_id from student_academic_score order by Marks")
		#d=cursor.fetchall()
		d=Academic_score.function1()
		e=[]
		f=[]
		f1=[]
		for i in d:
			e.append(list(i))
		print("c",c)
		print("e",e)
		if len(e)!=0:
			for j in range(len(e)):
				if c[0][0]==e[j][5]:
					#flag=1
					f.append(e[j][0])
					f.append(e[j][1])
					f.append(e[j][2])
					f.append(e[j][3])
					f.append(e[j][4])
					f1.append(f)
					f=[]
				"""if flag==1:
					flag=0
					break"""
			return render(request, 'student/marks.html',{'kl':f1,'li':li,'lp':lp,'x':x,'a':a})
		else:
			return render(request, 'student/marks.html',{'p':"Marks aren't updated yet!!!"})
		


# view marks by faculty for previous semester
def mlmarks(request):
	if request.method == 'POST':
		li=request.POST.get('id')
		lp=request.POST.get('pwd')
		x=request.POST.get('xid')
		a=request.POST.get('cid')
		return render(request, 'student/course.html',{'li':li,'lp':lp,'x':x,'w':a})
	#return render(request, 'student/course.html')
#def sendemail(request):
	
	#return render(request, 'student/Main_page.html')
		
	"""send_mail('This is the subject',
		'This is the message',
		'pullelamrudula8@gmail.com',
		['manogna.p16@iiits.in'],
		 fail_silently=False)

	return render(request, 'mainmail/index.html')"""
	
# ordered attendance on total percentage
def orderatten(request):
	if request.method == 'POST':
		a=request.POST.get('id')
		b=request.POST.get('pwd')
		now=datetime.datetime.now()
		month=now.month
		date=now.day
		ya=now.year
		year=str(now.year)
		a1=[1,2,3,4,5]
		b1=[8,9,10,11,12]
		if month in a1:
			year='S_'+year
		else:
			year='M_'+year
		cour=[]
		per=[]
		per1=[]
		per2=[]
		per3=[]

		# courses 
		cursor.execute("select student_attendance.Academic_course_Id_id from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
		h=cursor.fetchall()
		
			# count for classes 
		for i in range(len(h)):
			per.append(0)
			per1.append(0)
			per2.append(0)
			# append courses
		for i in range(len(h)):
			cour.append(h[i][0])
		if month==1 or month==8:
			for i in range(1,date+1):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M1_"+s+",student_attendance.Academic_course_Id_id from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1


		elif month==2 or month==9:
			for i in range(1,32):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M1_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1
			for i in range(1,date+1):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M2_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1

		elif month==3 or month==10:
			for i in range(1,32):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M1_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				cursor.execute("select M2_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				w=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if w[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1
					if w[i][0]=='A' or w[i][0]=='P':
						per1[i]+=1
			for i in range(1,date+1):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M3_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1


		elif month==4 or month==11:
			for i in range(1,32):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M1_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				cursor.execute("select M2_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				w=cursor.fetchall()
				cursor.execute("select M3_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				w1=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if w[i][0]=='P':
						per[i]+=1
					if w1[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1
					if w[i][0]=='A' or w[i][0]=='P':
						per1[i]+=1
					if w1[i][0]=='A' or w1[i][0]=='P':
						per1[i]+=1
			for i in range(1,date+1):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M4_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1


		elif month==5 or month==12:
			for i in range(1,32):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M1_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id "%(a,year))
				r=cursor.fetchall()
				cursor.execute("select M2_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				w=cursor.fetchall()
				cursor.execute("select M3_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				w1=cursor.fetchall()
				cursor.execute("select M4_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				w2=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if w[i][0]=='P':
						per[i]+=1
					if w1[i][0]=='P':
						per[i]+=1
					if w2[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1
					if w[i][0]=='A' or w[i][0]=='P':
						per1[i]+=1
					if w1[i][0]=='A' or w1[i][0]=='P':
						per1[i]+=1
					if w2[i][0]=='A' or w2[i][0]=='P':
						per1[i]+=1
			for i in range(1,date+1):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M5_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1
		for i in range(len(h)):
			per2[i]=round((per[i]/per1[i])*100,2)
		per4=[]
		for i in range(len(h)):
			per3.append(cour[i])
			per3.append(per2[i])
			per4.append(per3)
			per3=[]
		print(per4)
		per4.sort(key=itemgetter(1))
		return render(request, 'student/student_attendance.html',{'per':per4,'s':a,'lp':b,'cour':cour,'date':date,'month':month,'day':ya})

# view attendance for students
def phjmarks(request):
	if request.method == 'POST':
		a=request.POST.get('id')
		b=request.POST.get('pwd')
		now=datetime.datetime.now()
		month=now.month
		date=now.day
		ya=now.year
		year=str(now.year)
		a1=[1,2,3,4,5]
		b1=[8,9,10,11,12]
		if month in a1:
			year='S_'+year
		else:
			year='M_'+year
		cour=[]
		per=[]
		per1=[]
		per2=[]
		per3=[]

		# courses 
		cursor.execute("select student_attendance.Academic_course_Id_id from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
		h=cursor.fetchall()
		
			# count for classes 
		for i in range(len(h)):
			per.append(0)
			per1.append(0)
			per2.append(0)
			# append courses
		for i in range(len(h)):
			cour.append(h[i][0])
		if month==1 or month==8:
			for i in range(1,date+1):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M1_"+s+",student_attendance.Academic_course_Id_id from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1


		elif month==2 or month==9:
			for i in range(1,32):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M1_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1
			for i in range(1,date+1):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M2_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1

		elif month==3 or month==10:
			for i in range(1,32):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M1_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				cursor.execute("select M2_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				w=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if w[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1
					if w[i][0]=='A' or w[i][0]=='P':
						per1[i]+=1
			for i in range(1,date+1):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M3_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1


		elif month==4 or month==11:
			for i in range(1,32):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M1_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				cursor.execute("select M2_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				w=cursor.fetchall()
				cursor.execute("select M3_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				w1=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if w[i][0]=='P':
						per[i]+=1
					if w1[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1
					if w[i][0]=='A' or w[i][0]=='P':
						per1[i]+=1
					if w1[i][0]=='A' or w1[i][0]=='P':
						per1[i]+=1
			for i in range(1,date+1):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M4_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1


		elif month==5 or month==12:
			for i in range(1,32):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M1_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id "%(a,year))
				r=cursor.fetchall()
				cursor.execute("select M2_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				w=cursor.fetchall()
				cursor.execute("select M3_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				w1=cursor.fetchall()
				cursor.execute("select M4_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				w2=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if w[i][0]=='P':
						per[i]+=1
					if w1[i][0]=='P':
						per[i]+=1
					if w2[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1
					if w[i][0]=='A' or w[i][0]=='P':
						per1[i]+=1
					if w1[i][0]=='A' or w1[i][0]=='P':
						per1[i]+=1
					if w2[i][0]=='A' or w2[i][0]=='P':
						per1[i]+=1
			for i in range(1,date+1):
				if i<10:
					s='0'+str(i)
				else:
					s=str(i)
				cursor.execute("select M5_"+s+" from student_attendance join student_registration where student_attendance.Student_Id_id=student_registration.Student_Id_id and student_attendance.Academic_course_Id_id=student_registration .Academic_course_Id_id and student_attendance.Student_Id_id='%s' and Semester='%s' order by student_attendance.Academic_course_Id_id"%(a,year))
				r=cursor.fetchall()
				for i in range(len(r)):
					if r[i][0]=='P':
						per[i]+=1
					if r[i][0]=='A' or r[i][0]=='P':
						per1[i]+=1
		for i in range(len(h)):
			per2[i]=round((per[i]/per1[i])*100,2)
		per4=[]
		for i in range(len(h)):
			per3.append(cour[i])
			per3.append(per2[i])
			per4.append(per3)
			per3=[]
		print(per4)
		return render(request, 'student/student_attendance.html',{'per':per4,'s':a,'lp':b,'cour':cour,'date':date,'month':month,'day':ya})
		
		
		
now1=datetime.datetime.now()
time=now1.hour
print(time)
if time==1:
	#sendemail()
	cursor.execute("select student_student.Student_Id,student_attendance.Academic_Course_Id_id, student_student.Student_Email,M1_01,M1_02,M1_03,M1_04,M1_05,M1_06,M1_07,M1_08,M1_09,M1_10,M1_11,M1_12,M1_13,M1_14,M1_15,M1_16,M1_17,M1_18,M1_19,M1_20,M1_21,M1_22,M1_23,M1_24,M1_25,M1_26,M1_27,M1_28,M1_29,M1_30,M1_31,M2_01,M2_02,M2_03,M2_04,M2_05,M2_06,M2_07,M2_08,M2_09,M2_10,M2_11,M2_12,M2_13,M2_14,M2_15,M2_16,M2_17,M2_18,M2_19,M2_20,M2_21,M2_22,M2_23,M2_24,M2_25,M2_26,M2_27,M2_28,M2_29,M2_30,M2_31,M3_01,M3_02,M3_03,M3_04,M3_05,M3_06,M3_07,M3_08,M3_09,M3_10,M3_11,M3_12,M3_13,M3_14,M3_15,M3_16,M3_17,M3_18,M3_19,M3_20,M3_21,M3_22,M3_23,M3_24,M3_25,M3_26,M3_27,M3_28,M3_29,M3_30,M3_31,M4_01,M4_02,M4_03,M4_04,M4_05,M4_06,M4_07,M4_08,M4_09,M4_10,M4_11,M4_12,M4_13,M4_14,M4_15,M4_16,M4_17,M4_18,M4_19,M4_20,M4_21,M4_22,M4_23,M4_24,M4_25,M4_26,M4_27,M4_28,M4_29,M4_30,M4_31,M5_01,M5_02,M5_03,M5_04,M5_05,M5_06,M5_07,M5_08,M5_09,M5_10,M5_11,M5_12,M5_13,M5_14,M5_15,M5_16,M5_17,M5_18,M5_19,M5_20,M5_21,M5_22,M5_23,M5_24,M5_25,M5_26,M5_27,M5_28,M5_29,M5_30,M5_31 from student_student join student_attendance where student_student.Student_Id=student_attendance.Student_Id_id order by student_attendance.Student_Id_id")
	res=cursor.fetchall()
	count=0
	mid=[]
	for i in res:
		sid=i[0]
		cid=i[1]
		count=0
		for j in i:
			if count==15:
				dsid=sid
				mid.append(i[2])
				print(mid,dsid)
				send_mail('Regarding Attendance',
					'Absent for more than 15 days in '+cid+' .Dropped you from the course.',
					'spsattendance3@gmail.com',
					mid,
					fail_silently=False)
				mid=[]
				"""cursor.execute("delete from student_academic_score where student_Id_id='%s'"%(dsid))
				cursor.execute("delete from student_achievements where student_Id_id='%s'"%(dsid))
				cursor.execute("delete from student_attendance where student_Id_id='%s'"%(dsid))
				#cursor.execute("delete from student_club where student_Id_id='%s'"%(dsid))
				cursor.execute("delete from student_registration where student_Id_id='%s'"%(dsid))
				cursor.execute("delete from student_student where student_Id='%s'"%(dsid))"""
				break
			if j=='A':
				count+=1
				cursor.execute("update student_attendance set count='%d' where student_Id_id='%s' and Academic_Course_Id_id='%s'"%(count,sid,cid))
			elif j=='P':
				count=0
				cursor.execute("update student_attendance set count='%d' where student_Id_id='%s' and Academic_Course_Id_id='%s'"%(count,sid,cid))
	
	
	
	

	
else:
	print("&&&&&&")
