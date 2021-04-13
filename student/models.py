from django.db import models
from django.db import connection  

class Student(models.Model):
	Student_Id = models.CharField(max_length=20,primary_key=True)
	Student_First_Name = models.CharField(max_length=45)
	Student_Middle_Name = models.CharField(max_length=45)
	Student_Last_Name = models.CharField(max_length=45)
	Student_DOB = models.CharField(max_length=45)
	Student_Gender = models.CharField(max_length=10)
	Student_Email = models.EmailField(max_length=100)
	Student_Registered_Year = models.IntegerField()
	Club_President = models.CharField(max_length=20, null=True)
	Club_Vicepresident = models.CharField(max_length=20,null=True)
	student_image = models.ImageField(null=True)

class Academic_Course(models.Model):
	Academic_Course_Id = models.CharField(max_length=20,primary_key=True,default='C1')
	Academic_Course_Name = models.CharField(max_length=100)
class Registration(models.Model):
	Student_Id = models.ForeignKey(Student,on_delete=models.CASCADE)
	Academic_Course_Id = models.ForeignKey(Academic_Course,on_delete=models.CASCADE)
	Semester = models.CharField(max_length=10,null=True)
class Attendance(models.Model):
	Student_Id = models.ForeignKey(Student,on_delete=models.CASCADE)
	Academic_Course_Id = models.ForeignKey(Academic_Course,on_delete=models.CASCADE)

	M1_01 = models.CharField(max_length=10,null=True)
	M1_02 = models.CharField(max_length=10,null=True)
	M1_03 = models.CharField(max_length=10,null=True)
	M1_04 = models.CharField(max_length=10,null=True)
	M1_05 = models.CharField(max_length=10,null=True)
	M1_06 = models.CharField(max_length=10,null=True)
	M1_07 = models.CharField(max_length=10,null=True)
	M1_08 = models.CharField(max_length=10,null=True)
	M1_09 = models.CharField(max_length=10,null=True)
	M1_10 = models.CharField(max_length=10,null=True)
	M1_11 = models.CharField(max_length=10,null=True)
	M1_12 = models.CharField(max_length=10,null=True)
	M1_13 = models.CharField(max_length=10,null=True)
	M1_14 = models.CharField(max_length=10,null=True)
	M1_15 = models.CharField(max_length=10,null=True)
	M1_16 = models.CharField(max_length=10,null=True)
	M1_17 = models.CharField(max_length=10,null=True)
	M1_18 = models.CharField(max_length=10,null=True)
	M1_19 = models.CharField(max_length=10,null=True)
	M1_20 = models.CharField(max_length=10,null=True)
	M1_21 = models.CharField(max_length=10,null=True)
	M1_22 = models.CharField(max_length=10,null=True)
	M1_23 = models.CharField(max_length=10,null=True)
	M1_24 = models.CharField(max_length=10,null=True)
	M1_25 = models.CharField(max_length=10,null=True)
	M1_26 = models.CharField(max_length=10,null=True)
	M1_27 = models.CharField(max_length=10,null=True)
	M1_28 = models.CharField(max_length=10,null=True)
	M1_29 = models.CharField(max_length=10,null=True)
	M1_30 = models.CharField(max_length=10,null=True)
	M1_31 = models.CharField(max_length=10,null=True)
	
	M2_01 = models.CharField(max_length=10,null=True)
	M2_02 = models.CharField(max_length=10,null=True)
	M2_03 = models.CharField(max_length=10,null=True)
	M2_04 = models.CharField(max_length=10,null=True)
	M2_05 = models.CharField(max_length=10,null=True)
	M2_06 = models.CharField(max_length=10,null=True)
	M2_07 = models.CharField(max_length=10,null=True)
	M2_08 = models.CharField(max_length=10,null=True)
	M2_09 = models.CharField(max_length=10,null=True)
	M2_10 = models.CharField(max_length=10,null=True)
	M2_11 = models.CharField(max_length=10,null=True)
	M2_12 = models.CharField(max_length=10,null=True)
	M2_13 = models.CharField(max_length=10,null=True)
	M2_14 = models.CharField(max_length=10,null=True)
	M2_15 = models.CharField(max_length=10,null=True)
	M2_16 = models.CharField(max_length=10,null=True)
	M2_17 = models.CharField(max_length=10,null=True)
	M2_18 = models.CharField(max_length=10,null=True)
	M2_19 = models.CharField(max_length=10,null=True)
	M2_20 = models.CharField(max_length=10,null=True)
	M2_21 = models.CharField(max_length=10,null=True)
	M2_22 = models.CharField(max_length=10,null=True)
	M2_23 = models.CharField(max_length=10,null=True)
	M2_24 = models.CharField(max_length=10,null=True)
	M2_25 = models.CharField(max_length=10,null=True)
	M2_26 = models.CharField(max_length=10,null=True)
	M2_27 = models.CharField(max_length=10,null=True)
	M2_28 = models.CharField(max_length=10,null=True)
	M2_29 = models.CharField(max_length=10,null=True)
	M2_30 = models.CharField(max_length=10,null=True)
	M2_31 = models.CharField(max_length=10,null=True)

	M3_01 = models.CharField(max_length=10,null=True)
	M3_02 = models.CharField(max_length=10,null=True)
	M3_03 = models.CharField(max_length=10,null=True)
	M3_04 = models.CharField(max_length=10,null=True)
	M3_05 = models.CharField(max_length=10,null=True)
	M3_06 = models.CharField(max_length=10,null=True)
	M3_07 = models.CharField(max_length=10,null=True)
	M3_08 = models.CharField(max_length=10,null=True)
	M3_09 = models.CharField(max_length=10,null=True)
	M3_10 = models.CharField(max_length=10,null=True)
	M3_11 = models.CharField(max_length=10,null=True)
	M3_12 = models.CharField(max_length=10,null=True)
	M3_13 = models.CharField(max_length=10,null=True)
	M3_14 = models.CharField(max_length=10,null=True)
	M3_15 = models.CharField(max_length=10,null=True)
	M3_16 = models.CharField(max_length=10,null=True)
	M3_17 = models.CharField(max_length=10,null=True)
	M3_18 = models.CharField(max_length=10,null=True)
	M3_19 = models.CharField(max_length=10,null=True)
	M3_20 = models.CharField(max_length=10,null=True)
	M3_21 = models.CharField(max_length=10,null=True)
	M3_22 = models.CharField(max_length=10,null=True)
	M3_23 = models.CharField(max_length=10,null=True)
	M3_24 = models.CharField(max_length=10,null=True)
	M3_25 = models.CharField(max_length=10,null=True)
	M3_26 = models.CharField(max_length=10,null=True)
	M3_27 = models.CharField(max_length=10,null=True)
	M3_28 = models.CharField(max_length=10,null=True)
	M3_29 = models.CharField(max_length=10,null=True)
	M3_30 = models.CharField(max_length=10,null=True)
	M3_31 = models.CharField(max_length=10,null=True)

	M4_01 = models.CharField(max_length=10,null=True)
	M4_02 = models.CharField(max_length=10,null=True)
	M4_03 = models.CharField(max_length=10,null=True)
	M4_04 = models.CharField(max_length=10,null=True)
	M4_05 = models.CharField(max_length=10,null=True)
	M4_06 = models.CharField(max_length=10,null=True)
	M4_07 = models.CharField(max_length=10,null=True)
	M4_08 = models.CharField(max_length=10,null=True)
	M4_09 = models.CharField(max_length=10,null=True)
	M4_10 = models.CharField(max_length=10,null=True)
	M4_11 = models.CharField(max_length=10,null=True)
	M4_12 = models.CharField(max_length=10,null=True)
	M4_13 = models.CharField(max_length=10,null=True)
	M4_14 = models.CharField(max_length=10,null=True)
	M4_15 = models.CharField(max_length=10,null=True)
	M4_16 = models.CharField(max_length=10,null=True)
	M4_17 = models.CharField(max_length=10,null=True)
	M4_18 = models.CharField(max_length=10,null=True)
	M4_19 = models.CharField(max_length=10,null=True)
	M4_20 = models.CharField(max_length=10,null=True)
	M4_21 = models.CharField(max_length=10,null=True)
	M4_22 = models.CharField(max_length=10,null=True)
	M4_23 = models.CharField(max_length=10,null=True)
	M4_24 = models.CharField(max_length=10,null=True)
	M4_25 = models.CharField(max_length=10,null=True)
	M4_26 = models.CharField(max_length=10,null=True)
	M4_27 = models.CharField(max_length=10,null=True)
	M4_28 = models.CharField(max_length=10,null=True)
	M4_29 = models.CharField(max_length=10,null=True)
	M4_30 = models.CharField(max_length=10,null=True)
	M4_31 = models.CharField(max_length=10,null=True)

	M5_01 = models.CharField(max_length=10,null=True)
	M5_02 = models.CharField(max_length=10,null=True)
	M5_03 = models.CharField(max_length=10,null=True)
	M5_04 = models.CharField(max_length=10,null=True)
	M5_05 = models.CharField(max_length=10,null=True)
	M5_06 = models.CharField(max_length=10,null=True)
	M5_07 = models.CharField(max_length=10,null=True)
	M5_08 = models.CharField(max_length=10,null=True)
	M5_09 = models.CharField(max_length=10,null=True)
	M5_10 = models.CharField(max_length=10,null=True)
	M5_11 = models.CharField(max_length=10,null=True)
	M5_12 = models.CharField(max_length=10,null=True)
	M5_13 = models.CharField(max_length=10,null=True)
	M5_14 = models.CharField(max_length=10,null=True)
	M5_15 = models.CharField(max_length=10,null=True)
	M5_16 = models.CharField(max_length=10,null=True)
	M5_17 = models.CharField(max_length=10,null=True)
	M5_18 = models.CharField(max_length=10,null=True)
	M5_19 = models.CharField(max_length=10,null=True)
	M5_20 = models.CharField(max_length=10,null=True)
	M5_21 = models.CharField(max_length=10,null=True)
	M5_22 = models.CharField(max_length=10,null=True)
	M5_23 = models.CharField(max_length=10,null=True)
	M5_24 = models.CharField(max_length=10,null=True)
	M5_25 = models.CharField(max_length=10,null=True)
	M5_26 = models.CharField(max_length=10,null=True)
	M5_27 = models.CharField(max_length=10,null=True)
	M5_28 = models.CharField(max_length=10,null=True)
	M5_29 = models.CharField(max_length=10,null=True)
	M5_30 = models.CharField(max_length=10,null=True)
	M5_31 = models.CharField(max_length=10,null=True)
	count = models.IntegerField(null=True)
	

	def function3(count,sid,cid):
		cur = connection.cursor()   
        # execute the stored procedure passing in   
        # search_string as a parameter  
		cur.callproc('pro3',[count,sid,cid,])  
        # grab the results  
		results = cur.fetchall()  
		"""l=[]
		for i in results:
			l.append(list(i))"""
		cur.close() 
	

