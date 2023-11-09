if __name__ == "__main__":
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore

    # Use a service account
    cred = credentials.Certificate('..\config\chatbot-2c28b-firebase-adminsdk-eoj2u-af1dbe56f8.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    if (db):
        print("succes")
