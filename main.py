from ast import dump
from app import App

if __name__ == '__main__':
    app = App()
    args = app.parse_args()
    if args["generate_pair"]:
        app.generate_keypair()

    elif args["sign_pdf"]:
        if not args["input_pdf"]:
            raise Exception("Input pdf file path.")
        pdf_path = args["input_pdf"]
        key_path = args["sign_pdf"]
        app.sign_pdf(pdf_path, key_path)
        print(f"Document {pdf_path} has been signed.")

    elif args["verify_pdf"]:
        if not args["input_pdf"]:
            raise Exception("Input pdf file path.")
        pdf_path = args["input_pdf"]
        key_path = args["verify_pdf"]
        app.verify_pdf(pdf_path, key_path)