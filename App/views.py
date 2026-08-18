from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import userProfile,Block,Policy,Notification
import hashlib
from solcx import compile_standard, install_solc
install_solc('0.8.0')
import json
# Create your views here.

with open("ContactList.sol", "r") as file:
        contact_list_file = file.read()

    #to save the output in a JSON file
    
compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"ContactList.sol": {"content": contact_list_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract 
                    }
                }
            },
        },
        solc_version="0.8.0",
    )
    # print(compiled_sol)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["ContactList.sol"]["ContactList"]["evm"]["bytecode"]["object"]
abi = json.loads(compiled_sol["contracts"]["ContactList.sol"]["ContactList"]["metadata"])["output"]["abi"]



from web3 import Web3
    
    # For connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
address = "0xF6A1fd15672f03b1821E55c197943f2773DBbD1b"
private_key = "0x087a0c65caf76b725423cbc9cc5677fdc305f1ee56d964e7dd9325360caf1439"  # leaving the private key like this is very insecure if you are working on real world project
    # Create the contract in Python
ContactList = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get the number of latest transaction
nonce = w3.eth.get_transaction_count(address)

transaction = ContactList.constructor().build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": address,
            "nonce": nonce,
        }
    )

GEMINI_API_KEY = "AIzaSyCgNfTeZZPTfEgAqV1NpgzALAHyOD7oYMw"  # Replace with your actual Gemini API key

def homepage(request):
    
    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()
        if not profile.is_an_insurance_company:
            notifications = Notification.objects.filter(user = request.user).order_by('-date')
        elif not profile.is_a_hospital:
            notifications = Notification.objects.filter(user = request.user).order_by('-date')
        else:
            notifications = Notification.objects.filter(user = request.user).order_by('-date')


    else:
        profile = ''
        notifications = []
    policies = Policy.objects.all()
    hospitals = userProfile.objects.filter(is_a_hospital = True)
    return render(request,'index.html',context = {'profile':profile,"notifications":notifications,"policies":policies,"hospitals":hospitals,"bills":Block.objects.filter(user =request.user.username).order_by('-date')})


message = 0
reg_error = 0