class Achievements(models.Model):
	Student_Id = models.ForeignKey(Student,on_delete=models.CASCADE)
	Student_Achievement = models.CharField(max_length=100)

class Credentials(models.Model):
	User_Id = models.CharField(max_length=100)
	First_Name = models.CharField(max_length=45)
	Middle_Name = models.CharField(max_length=45)
	Last_Name = models.CharField(max_length=45)
	Password = models.CharField(max_length=20)
	Confirm_Password = models.CharField(max_length=20)

class Faculty(models.Model):
	Facultycourse_Id = models.IntegerField(primary_key=True,default=1)
	Faculty_Id = models.CharField(max_length=20)
	Academic_Course_Id = models.ForeignKey(Academic_Course,on_delete=models.CASCADE,default='C1')
	Status = models.CharField(max_length=100,null=True)
	Faculty_Name = models.CharField(max_length=100,null=True)

	def function2(u):
		cur = connection.cursor()   
        # execute the stored procedure passing in   
        # search_string as a parameter  
		cur.callproc('pro2',[u,])  
        # grab the results  
		results = cur.fetchall()  
		l=[]
		for i in results:
			l.append(list(i))
		cur.close() 
	
class Gradeschema(models.Model):
	Facultycourse_Id = models.ForeignKey(Faculty,on_delete=models.CASCADE,default=1)
	A = models.CharField(max_length=10)
	A2 = models.CharField(max_length=10)
	B = models.CharField(max_length=10)
	B2 = models.CharField(max_length=10)
	C = models.CharField(max_length=10)
	C2 = models.CharField(max_length=10)
	D = models.CharField(max_length=10)
	Semester = models.CharField(max_length=10,null=True)

