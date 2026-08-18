// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ContactList {
    // uint phoneNumber;
    
    struct Contact {
        // assosiate name with phone number
        
        
        string amount;
       
    }

    Contact[] public contact; //array for list of contacts
    // mapping(string => string) public nameToPhoneNumber; //used to map name to phone number, so you can get phone number using name
     
    function retrieve() public view returns (Contact[] memory){
        return contact; //retrieve tuple of all contacts
    }
    
    function addContact(string memory _amount) public {
        contact.push(Contact(_amount)); //append to  Contact[] array
        // nameToPhoneNumber[_name] = _phoneNumber; //use name to get phone number
    }
    
}



