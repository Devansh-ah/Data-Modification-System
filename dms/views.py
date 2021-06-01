from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import *
from dms.models import *
from dms import app
import subprocess
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from django.contrib.auth.models import User, auth


def index(request):
    return render(request, 'dms/index.html')


def registration(request):
    if request.method == 'POST':
        aadhar = int(request.POST.get("aadhar"))
        password = request.POST.get("password")
        re_pass = request.POST.get("re-pass")
        fp = request.FILES.get("fingerprint")
        Aadhar_data = Aadhar.objects.all()
        signup_data = user.objects.all()

        all_accounts = signup_data.values_list()
        aadhar_numbers_available = [i[1] for i in all_accounts]
        if aadhar in aadhar_numbers_available:
            messages.error(request, "Aadhar Number already exists...")
            return redirect("registration")
        if password == re_pass:
            data = Aadhar_data.values_list()
            aadhar_numbers = [i[0] for i in data]
            f = 0
            for i, x in enumerate(aadhar_numbers):
                if aadhar == x:
                    y1 = "./images/" + data[i][-1]
                    f = 1
                    break
            if f == 0:
                messages.error(
                    request, "Aadhar Number not found... Go to the nearest SevaSadan and apply for new Aadhar...")
                return redirect("index")
            ins = signup(Aadhar_Number=aadhar, fp_User=fp)
            ins.save()
            signup_data = signup.objects.using('system').all()
            data = signup_data.values_list()
            aadhar_numbers = [i[1] for i in data]
            for i, x in enumerate(aadhar_numbers):
                if aadhar == x:
                    y2 = "./images/" + data[i][-1]

            command = "python ./dms/finger_match.py "+y1+" "+y2
            finger_match_output = subprocess.check_output(
                ['python', './dms/finger_match.py', y1, y2])
            finger_match_output = str(finger_match_output).strip()
            finger_match_output = finger_match_output[2:]
            finger_match_output = finger_match_output[:len(
                finger_match_output)-5]
            if finger_match_output == "Fingerprint matches":
                new_user = User.objects.create_user(
                    username=aadhar, password=password)
                messages.error(request, "Account Created Successfully...")
                return redirect("login")
            else:
                messages.error(
                    request, "Fingerprint did not match with actual fingerprint... \
                        Please try again with another fingerprint...")
                return redirect("registration")
        else:
            messages.error(request, "Passwords do not match...")
            return redirect("registration")
    else:
        return render(request, 'dms/registration.html')


