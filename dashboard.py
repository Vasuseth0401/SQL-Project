
import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy import text
from databse import engine

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="MediCare | Hospital Management",
    page_icon="🏥",
    layout="wide"
)

# ----------------------------------
# CUSTOM CSS
# ----------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #18283c);
    color: white;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.07);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
}

[data-testid="stMetricLabel"] {
    color: #aab6c8;
}

[data-testid="stMetricValue"] {
    color: #62d6c8;
}

h1, h2, h3 {
    color: white;
}

[data-testid="stSidebar"] {
    background: #111c2d;
}
</style>
""", unsafe_allow_html=True)


# ----------------------------------
# DATABASE FUNCTION
# ----------------------------------

def load_data(query):

    try:
        with engine.connect() as connection:
            df = pd.read_sql(
                text(query),
                connection
            )
        return df

    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()


# ----------------------------------
# SIDEBAR
# ----------------------------------

st.sidebar.title("🏥 MediCare")
st.sidebar.caption("Hospital Management System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Patients",
        "Doctors",
        "Appointments",
        "Billing"
    ]
)

if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()


# ----------------------------------
# DASHBOARD PAGE
# ----------------------------------

if page == "Dashboard":

    st.title("Hospital Dashboard")
    st.caption("Hospital performance and database analytics")

    # KPI QUERIES

    patients = load_data(
        "SELECT COUNT(*) AS total FROM patients"
    )

    doctors = load_data(
        "SELECT COUNT(*) AS total FROM doctors"
    )

    appointments = load_data(
        "SELECT COUNT(*) AS total FROM appointments"
    )

    revenue = load_data("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM billing
        WHERE payment_status = 'Paid'
    """)

    pending = load_data("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM billing
        WHERE payment_status = 'Pending'
    """)

    if all(not df.empty for df in [
        patients, doctors, appointments, revenue, pending
    ]):

        # KPI CARDS

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Total Patients",
            int(patients.iloc[0]["total"])
        )

        c2.metric(
            "Total Doctors",
            int(doctors.iloc[0]["total"])
        )

        c3.metric(
            "Appointments",
            int(appointments.iloc[0]["total"])
        )

        c4.metric(
            "Revenue Collected",
            f"₹{revenue.iloc[0]['total']:,.2f}"
        )

        st.divider()

        st.metric(
            "Pending Revenue",
            f"₹{pending.iloc[0]['total']:,.2f}"
        )

    # DISEASE ANALYTICS

    st.subheader("Hospital Analytics")

    left, right = st.columns(2)

    disease_df = load_data("""
        SELECT disease, COUNT(*) AS total
        FROM patients
        GROUP BY disease
    """)

    status_df = load_data("""
        SELECT status, COUNT(*) AS total
        FROM appointments
        GROUP BY status
    """)

    with left:

        st.markdown("### Disease Distribution")

        if not disease_df.empty:

            fig = px.bar(
                disease_df,
                x="disease",
                y="total",
                color="disease",
                template="plotly_dark",
                title="Patients by Disease"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("No disease records available.")

    with right:

        st.markdown("### Appointment Status")

        if not status_df.empty:

            fig = px.pie(
                status_df,
                names="status",
                values="total",
                hole=0.5,
                template="plotly_dark",
                title="Appointment Overview"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("No appointment records available.")

    # DOCTOR ANALYTICS

    st.subheader("Doctor-wise Appointments")

    doctor_df = load_data("""
        SELECT
            d.name AS doctor,
            COUNT(a.appointment_id) AS total_appointments
        FROM doctors d
        LEFT JOIN appointments a
        ON d.doctor_id = a.doctor_id
        GROUP BY d.doctor_id, d.name
    """)

    if not doctor_df.empty:

        fig = px.bar(
            doctor_df,
            x="doctor",
            y="total_appointments",
            template="plotly_dark",
            title="Appointments per Doctor"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No doctor records available.")


# ----------------------------------
# PATIENTS PAGE
# ----------------------------------

elif page == "Patients":

    st.title("Patient Management")

    df = load_data(
        "SELECT * FROM patients"
    )

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No patient records available.")


# ----------------------------------
# DOCTORS PAGE
# ----------------------------------

elif page == "Doctors":

    st.title("Doctor Management")

    df = load_data(
        "SELECT * FROM doctors"
    )

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No doctor records available.")


# ----------------------------------
# APPOINTMENTS PAGE
# ----------------------------------

elif page == "Appointments":

    st.title("Appointment Management")

    df = load_data("""
        SELECT
            a.appointment_id,
            p.name AS patient,
            d.name AS doctor,
            a.appointment_date,
            a.status
        FROM appointments a
        JOIN patients p
            ON a.patient_id = p.patient_id
        JOIN doctors d
            ON a.doctor_id = d.doctor_id
    """)

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No appointment records available.")


# ----------------------------------
# BILLING PAGE
# ----------------------------------

elif page == "Billing":

    st.title("Billing Management")

    df = load_data(
        "SELECT * FROM billing"
    )

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No billing records available.")


# ----------------------------------
# FOOTER
# ----------------------------------

st.divider()

st.caption(
    "MediCare | Hospital Management System | Python + MySQL"
)
