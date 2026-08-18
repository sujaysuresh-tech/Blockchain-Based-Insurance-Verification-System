with open("ContactList.sol", "r") as file:
    contact_list_file = file.read()

from solcx import compile_standard, install_solc
install_solc('0.8.0')
import json #to save the output in a JSON file
...
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
# chain_id = 1337
# address = "0x800A3BF5d9C6e42fFe4A57c7968618DdE81fd7cA"
# private_key = "e0a9f2f78b2dca326b4116744b422d2ba1ba5c15392492c3c45a2e3fbe9021b0" # leaving the private key like this is very insecure if you are working on real world project
# # Create the contract in Python
# ContactList = w3.eth.contract(abi=abi, bytecode=bytecode)
# # Get the number of latest transaction
# nonce = w3.eth.getTransactionCount(address)

# transaction = ContactList.constructor().buildTransaction(
#     {
#         "chainId": chain_id,
#         "gasPrice": w3.eth.gas_price,
#         "from": address,
#         "nonce": nonce,
#     }
# )
# # Sign the transaction
# sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# print("Deploying Contract!")
# # Send the transaction
# transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
# # Wait for the transaction to be mined, and get the transaction receipt
# print("Waiting for transaction to finish...")
# transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
# print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")

# contact_list = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)
# store_contact = contact_list.functions.addContact(
#     "_patientInfo","_providerInfo","_services","_payment"
    
# ).buildTransaction({"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 1})

# # Sign the transaction
# sign_store_contact = w3.eth.account.sign_transaction(
#     store_contact, private_key=private_key
# )
# # Send the transaction
# send_store_contact = w3.eth.send_raw_transaction(sign_store_contact.rawTransaction)
# transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)

# print(contact_list.functions.retrieve().call())

# used to get data from blockchain
test = w3.eth.contract(address="0x3e1a17e419eeA1Ebbb9d0b4C5b5D01e1cD8BF9B9", abi=abi)
print(test.functions.retrieve().call())

result = test.functions.retrieve().call()
print("result",result[0])
# test = w3.eth.get_transaction('0xbf1b445cf5e9d016ef49034d6cba56d2e9397831289d3ae8478028f4690bddf2')