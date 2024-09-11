function showSignupForm() {
    const userType = document.getElementById('signup-user-type').value;
    const doctorForm = document.getElementById('doctor-form');
    const patientForm = document.getElementById('patient-form');

    if (userType === 'doctor') {
      doctorForm.classList.add('visible');
      doctorForm.classList.remove('hidden');
      patientForm.classList.add('hidden');
      patientForm.classList.remove('visible');
    } else if (userType === 'patient') {
      patientForm.classList.add('visible');
      patientForm.classList.remove('hidden');
      doctorForm.classList.add('hidden');
      doctorForm.classList.remove('visible');
    }
  }

  // Call this function when the page loads to show the correct default form
  window.onload = function() {
    showSignupForm(); // Automatically call to ensure the correct form is shown on page load
  }
  function login() {
    const userType = document.getElementById("user-type").value;
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;
  
    if (userType === "doctor") {
      window.location.href = "doctor_dashboard.html";
    } else {
      window.location.href = "patient_dashboard.html";
    }
  }
  
  function signup(userType) {
    if (userType === "doctor") {
      const email = document.getElementById("doctor-email").value;
      const password = document.getElementById("doctor-password").value;
      // Collect the rest of the doctor details here
      window.location.href = "doctor_dashboard.html";
    } else {
      const email = document.getElementById("patient-email").value;
      const password = document.getElementById("patient-password").value;
      // Collect the rest of the patient details here
      window.location.href = "patient_dashboard.html";
    }
  }
  