
import hashlib

TESTING_SECRET = "testing123"  # Default value for testing purposes

def check_master_secret(MASTER_SECRET):

    # Fix this in the code to the sha256sum of the master secret
    MASTER_HASH='59a61bdad01d1074a37bc6ee2ae4bac0a424fc2fcfcbdfd0c386d1fdac0d5c7e'
    # MASTER_HASH = hashlib.sha256(TESTING_SECRET.encode()).hexdigest()  # For testing purposes

    # PLEASE PLEASE PLEASE DO NOT REMOVE THIS CHECK
    # IF YOU FLASH THE WRONG SECRET TO THE DEVICE IT CAN NEVER BE UNDONE
    if hashlib.sha256(MASTER_SECRET.encode()).hexdigest() != MASTER_HASH:
        print("Master secret does not match")
        raise Exception("Master secret does not match")
