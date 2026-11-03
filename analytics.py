
from databse import create_connection


def run_analytics():

    conn = create_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    # 1. Total Patients
    cursor.execute("""
        SELECT COUNT(*) FROM patients
    """)

    total_patients = cursor.fetchone()[0]

    print("\nTotal Patients:", total_patients)

    # 2. Patients by Disease
    cursor.execute("""
        SELECT disease, COUNT(*)
        FROM patients
        GROUP BY disease
        ORDER BY COUNT(*) DESC
    """)

    print("\nPatients by Disease:")

    for row in cursor.fetchall():
        print(row)

    # 3. Appointment Statistics
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM appointments
        GROUP BY status
    """)

    print("\nAppointment Statistics:")

    for row in cursor.fetchall():
        print(row)

    # 4. Doctor-wise Appointments
    cursor.execute("""
        SELECT d.name, COUNT(a.appointment_id)
        FROM doctors d
        LEFT JOIN appointments a
        ON d.doctor_id = a.doctor_id
        GROUP BY d.doctor_id, d.name
    """)

    print("\nDoctor-wise Appointments:")

    for row in cursor.fetchall():
        print(row)

    # 5. Revenue
    cursor.execute("""
        SELECT
            SUM(amount),
            SUM(CASE WHEN payment_status = 'Paid'
                THEN amount ELSE 0 END),
            SUM(CASE WHEN payment_status = 'Pending'
                THEN amount ELSE 0 END)
        FROM billing
    """)

    revenue = cursor.fetchone()

    print("\nTotal Billed:", revenue[0])
    print("Collected Revenue:", revenue[1])
    print("Pending Revenue:", revenue[2])

    cursor.close()
    conn.close()


if __name__ == "__main__":
    run_analytics()
