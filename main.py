
from databse import engine
from sqlalchemy import text


# --------------------------------
# ADD PATIENT
# --------------------------------

def add_patient():

    name = input("Enter patient name: ")
    age = int(input("Enter patient age: "))
    gender = input("Enter gender: ")
    phone = input("Enter phone number: ")
    disease = input("Enter disease: ")

    query = text("""
        INSERT INTO patients
        (name, age, gender, phone, disease)
        VALUES
        (:name, :age, :gender, :phone, :disease)
    """)

    try:
        with engine.begin() as connection:
            connection.execute(query, {
                "name": name,
                "age": age,
                "gender": gender,
                "phone": phone,
                "disease": disease
            })

        print("Patient added successfully!")

    except Exception as e:
        print("Error:", e)


# --------------------------------
# VIEW PATIENTS
# --------------------------------

def view_patients():

    query = text("SELECT * FROM patients")

    try:
        with engine.connect() as connection:
            result = connection.execute(query)

            rows = result.fetchall()

            if not rows:
                print("No patient records found.")
                return

            for row in rows:
                print(row)

    except Exception as e:
        print("Error:", e)


# --------------------------------
# UPDATE PATIENT
# --------------------------------

def update_patient():

    patient_id = int(input("Enter patient ID: "))
    name = input("Enter new patient name: ")
    age = int(input("Enter new age: "))
    gender = input("Enter new gender: ")
    phone = input("Enter new phone: ")
    disease = input("Enter new disease: ")

    query = text("""
        UPDATE patients
        SET name = :name,
            age = :age,
            gender = :gender,
            phone = :phone,
            disease = :disease
        WHERE patient_id = :patient_id
    """)

    try:
        with engine.begin() as connection:
            result = connection.execute(query, {
                "name": name,
                "age": age,
                "gender": gender,
                "phone": phone,
                "disease": disease,
                "patient_id": patient_id
            })

        if result.rowcount > 0:
            print("Patient updated successfully!")
        else:
            print("Patient ID not found.")

    except Exception as e:
        print("Error:", e)


# --------------------------------
# DELETE PATIENT
# --------------------------------

def delete_patient():

    patient_id = int(input("Enter patient ID: "))

    query = text("""
        DELETE FROM patients
        WHERE patient_id = :patient_id
    """)

    try:
        with engine.begin() as connection:
            result = connection.execute(query, {
                "patient_id": patient_id
            })

        if result.rowcount > 0:
            print("Patient deleted successfully!")
        else:
            print("Patient ID not found.")

    except Exception as e:
        print("Error:", e)


# --------------------------------
# MAIN MENU
# --------------------------------

def main():

    while True:

        print("\n===== HOSPITAL MANAGEMENT SYSTEM =====")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Update Patient")
        print("4. Delete Patient")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_patient()

        elif choice == "2":
            view_patients()

        elif choice == "3":
            update_patient()

        elif choice == "4":
            delete_patient()

        elif choice == "5":
            print("Exiting Hospital Management System...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
