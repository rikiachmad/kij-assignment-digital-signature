from PyPDF2 import PdfFileReader, errors
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from pathlib import Path
import argparse

class App:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Available Options")
    
    def import_public_key(self, path):
        try:
            pkey_str = open(path,"r").read()
            public_key = RSA.importKey(pkey_str)
        except:
            raise Exception("Invalid key path")
        return public_key

    def import_private_key(self, path):
        try:
            pkey_str = open(path,"r").read()
            private_key = RSA.importKey(pkey_str)
        except:
            raise Exception("Invalid key path")
        return private_key

    def verify_pdf(self, pdf_path, key_path):
        hash = self.get_hash(pdf_path)
        public_key = self.import_public_key(key_path)
        decryptor = pkcs1_15.new(public_key)

        f = open(pdf_path, "rb")
        lines = f.readlines()
        sig = ""
        for line in lines:
            if line.startswith(b"Signature"):
                sig = line.split(b':')[1]
                break
        f.close()

        if not sig:
            print(f"Signature not found in {pdf_path}")
            return
        try:
            decryptor.verify(hash, bytes.fromhex(sig.decode()))
        except ValueError:
            print("Signature not valid.")
            return
        print("Signature is valid.")

    def sign_pdf(self, pdf_path, key_path):
        hash = self.get_hash(pdf_path)
        private_key = self.import_private_key(key_path)
        encryptor = pkcs1_15.new(private_key)
        encrypted_hash = encryptor.sign(hash)

        new_pdf = Path(pdf_path).stem + '-signed.pdf'

        f = open(pdf_path, "rb")
        nf = open(new_pdf, "wb")
        lines = f.readlines()
        for line in lines:
            nf.write(line)
            if line == b"%%EOF" or line == b"%%EOF\n":
                break
        nf.write(b"\nSignature:")
        nf.write(encrypted_hash.hex().encode())
        nf.close()
        f.close()

    def get_hash(self, path):
        sha256 = SHA256.new()
        try:
            f = open(path, "rb")
            lines = f.readlines()
            for line in lines:
                if line == b"%%EOF" or line == b"%%EOF\n":
                    sha256.update(b"%%EOF")
                    break
                sha256.update(line)
            f.close()
        except errors:
            raise Exception(errors)
        return sha256

    def generate_keypair(self):
        key = RSA.generate(2048)
        priv = open('private_key.pem','wb')
        pub = open('public_key.pem', 'wb')
        priv.write(key.export_key('PEM'))
        pub.write(key.public_key().export_key('PEM'))
        priv.close()
        pub.close()

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