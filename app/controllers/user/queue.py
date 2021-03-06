from app.allImports import *
from app.logic.validation import *
from app.logic.data_validation import *

@app.route('/', methods=["GET","POST"])
def queue():
    user = require_login()
    #Create the class objects
    form_obj      = FormQueries()
    staff_obj     = StaffAssignedQueries()
    data_val_obj  = DataValidation()
    requestor_obj = RequestorQueries()
    
    #find incomplete forms
    forms = form_obj.select_all_incomplete()
    
    
    #find the staff assigned for those incomplete forms
    staffDict = data_val_obj.create_staff_assigned_dict(forms,staff_obj)
    
    #find the requestors for those incomplete forms
    requestorDict = data_val_obj.create_requestors_dict(forms,requestor_obj)
    
    if user.is_admin != True:
        # finds the requestors that are under the user.
        requestorDict = data_val_obj.create_user_dict(forms, requestor_obj, user.username)
        #creates an empty list to store the user's FID numbers in
        userFIDList = []
        #get user's FID number from dict.
        for key, value in requestorDict.iteritems():
            userFIDList.append(key)
        # finds the forms that match with the users FID numbers. 
        forms = form_obj.select_from_list(userFIDList)
    

    return render_template('views/queue.html', 
                        cfg             = cfg, 
                        forms           = forms, 
                        staffDict       = staffDict, 
                        requestorDict   = requestorDict, 
                        user            = user)
  