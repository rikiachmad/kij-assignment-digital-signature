from PyPDF2 import PdfFileReader, errors, PdfFileWriter
from OpenSSL import crypto
import argparse
import hashlib
import pprint
import os

class App:
    BUF_SIZE = 65536
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Available Options")
    
    def add_metadata(self, path, metadata="null"):
        print("hash-1")
        hash = self.get_hash(path).hexdigest()
        print(hash)
        # f = open(path, "ab+")
        # f.write(b"tes123\n")
        # f.close()

    def get_hash(self, path):
        sha256 = hashlib.sha256()
        try:
            f = open(path, "rb")
            lines = f.readlines()
            for line in lines:
                print(line)
                if line == b"%%EOF" or line == b"%%EOF\n" or line == b"%%EOF\r\n":
                    sha256.update(b"%%EOF")
                    break
                sha256.update(line)
            f.close()
        except errors:
            raise Exception(errors)
        return sha256

    def generate_keypair(self, type=crypto.TYPE_RSA, bits=4096):
        pkey = crypto.PKey()
        pkey.generate_key(type, bits)
        with open('private_key.pem', 'wb') as private:
            pk = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey)
            private.write(pk)
        # generate public key
        with open('public_key.pem', 'wb') as public:
            pk = crypto.dump_publickey(crypto.FILETYPE_PEM, pkey)
            public.write(pk)

    def parse_args(self):
        self.parser.add_argument('-i', '--input_pdf', dest='input_pdf', type=self.is_valid_pdf,
                            help="Enter the path of the pdf file to process")
        self.parser.add_argument('-s', '--sign', dest='sign_pdf',
                            type=str, help="Enter the private key to sign the document")
        self.parser.add_argument('-v', '--verify', dest='verify_pdf', type=str,
                            help="Enter the public key to verify the document")
        self.parser.add_argument('-x', '--generate', dest='generate_pair',
                            action="store_true", help="Generating key pair")

        args = vars(self.parser.parse_args())
        return args

    def is_valid_pdf(self,path):
        try:
            PdfFileReader(open(path, "rb"))
        except errors.PdfReadError:
            raise ValueError("invalid PDF file")
        if not path:
            raise ValueError(f"Invalid Path")
        return path

    def is_valid_private_key(self,path):
        pass

    def is_valid_public_key(self,path):
        pass