def login(request):
    if request.method == 'POST':
        aadhar = int(request.POST.get("AadharNo"))
        password = request.POST.get("password")
        user = auth.authenticate(username=aadhar, password=password)
        # login_data=userlogin.objects.using('system').all()
        # data=login_data.values_list()
        #aadhar_numbers = [i[1] for i in data]
        #passw = [i[2] for i in data]
        # for x in aadhar_numbers:
        #   if x==aadhar:
        #       for y in passw:
        #          if y==password:
        #             messages.info(request,"You are successfully logged in.")
        #            return redirect("index")
        # else:
        #   messages.info(request,"Invalid details, Please try again!")
        #  return redirect("login")
        if user is not None:
            auth.login(request, user)
            messages.info(request, "Logged in Successfully...")
            return redirect('index')
        else:
            messages.info(request, "Invalid user info")
            return redirect('login')
    else:
        return render(request, 'dms/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def aadhar(request):
    if request.user.is_authenticated:
        return render(request, 'dms/aadhar.html')
    else:
        messages.info(request, "Please log in first.")
        return redirect('login')


def aadhar1(request):
    if request.method == 'POST':
        fName = request.POST.get("first_name")
        mName = request.POST.get("middle_name")
        lName = request.POST.get("last_name")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        street = request.POST.get("street")
        city = request.POST.get("city")
        address_proof = request.FILES.get("address_proof")
        pincode = request.POST.get("pincode")
        dob = request.POST.get("dob")
        birth_proof = request.FILES.get("birth_proof")

        print("Address Proof: ", address_proof)
        print("Birth Proof: ", birth_proof)

        Aadhar_data = Aadhar.objects.all()
        data = Aadhar_data.values_list()
        row = -1
        fnames = [i[2] for i in data]
        mnames = [i[3] for i in data]
        lnames = [i[4] for i in data]
        DOBdb = [i[7] for i in data]
        sex = [i[6] for i in data]
        contacts = [i[8] for i in data]
        streetdb = [i[12] for i in data]
        citydb = [i[13] for i in data]
        pincodedb = [i[14] for i in data]
        # aadhar_nums = [i[]]

        for fname in fnames:
            row = row+1
            if fname == fName:
                if lnames[row] == lName:
                    if mnames[row] == mName:
                        if streetdb[row] == street:
                            if citydb[row] == city:
                                if int(pincodedb[row]) == int(pincode):
                                    if sex[row] == gender:
                                        if int(contacts[row]) == int(phone):
                                            messages.info(
                                                request, "No changes detected.")
                                            return redirect("aadhar1")
                                        else:
                                            break
        ins = aadharQ(FirstName=fName, MidName=mName, LastName=lName, DOB=dob,
                      Mobile_Number=phone, Sex=gender, Street=street, city=city, address_proof=address_proof, pincode=pincode, birth_proof=birth_proof, AadharNo=int(request.user.username))
        ins.save()
        messages.info(
            request, "Your application is sent successfully.")
        return redirect('/')
    else:
        aadhar = Aadhar.objects.all()
        return render(request, 'dms/aadhar1.html', {'aadhar': aadhar})


def pan(request):
    if request.user.is_authenticated:
        return render(request, 'dms/pan.html')
    else:
        messages.info(request, "Please log in first.")
        return redirect('login')


def pan1(request):
    if request.method == 'POST':
        fName = request.POST.get("first_name")
        mName = request.POST.get("middle_name")
        lName = request.POST.get("last_name")
        dob = request.POST.get("dob")
        pan_data = PanCard.objects.all()
        data = pan_data.values_list()
        row = -1
        fnames = [i[3] for i in data]
        mnames = [i[4] for i in data]
        lnames = [i[5] for i in data]
        for fname in fnames:
            row = row+1
            if fname == fName:
                if lnames[row] == lName:
                    if mnames[row] == mName:
                        messages.info(request, "No changes detected.")
                        return redirect("pan1")
        else:
            ins = pancardQ(FirstName=fName, MidName=mName,
                           LastName=lName, DOB=dob)
            ins.save()
            messages.info(request, "Your application is sent successfully.")
            return redirect('/')
    else:
        aadhar = PanCard.objects.all()
        return render(request, 'dms/pan1.html', {'aadhar': aadhar})


def licence(request):
    if request.user.is_authenticated:
        return render(request, 'dms/licence.html')
    else:
        messages.info(request, "Please log in first.")
        return redirect('login')


def licence1(request):
    if request.method == 'POST':
        fName = request.POST.get("first_name")
        mName = request.POST.get("middle_name")
        lName = request.POST.get("last_name")
        phone = request.POST.get("phone")
        street = request.POST.get("street")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        dob = request.POST.get("dob")
        licence_data = DrivingLicence.objects.all()
        data = licence_data.values_list()
        row = -1
        fnames = [i[8] for i in data]
        mnames = [i[9] for i in data]
        lnames = [i[10] for i in data]
        contacts = [i[6] for i in data]
        streetdb = [i[13] for i in data]
        citydb = [i[14] for i in data]
        pincodedb = [i[15] for i in data]
        for fname in fnames:
            row = row+1
            if fname == fName:
                if lnames[row] == lName:
                    if mnames[row] == mName:
                        if streetdb[row] == street:
                            if citydb[row] == city:
                                if int(pincodedb[row]) == int(pincode):
                                    if int(contacts[row]) == int(phone):
                                        messages.info(
                                            request, "No changes detected.")
                                        return redirect("licence1")
        else:
            ins = licenceQ(FirstName=fName, MidName=mName, LastName=lName, DOB=dob,
                           Mobile_NUmber=phone, Street=street, city=city, pincode=pincode)
            ins.save()
            messages.info(request, "Your application is sent successfully.")
            return redirect('/')
    else:
        dl = DrivingLicence.objects.all()
        return render(request, 'dms/licence1.html', {'aadhar': dl})


def ration(request):
    if request.user.is_authenticated:
        return render(request, 'dms/ration.html')
    else:
        messages.info(request, "Please log in first.")
        return redirect('login')


def ration1(request):
    if request.method == 'POST':
        fName = request.POST.get("first_name")
        mName = request.POST.get("middle_name")
        lName = request.POST.get("last_name")
        street = request.POST.get("street")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        hof_name = request.POST.get("hof_name")
        hof_relation = request.POST.get("hof_relation")
        fh = request.POST.get("fh")
        fh_name = request.POST.get("fh_name")
        dob = request.POST.get("dob")
        Aadhar_data = Ration.objects.all()
        data = Aadhar_data.values_list()
        row = -1
        fnames = [i[3] for i in data]
        mnames = [i[4] for i in data]
        lnames = [i[5] for i in data]
        hof_namedb = [i[6] for i in data]
        hof_relationdb = [i[7] for i in data]
        fhdb = [i[8] for i in data]
        fh_namedb = [i[9] for i in data]
        streetdb = [i[11] for i in data]
        citydb = [i[12] for i in data]
        pincodedb = [i[13] for i in data]
        for fname in fnames:
            row = row+1
            if fname == fName:
                if lnames[row] == lName:
                    if mnames[row] == mName:
                        if streetdb[row] == street:
                            if citydb[row] == city:
                                if int(pincodedb[row]) == int(pincode):
                                    if str(fhdb[row]) == str(fh):
                                        if fh_namedb[row] == fh_name:
                                            if hof_namedb[row] == hof_name:
                                                if hof_relationdb[row] == hof_relation:
                                                    messages.info(
                                                        request, "No changes detected.")
                                                    return redirect("ration1")
        else:
            ins = RationQ(FirstName=fName, MidName=mName, LastName=lName, DOB=dob, HOF_name=hof_name, HOF_relation=hof_relation,
                          Father_or_Husband=fh, name_F_or_H=fh_name, Street=street, city=city, pincode=pincode)
            ins.save()
            messages.info(request, "Your application is sent successfully.")
            return redirect('/')
    else:
        aadhar = Ration.objects.all()
        return render(request, 'dms/ration1.html', {'aadhar': aadhar})


def voterid(request):
    if request.user.is_authenticated:
        return render(request, 'dms/voterid.html')
    else:
        messages.info(request, "Please log in first.")
        return redirect('login')


def voterid1(request):
    if request.method == 'POST':
        fName = request.POST.get("first_name")
        mName = request.POST.get("middle_name")
        lName = request.POST.get("last_name")
        dob = request.POST.get("dob")
        father = request.POST.get("FathersName")
        gender = request.POST.get("gender")
        street = request.POST.get("street")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        vid = VoterId.objects.all()
        data = vid.values_list()
        row = -1
        fnames = [i[4] for i in data]
        lnames = [i[6] for i in data]
        mnames = [i[5] for i in data]
        fatherdb = [i[7] for i in data]
        sex = [i[9] for i in data]
        streetdb = [i[10] for i in data]
        citydb = [i[11] for i in data]
        pincodedb = [i[12] for i in data]
        for fname in fnames:
            row = row+1
            if fname == fName:
                if lnames[row] == lName:
                    if mnames[row] == mName:
                        if streetdb[row] == street:
                            if citydb[row] == city:
                                if int(pincodedb[row]) == int(pincode):
                                    if sex[row] == gender:
                                        if fatherdb[row] == father:
                                            messages.info(
                                                request, "No changes detected.")
                                            return redirect("voterid1")
        else:
            ins = voteridQ(FirstName=fName, MidName=mName, LastName=lName, DOB=dob,
                           FathersName=father, Sex=gender, Street=street, city=city, pincode=pincode)
            ins.save()
            messages.info(request, "Your application is sent successfully.")
            return redirect('/')
    else:
        aadhar = VoterId.objects.all()
        return render(request, 'dms/voterid1.html', {'aadhar': aadhar})


def display_aadhar(request):
    aadhar = Aadhar.objects.all()
    #data = aadhar.values_list()
    #aadhar_numbers = [i[0] for i in data]
    # print(aadhar_numbers)
    # aadharindex=aadhar_numbers.index(int(request.user.username))
    # img=data[aadharindex][1]
    # img="../../../"+img
    return render(request, 'dms/display_aadhar.html', {'aadhar': aadhar})


def display_pancard(request):
    aadhar = PanCard.objects.all()
    return render(request, 'dms/display_pancard.html', {'aadhar': aadhar})


def display_voterid(request):
    aadhar = VoterId.objects.all()
    return render(request, 'dms/display_voterid.html', {'aadhar': aadhar})


def display_licence(request):
    aadhar = DrivingLicence.objects.all()
    return render(request, 'dms/display_licence.html', {'aadhar': aadhar})


def display_ration(request):
    aadhar = Ration.objects.all()
    return render(request, 'dms/display_ration.html', {'aadhar': aadhar})


def adminLogin(request):
    if request.method == 'POST':
        empid = request.POST.get("EmpId")
        password = request.POST.get("password")
        fp = request.FILES.get("finger")
        user = auth.authenticate(username=empid, password=password)

        data = AdminInfo.objects.all().values_list()
        EmpIds = [i[1] for i in data]
        for i, x in enumerate(EmpIds):
            if empid == x:
                y1 = "./images/" + data[i][-1]
                break

        ins = signup1(EmpId=empid, fp_User=fp)
        ins.save()
        signup_data = signup1.objects.using('system').all()
        data = signup_data.values_list()
        empids = [i[1] for i in data]
        for i, x in enumerate(empids):
            if empid == x:
                y2 = "./images/" + data[i][-1]
        #command = "python ./dms/finger_match.py "+y1+" "+fp
        finger_match_output = subprocess.check_output(
            ['python', './dms/finger_match.py', y1, y2])
        finger_match_output = str(finger_match_output).strip()
        finger_match_output = finger_match_output[2:]
        finger_match_output = finger_match_output[:len(finger_match_output)-5]

        if finger_match_output == "Fingerprint matches":
            if user is not None:
                auth.login(request, user)
                messages.info(request, "Logged in Successfully...")
                return redirect('dashboard')

        else:
            messages.info(request, "Invalid user info")
            return redirect('adminLogin')
    else:
        return render(request, 'dms/adminLogin.html')


def adminSignup(request):
    if request.method == 'POST':
        EmpId = request.POST.get("EmpId")
        password = request.POST.get("password")
        re_pass = request.POST.get("re_pass")
        fp = request.FILES.get("finger")
        data = AdminInfo.objects.all().values_list()
        EmpIds = [i[1] for i in data]

        signup_data = user.objects.all()
        all_accounts = signup_data.values_list()
        empids_available = [i[1] for i in all_accounts]
        if EmpId in empids_available:
            messages.error(request, "Employee id already exists...")
            return redirect("adminSignup")

        if password == re_pass:
            f = 0
            for i, x in enumerate(EmpIds):
                if EmpId == x:
                    y1 = "./images/" + data[i][-1]
                    f = 1
                    break
            if f == 0:
                messages.error(
                    request, "Employee id not found...")
                return redirect("index")
            ins = signup1(EmpId=EmpId, fp_User=fp)
            ins.save()
            signup_data = signup1.objects.using('system').all()
            data = signup_data.values_list()
            empids = [i[1] for i in data]
            for i, x in enumerate(empids):
                if EmpId == x:
                    y2 = "./images/" + data[i][-1]

            command = "python ./dms/finger_match.py "+y1+" "+y2
            finger_match_output = subprocess.check_output(
                ['python', './dms/finger_match.py', y1, y2])
            finger_match_output = str(finger_match_output).strip()
            finger_match_output = finger_match_output[2:]
            finger_match_output = finger_match_output[:len(
                finger_match_output)-5]
            if finger_match_output == "Fingerprint matches":
                new_user = User.objects.create_user(
                    is_staff=True, username=EmpId, password=password)
                messages.error(request, "Account Created Successfully...")
                return redirect("adminLogin")
            else:
                messages.error(
                    request, "Fingerprint did not match with actual fingerprint...Please try again with another fingerprint...")
                return redirect("adminSignup")
        else:
            messages.error(request, "Passwords do not match...")
            return redirect("registration")

        # if EmpId in EmpIds:
         #   if password==re_pass:
          #      new_user = User.objects.create_user(is_staff=True,username=EmpId, password=password)
           #     messages.error(request, "Account Created Successfully...")
            #    return redirect("adminLogin")
        # else:
         #   messages.error(request, "Invalid information...try again")
          #  return redirect("adminSignup")
    else:
        return render(request, 'dms/adminSignup.html')


# def dashboard(request):
#     if request.user.is_authenticated:
#         return render(request, 'dms/dashboard.html')
#     else:
#         messages.info(request, "Please log in first.")
#         return redirect('adminLogin')


def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            all_queries = aadharQ.objects.using("system").all().values_list()
            data = {}
            for i in all_queries:
                data[i[1]] = str(request.build_absolute_uri()) + \
                    "/change/"+str(i[1])

            # print("Path: ", str(request.build_absolute_uri()))
            return render(request, "dms/dashboard.html", {"all_queries": data})
        else:
            messages.error(
                request, "You Do not have rights to access this page...")
            return redirect("/")
    else:
        messages.info(request, "Please log in first.")
        return redirect('adminLogin')


def doc_verification(request, user):

    all_queries = aadharQ.objects.all()
    f = 0
    data = []
    whole_data = list(aadharQ.objects.all().values_list())

    metadata = aadharQ._meta.get_fields()
    col_names = []
    # print(whole_data)
    for i in range(len(metadata)):
        col_names.append(str(list(metadata)[i]).split(".")[-1])
    col_names = col_names[1:]

    for k, i in enumerate(all_queries):
        # print(i.address_proof)
        if str(i.AadharNo) == str(user):
            whole_data = whole_data[k]
            data = i
            f = 1
    aadhar_data = Aadhar.objects.all().values_list()

    aadhar_data_user = []
    for i in aadhar_data:

        if str(i[0]) == str(user):
            aadhar_data_user = list(i)
    # print("aadhar data user: ", aadhar_data_user)

    metadata_aadhar = Aadhar._meta.get_fields()
    col_names_aadhar = []
    for i in range(len(metadata_aadhar)):
        col_names_aadhar.append(str(list(metadata_aadhar)[i]).split(".")[-1])
    col_names_aadhar = col_names_aadhar[5:]
    # print("colums_aadhar: ", col_names_aadhar)

    whole_data = list(whole_data)[1:]
    if f == 0:
        messages.error(request, "Query not found...")
        return redirect("dashboard")
    else:
        context = {"zipped_values": zip(
            col_names, whole_data), "data": data, "col_names": col_names, "aadhar_details": zip(col_names_aadhar, aadhar_data_user), "aadhar_data": aadhar_data_user}
        return render(request, "dms/verify_details.html", context)


def aorr(request):
    col_names = request.POST.get("col_names").split(",")
    # print("Col names: ", col_names[0])
    user_aadhar = int(col_names[0])
    print(user_aadhar)
    cols = []
    vals = []
    data = {}

    for i, j in request.POST.items():
        if "field_" in i:
            cols.append(i[6:])
            vals.append(j)
            data[i[6:]] = j

    # print("Columns: ", cols)
    # print("Values: ", vals)

    ins = aadhar_status(Actual_AadharNo=user_aadhar, AadharNo=data["AadharNo"], FirstName=data["FirstName"], MidName=data["MidName"], LastName=data["LastName"], Street=data[
        "Street"], city=data["city"], pincode=data["pincode"], address_proof=data["address_proof"], Sex=data['Sex'], Mobile_Number=data["Mobile_Number"], DOB=data["DOB"], birth_proof=data["birth_proof"])
    ins.save()

    zipped_values = zip(cols, vals)
    return render(request, "dms/aorr.html", {"zipped_values": zipped_values, "user_aadhar": user_aadhar})


def aadhar_query_status(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please Login First...")
        return redirect("login")

    all_queries_queries = aadharQ.objects.all().values_list()
    all_queries = aadhar_status.objects.all().values_list()
    col_names_metadata = aadhar_status._meta.get_fields()
    col_names = []

    if(len(all_queries) == 0):
        return render(request, 'dms/aadhar_status.html', {"entries": "No application found!"})
    # print("Aadhar_status: ", all_queries)
    # print("All queries: ", all_queries_queries)
    all_queries_aadhars = []
    for i in all_queries:
        all_queries_aadhars.append(i[1])

    id_to_remove_query = -1
    current_query = 0
    for i in all_queries_queries:
        if str(i[1]) == str(request.user):
            if i[1] not in all_queries_aadhars:
                messages.error(request, "Your Query is under process...")
                return redirect("index")
            else:
                id_to_remove_query = i[0]
                current_query = i[1:]

    for i in range(1, len(col_names_metadata)):
        col_names.append(str(list(col_names_metadata)[i]).split(".")[-1])

    # print("Col_Names: ", col_names)
    status_values = []
    id_to_remove_status_query = -1
    for i in all_queries:
        if str(i[1]) == str(request.user):
            id_to_remove_status_query = list(i)[0]
            status_values = list(i)[1:]
    # print("Id to be removed from query: ", id_to_remove_query)
    # print("Id to be removed from status: ", id_to_remove_status_query)

    if id_to_remove_query == -1 or id_to_remove_status_query == -1:
        return render(request, 'dms/aadhar_status.html', {"entries": "No application found!"})

    f = 0
    status_values[0] = str(status_values[0])
    for i in range(1, len(status_values)):
        status_values[i] += "ed"
    for i in status_values:
        if i == "reject":
            f = 1
            break

    # check if query accepted or rejected
    # f = 0 means accepted, f = 1 means rejected
    # if f==0:
    active_user = int(str(request.user))

    aadhar_all_objects = Aadhar.objects.all().values_list()

    # get the object of the aadhar number for which details are to be changed
    aadhar_to_be_updated = Aadhar.objects.get(Aadhar_Number=active_user)

    for i in aadhar_all_objects:
        if i[0] == active_user:
            # print("Matched: ", i)
            # print("Query: ", current_query)

            current_query_fname = current_query[1]
            current_query_mname = current_query[2]
            current_query_lname = current_query[3]
            current_query_street = current_query[4]
            current_query_city = current_query[5]
            current_query_pincode = current_query[6]
            current_query_sex = current_query[8]
            current_query_mobile = current_query[9]

            # print("Current Query Fname: ", current_query_fname)

            aadhar_to_be_updated.fName = current_query_fname
            aadhar_to_be_updated.mName = current_query_mname
            aadhar_to_be_updated.lName = current_query_lname
            aadhar_to_be_updated.Street = current_query_street
            aadhar_to_be_updated.city = current_query_city
            aadhar_to_be_updated.pincode = current_query_pincode
            aadhar_to_be_updated.Sex = current_query_sex
            aadhar_to_be_updated.Mobile_NUmber = current_query_mobile

            aadhar_to_be_updated.save()
            # print("After updation: ", aadhar_to_be_updated)
            # print(aadhar_to_be_updated.fName)
            break

    zipped_values = zip(col_names, status_values)

    # remove the query from dms_aadharq
    temp = aadharQ.objects.filter(id=id_to_remove_query)
    temp.delete()

    # remove the status query from dms_aadhar_status
    temp = aadhar_status.objects.filter(id=id_to_remove_status_query)
    temp.delete()

    # print("Object: ", temp)
    return render(request, "dms/aadhar_status.html", {"zipped_values": zipped_values})