class Gradeweightage(models.Model):
	Facultycourse_Id = models.ForeignKey(Faculty,on_delete=models.CASCADE,default=1)
	Exam_Type = models.CharField(max_length=20,null=True)
	tmarks = models.DecimalField(max_digits=10,decimal_places=2,null=True)
	wmarks = models.DecimalField(max_digits=10,decimal_places=2,null=True)	
	Semester = models.CharField(max_length=10,null=True)

class Academic_score(models.Model):
	Student_Id = models.ForeignKey(Student,on_delete=models.CASCADE)
	Academic_Course_Id = models.ForeignKey(Academic_Course,on_delete=models.CASCADE,default='C1')
	Exam_Type = models.CharField(max_length=20)
	Marks = models.DecimalField(max_digits=10,decimal_places=2,null=True)
	Marks_perc = models.DecimalField(max_digits=10,decimal_places=2,null=True)
	Facultycourse_Id = models.ForeignKey(Faculty,on_delete=models.CASCADE,default=1)
	Semester = models.CharField(max_length=10,null=True)
	#course = models.CharField(max_length=10,null=True)

	def function(q,s):  
		# create a cursor  
		cur = connection.cursor()   
        # execute the stored procedure passing in   
        # search_string as a parameter  
		cur.callproc('display',[q,s,])  
        # grab the results  
		results = cur.fetchall()  
		l=[]
		for i in results:
			l.append(list(i))
		cur.close()  
  
        # wrap the results up into Document domain objects   
		return l
	def function1():
		cur = connection.cursor()  
		cur.callproc('pro1')
		results = cur.fetchall()  
		l=[]
		for i in results:
			l.append(list(i))
		cur.close()  
  
        # wrap the results up into Document domain objects   
		return l  


class Club(models.Model):
	Student_Id = models.ForeignKey(Student,on_delete=models.CASCADE)
	Club_name = models.CharField(max_length=100)
	session1 = models.CharField(max_length=200,null=True)
	session2 = models.CharField(max_length=10,null=True)
	session3 = models.CharField(max_length=10,null=True)
	session4 = models.CharField(max_length=10,null=True)
	session5 = models.CharField(max_length=10,null=True)
	session6 = models.CharField(max_length=10,null=True)
	session7 = models.CharField(max_length=10,null=True)
	session8 = models.CharField(max_length=10,null=True)
	session9 = models.CharField(max_length=10,null=True)
	session10 = models.CharField(max_length=10,null=True)
	session11 = models.CharField(max_length=10,null=True)
	session12 = models.CharField(max_length=10,null=True)