def checkname(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    
    u = User.objects.filter(username = username).first()
    
    if u == None:
        message = 0
    else:
        message = 1
    
    return JsonResponse({"message":message})


def checkSignup(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    
    u = User.objects.filter(username = username).first()
    
    if u == None:
        message = 0
    else:
        message = 1
    
    return JsonResponse({"message":message})

def checkipn(request):
    
    ipn = request.POST.get('ipn')
    # password = request.POST.get('password')



    
    u = Block.objects.filter(ipn = ipn).first()
    
    if u == None:
        message = 0
    else:
        message = 1
    
    return JsonResponse({"message":message})

def register(request):
    if request.method == 'POST':
        try:
            user = User.objects.create(username = request.POST.get('username'),email=request.POST.get('email'))
            user.set_password(request.POST.get('password'))
            user.save()
        except:
            pass

        user = User.objects.filter(username=request.POST.get('username')).first()
        
        profile = userProfile.objects.create(user=user)
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.save()
        
            

    return HttpResponseRedirect(reverse('homepage'))


def checkLogin(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username = username,password = password)
    if user:
        print(username)
        return JsonResponse({"message":0})
            
    else:
        print("No user found")
        return JsonResponse({"message":1})
        

def user_login(request):
   
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username = username,password = password)
        if user:

            if user.is_active:
                login(request, user)
                print("login success!!!")
                return HttpResponseRedirect(reverse('homepage'))
        else:
            
            print("No such user")


    return HttpResponseRedirect(reverse('homepage'))
    
@login_required
def user_logout(request):

    logout(request)


    return HttpResponseRedirect(reverse('homepage'))

def show_login(request):
    return render(request,'login.html')

def show_register(request):
    return render(request,'register.html')


def uploadBill(request):
    with open("ContactList.sol", "r") as file:
        contact_list_file = file.read()

    #to save the output in a JSON file
    
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"ContactList.sol": {"content": contact_list_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract 
                    }
                }
            },
        },
        solc_version="0.8.0",
    )
    # print(compiled_sol)
    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

    bytecode = compiled_sol["contracts"]["ContactList.sol"]["ContactList"]["evm"]["bytecode"]["object"]
    abi = json.loads(compiled_sol["contracts"]["ContactList.sol"]["ContactList"]["metadata"])["output"]["abi"]

    from web3 import Web3
   
    # For connecting to ganache
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    chain_id = 1337
    address = "0xF6A1fd15672f03b1821E55c197943f2773DBbD1b"
    private_key = "0x087a0c65caf76b725423cbc9cc5677fdc305f1ee56d964e7dd9325360caf1439" # leaving the private key like this is very insecure if you are working on real world project
    # Create the contract in Python
    ContactList = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get the number of latest transaction
    nonce = w3.eth.get_transaction_count(address)

    transaction = ContactList.constructor().build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": address,
            "nonce": nonce,
        }
    )
    # Sign the transaction
    sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Deploying Contract!")
    # Send the transaction
    transaction_hash = w3.eth.send_raw_transaction(sign_transaction.raw_transaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")
    block = Block.objects.create(ipn= request.POST.get("ins-policy"),transacion_address = str(transaction_receipt.contractAddress),user = request.POST.get('username'),ins = User.objects.filter(username = request.POST.get("prov-name")).first())

    contact_list = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)
    patientInfo = request.POST.get('name') + ";" + str(request.POST.get('address'))+ ";" + request.POST.get("dob")+ ";"+request.POST.get("ins-policy")
    providerInfo = request.POST.get("prov-name")+ ";"+request.POST.get("prov-address")+ ";"+ request.POST.get("prov-npi")
    service = request.POST.get("date-of-service")+ ";"+request.POST.get("service-desc")+ ";"+request.POST.get("service-code")+ ";"+request.POST.get("diagnosis-code")+ ";"+request.POST.get("charge")
    amount = request.POST.get("total-due")
    InsAmount = "0"

    # Generate fraud-detection hash from IPN, charge, total-due
    bill_hash_str = "|".join([
        request.POST.get('ins-policy', ''),
        request.POST.get('charge', ''),
        request.POST.get('total-due', ''),
    ])
    block.bill_hash = hashlib.sha256(bill_hash_str.encode()).hexdigest()
    block.save()

    store_contact = contact_list.functions.addContact(
        patientInfo,providerInfo,service,amount,InsAmount
        
    ).build_transaction({"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 1})

    # Sign the transaction
    sign_store_contact = w3.eth.account.sign_transaction(
        store_contact, private_key=private_key
    )
    # Send the transaction
    send_store_contact = w3.eth.send_raw_transaction(sign_store_contact.raw_transaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)

    print("saved!!!!!!!!!!!")
    return HttpResponseRedirect(reverse('homepage'))


def getBill(request):
    valid = 1
    
    block = Block.objects.filter(ipn = request.POST.get("bill")).first()
        # request.POST.get('university_name') + str(request.POST.get('date_issued'))+ request.POST.get("c_no")+request.POST.get("reg_no")+request.POST.get("student_name")+request.POST.get("faculty_of")+ request.POST.get("degree_of")+request.POST.get("degree_in")+str(request.POST.get("completed_in"))+ request.POST.get("comp_1")+request.POST.get("comp_2")+request.POST.get("class")+request.POST.get("grade")+request.POST.get("course_name") + str(p_block.current_hash)
        

    if block:
        test = w3.eth.contract(address=block.transacion_address, abi=abi)
        result = test.functions.retrieve().call()
        print("result", result)

        if not result:
            return JsonResponse({"found": 0, "error": "Block exists in database but no data found on chain. Ganache may have been restarted."})

        print("result[0]", result[0])
        found = 1
        print({"name":result[0][0].split(";")[0],"address":result[0][0].split(";")[1],"date":result[0][0].split(";")[2],"ipn":result[0][0].split(";")[3],"InsName":result[0][1].split(";")[0],"InsAdd":result[0][1].split(";")[1],"Npi":result[0][1].split(";")[2],"serviceDate":result[0][2].split(";")[0],"desc":result[0][2].split(";")[1],"pcode":result[0][2].split(";")[2],"dcode":result[0][2].split(";")[3],"charge":result[0][2].split(";")[4],"amount":result[0][3],"=====":result[0][4]})
        print(block.requested)
        return JsonResponse({"name":result[0][0].split(";")[0],"address":result[0][0].split(";")[1],"date":result[0][0].split(";")[2],"ipn":result[0][0].split(";")[3],"InsName":result[0][1].split(";")[0],"InsAdd":result[0][1].split(";")[1],"Npi":result[0][1].split(";")[2],"serviceDate":result[0][2].split(";")[0],"desc":result[0][2].split(";")[1],"pcode":result[0][2].split(";")[2],"dcode":result[0][2].split(";")[3],"charge":result[0][2].split(";")[4],"amount":result[0][3],"found":found,"pk":block.pk,"insAmt":result[0][4],"claimed":block.claimed,"requested":block.requested})
    else:
        found = 0
        return JsonResponse({"found":found})


def uploadBillInsurance(request):
   
    
    with open("ContactList.sol", "r") as file:
        contact_list_file = file.read()

    #to save the output in a JSON file
    
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"ContactList.sol": {"content": contact_list_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract 
                    }
                }
            },
        },
        solc_version="0.8.0",
    )
    # print(compiled_sol)
    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

    bytecode = compiled_sol["contracts"]["ContactList.sol"]["ContactList"]["evm"]["bytecode"]["object"]
    abi = json.loads(compiled_sol["contracts"]["ContactList.sol"]["ContactList"]["metadata"])["output"]["abi"]

    from web3 import Web3
   
    # For connecting to ganache
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    chain_id = 1337
    address = "0xF6A1fd15672f03b1821E55c197943f2773DBbD1b"
    private_key = "0x087a0c65caf76b725423cbc9cc5677fdc305f1ee56d964e7dd9325360caf1439"  # leaving the private key like this is very insecure if you are working on real world project
    # Create the contract in Python
    ContactList = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get the number of latest transaction
    nonce = w3.eth.get_transaction_count(address)

    transaction = ContactList.constructor().build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": address,
            "nonce": nonce,
        }
    )
    # Sign the transaction
    sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Deploying Contract!")
    # Send the transaction
    transaction_hash = w3.eth.send_raw_transaction(sign_transaction.raw_transaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")

    block = Block.objects.filter(pk= request.POST.get("pk")).first()
    block.transacion_address = str(transaction_receipt.contractAddress)
    block.save()
    Notification.objects.create(user = User.objects.filter(username = block.user).first(),message = "Your insurance for medical bill " + block.ipn + " has been approved. Insurance of " + request.POST.get('insAmt') +" has been approved.", ipn = block.ipn)
    block.claimed =  True
    block.save()
    contact_list = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)
    patientInfo = request.POST.get('name') + ";" + str(request.POST.get('address'))+ ";" + request.POST.get("dob")+ ";"+request.POST.get("ins-policy")
    providerInfo = request.POST.get("prov-name")+ ";"+request.POST.get("prov-address")+ ";"+ request.POST.get("prov-npi")
    service = request.POST.get("date-of-service")+ ";"+request.POST.get("service-desc")+ ";"+request.POST.get("service-code")+ ";"+request.POST.get("diagnosis-code")+ ";"+request.POST.get("charge")
    amount = request.POST.get("total-due")
    InsAmount = request.POST.get('insAmt')
    store_contact = contact_list.functions.addContact(
        patientInfo,providerInfo,service,amount,InsAmount
        
    ).build_transaction({"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 1})

    # Sign the transaction
    sign_store_contact = w3.eth.account.sign_transaction(
        store_contact, private_key=private_key
    )
    # Send the transaction
    send_store_contact = w3.eth.send_raw_transaction(sign_store_contact.raw_transaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)

    print("saved!!!!!!!!!!!")
    
    return HttpResponseRedirect(reverse('homepage'))


def createPolicy(request):
    Policy.objects.create(user = request.user,image = request.FILES['image'],name = request.POST.get('policy_name'),description = request.POST.get('policy_desc'),type =request.POST.get('policy_type'),amount = request.POST.get('policy_amount'))
    return HttpResponseRedirect(reverse('homepage'))

def policies(request):
    policies = Policy.objects.all()
    return render(request,'policies.html',{'policies':policies})


def getPolicy(request):
    policy = Policy.objects.filter(pk = request.POST.get('pk')).first()
    return JsonResponse({"title":policy.name,"desc":policy.description,"image":policy.image.url,"type":policy.type,"amount":policy.amount})

def contact(request):
    return render(request,'Contactus.html')

def claim(request):
    block = Block.objects.filter(ipn = request.POST.get('ipn')).first()
    block.requested = True 
    block.save()
    Notification.objects.create(user = block.ins,message = "Approval request for medical bill with ipn " + block.ipn,ipn = block.ipn)

    return JsonResponse({"found":"found"})


def checkFraud(request):
    ipn       = request.POST.get('ipn', '').strip()
    charge    = request.POST.get('charge', '').strip()
    total_due = request.POST.get('total-due', '').strip()

    if not ipn or not charge or not total_due:
        return JsonResponse({"error": "IPN, Charge, and Total Due are all required."}, status=400)

    # Generate hash from the submitted values (same formula as uploadBill)
    submitted_hash = hashlib.sha256("|".join([ipn, charge, total_due]).encode()).hexdigest()

    # Look up the bill record by IPN
    block = Block.objects.filter(ipn=ipn).first()
    if not block:
        return JsonResponse({"genuine": None, "error": f"IPN '{ipn}' not found in the system."})

    if not block.bill_hash:
        return JsonResponse({"genuine": None, "error": "This bill has no hash on record. It may have been uploaded before fraud detection was enabled."})

    genuine = (submitted_hash == block.bill_hash)
    return JsonResponse({"genuine": genuine, "ipn": ipn})
