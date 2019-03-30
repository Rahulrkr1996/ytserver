import smtplib 
  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login("rahul.kumarrkr95@gmail.com", "Rahulrkr1996#") 
  
# message to be sent 
message = "Message_you_need_to_send"
  
# sending the mail 
s.sendmail("rahul.kumarrkr95@gmail.com", "rahul.kumarrkr96@gmail.com", message) 
  
# terminating the session 
s.quit() 