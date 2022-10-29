from ast import dump
from app import App
from OpenSSL import crypto

if __name__ == '__main__':
    app = App()
    args = app.parse_args()
    if args["generate_pair"]:
        app.generate_keypair()

    elif args["sign_pdf"]:
        if not args["input_pdf"]:
            raise Exception("Input pdf file path.")
        path = args["input_pdf"]
        app.add_metadata(path)
        print(f"Document {path} has been signed.")
        # hash = app.get_hash(path)
        # print(hash.hexdigest())

    elif args["verify_pdf"]:
        if not args["input_pdf"]:
            raise Exception("Input pdf file path.")
        path = args["input_pdf"]
