import smtplib 

sender = "rahul.kumarrkr95@gmail.com"
sender_password = "Rahulrkr1996#"
receivers = ["rahul.kumarrkr96@gmail.com"]  

def getRescheduleBKMessage(bk_id,sender,receiver,identifier):
	text = "From: Yo Tours <"+sender+">\n" 
	text += "To: To Person <"+ receiver +">\n"
	text += "MIME-Version: 1.0\n"
	text += "Content-type: text/html\n"

	text += "Subject: Booking Rescheduled !\n\n"
	if identifier=="customer":
		text += "This is to inform you that your Booking " + bk_id + " on " + bk_id + " is Rescheduled to " + bk_id + "!\n"
	elif identifier=="storyteller":
		text += "This is to inform you that the Booking " + bk_id + " on " + bk_id + " is rescheduled and you have been unallotted !\n"
	return text
def getCancellBKMessage(bk_id,sender,receiver,identifier):
	text = "From: Yo Tours <"+sender+">\n" 
	text += "To: To Person <"+ receiver +">\n"
	text += "MIME-Version: 1.0\n"
	text += "Content-type: text/html\n"

	text += "Subject: Booking Cancelled !\n\n"
	if identifier=="customer":
		text += "This is to inform you that your Booking " + bk_id + " on " + bk_id + " is Cancelled !\n"
	elif identifier=="storyteller":
		text += "This is to inform you that the Booking " + bk_id + " on " + bk_id + " is cancelled and you have been unallotted !\n"
	return text
def getSTAllocationMessage(bk_id,sender,receiver,identifier):
	text = "From: Yo Tours <"+sender+">\n" 
	text += "To: To Person <"+ receiver +">\n"
	text += "MIME-Version: 1.0\n"
	text += "Content-type: text/html\n"

	if identifier=="customer":
		text += "Subject: Storyteller Allotted !\n\n"
		text += "This is to inform that the storyteller for your Booking " + bk_id + " on " + bk_id + " is changed to  " + bk_id + " ...\n"
	elif identifier=="st_old":
		text += "Subject: Storyteller Changed !\n\n"
		text += "This is to inform that you have been unallotted from the Booking " + bk_id + " on " + bk_id + " !\n"
	elif identifier=="st_new":
		text += "Subject: Storyteller Changed !\n\n"
		text += "This is to inform that you have been allotted to the Booking " + bk_id + " on " + bk_id + " !\n"
	
	return text
def getSaveBKMessage(bk_id,sender,receiver):
	text = "From: Yo Tours <"+sender+">\n" 
	text += "To: To Person <"+ receiver +">\n"
	text += "MIME-Version: 1.0\n"
	text += "Content-type: text/html\n"

	text += "Subject: Booking Saved !\n\n"
	text += "This is to inform you that your Booking " + bk_id + " on " + bk_id + " is saved and will soon be allotted to a storyteller !!\n"
	return text


def sendmail(sender,sender_password,receivers,message):	
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login(sender, sender_password) 
	  
	try:
		s.sendmail(sender, receivers, message)         
		print "Successfully sent email"
	except :
	   print "Error: unable to send email!"

	s.quit() 

		
message = getSaveBKMessage("1",sender,receivers[0])		
sendmail(sender,sender_password,receivers,message)

message = getCancellBKMessage("1",sender,receivers[0],"customer")		
sendmail(sender,sender_password,receivers,message)
message = getSTAllocationMessage("1",sender,receivers[0],"customer")		
sendmail(sender,sender_password,receivers,message)
message = getRescheduleBKMessage("1",sender,receivers[0],"customer")		
sendmail(sender,sender_password,receivers,message)

message = getCancellBKMessage("1",sender,receivers[0],"storyteller")		
sendmail(sender,sender_password,receivers,message)
message = getRescheduleBKMessage("1",sender,receivers[0],"storyteller")		
sendmail(sender,sender_password,receivers,message)
message = getSTAllocationMessage("1",sender,receivers[0],"st_new")		
sendmail(sender,sender_password,receivers,message)
message = getSTAllocationMessage("1",sender,receivers[0],"st_old")		
sendmail(sender,sender_password,receivers,message)
