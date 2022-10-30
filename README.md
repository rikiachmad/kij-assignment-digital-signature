# kij-assignment-digital-signature

# Table of contents
- [kij-assignment-digital-signature](#kij-assignment-digital-signature)
- [Table of contents](#table-of-contents)
  - [Description](#description)
  - [Requirements](#requirements)
  - [Usage](#usage)

## Description
![alt text](https://github.com/rikiachmad/kij-assignment-digital-signature/blob/main/assets/digital-signature.jpg?raw=true)

In this assignment we create a python program that takes a PDF documents and create a digital signature with the user's private key. This program also able to verify the PDF documents that is already signed. To be able to validate the PDF's digital signature, the verifier needs the public key corresponding to the user's private key used to sign the documents. If user doesn't have any key pairs this program has the feature to generate the key pairs in the PEM format.

**Signing PDF Documents**
<br />
The program uses the SHA256 to create hash value of the pdf document. After the hash value is generated, that hash value will be encrypted with private key using RSA Algorithm with the help of PyCrypto library. The encrypted hash value then embedded in the pdf documents without changing any content of the document itself.

**Verifying Signature**
<br />
The program first goes through the documents binary to find any embedded signature. If the signature is not found then the program will output 'Signature not found'. If the signature is found, the program then fetch the encrypted hash value and uses the provided public key to validate the signature. The program will print 'Signature is valid' if the public key is able to validate the signature, otherwise 'Signature is not valid' will be printed.

**Generating Key Pairs**
<br />
If the user doesnt have any keys to sign the pdf documents, this program has the feature to generate the key pairs. Using the help of the PyCrypto, key pairs is generated using the RSA key generations.

## Requirements
Requirements to run this program is defined in the requirements.txt. Run ``` pip install -r requirements.txt``` to install all the requirements.

## Usage
Clone this repo with
``` git clone https://github.com/rikiachmad/kij-assignment-digital-signature.git ```  
<br />
See full available commands
<br />
``` python3 main.py --help```
<br />
Generating key pairs
<br />
``` python3 main.py -x```
<br />
To sign the pdf documents
<br />
``` python3 main.py -i [PDF_FILE_PATH] -s [PRIVATE_KEY_PATH] ```
<br />
And for verifying the signed document
<br />
``` python3 main.py -i [PDF_FILE_PATH] -v [PUBLIC_KEY_PATH] ```
<br />
Note: In digital signature private key can only be used for encryption(signing) and public key can only be used for decryption(verifying).