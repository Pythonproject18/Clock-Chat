function open_sign_up_modal(){
    let loginModal = document.getElementById('log_in');
    let signupmodal = document.getElementById('sign_up');
    signupmodal.style.display = "block";
    loginModal.style.display="none";
}

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

async function sendOTP2() {
    let purpose = "signup";
    let email = document.getElementById("email2").value;
    let loader = document.getElementById("modal"); // Get the loader element

    if (!email) {
        console.log("Error: Please enter your email.");
        return;
    }

    console.log("Sending OTP to:", email);
    loader.style.display = "block"; // Show the loader
    document.body.style.overflow = 'hidden';


    try {
        let response = await fetch("/api/send-otp/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken()
            },
            body: new URLSearchParams({ email: email , purpose:purpose })
        });

        let result = await response.json();
        console.log("Response received:", result);

        if (response.ok) {
            console.log("OTP sent successfully.");
            document.getElementById("otpSection2").classList.remove("hidden");
            document.getElementById("emailSection2").classList.add("hidden");
        } else {
            console.log("Error:", result.message || "Failed to send OTP.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
    finally {
        loader.style.display = "none"; // Hide the loader after request completes
        document.body.style.overflow = 'auto';
    }
}

async function verifyOTP2() {
    let email = document.getElementById("email2").value;
    let otp = document.getElementById("otp2").value;


    if (!otp) {
        console.log("Error: Please enter the OTP.");
        return;
    }

    console.log("Verifying OTP for:", email, "OTP:", otp);

    try {
        let response = await fetch("/api/verify-otp/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken()
            },
            body: new URLSearchParams({ email: email, otp: otp })
        });

        let result = await response.json();
        console.log("Response received:", result);

        if (response.ok) {
            console.log("OTP verification successful.");
            document.getElementById("otpSection2").classList.add("hidden");
            document.getElementById("emailSection2").classList.add("hidden");
            document.getElementById("nameSection").classList.remove("hidden");
        } else {
            console.log("Error:", result.message || "Invalid OTP.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

async function submitForm() {
    let email = document.getElementById("email2").value;
    let first_name = document.getElementById("first_name").value;
    let middle_name = document.getElementById("middle_name").value;
    let last_name = document.getElementById("last_name").value;
    let loader = document.getElementById("modal"); // Get the loader element
    let loginModal = document.getElementById('log_in');
    let signupmodal = document.getElementById('sign_up');

    if (!first_name || !last_name) {
        console.log("Error: First name and Last name are required.");
        return;
    }

    console.log("Submitting signup form for:", email);
    
    loader.style.display = "block"; // Show the loader
    document.body.style.overflow = 'hidden';


    try {
        let response = await fetch("/api/signup/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken()
            },
            body: new URLSearchParams({ 
                email: email, 
                first_name: first_name, 
                middle_name: middle_name, 
                last_name: last_name 
            })
        });

        let result = await response.json();
        console.log("Response received:", result);

        if (response.ok) {
            console.log("Signup successful. Redirecting...");
            // Keep the loader visible during redirection
            setTimeout(() => {
                loader.style.display = "none"; // Hide loader only if verification fails
                signupmodal.style.display = "none";
                loginModal.style.display="block";
            }, 2000);
            
            document.body.style.overflow = 'auto';
        } else {
            console.log("Error:", result.message || "Signup failed.");
            loader.style.display = "none"; // Hide the loader if signup fails
            document.body.style.overflow = 'auto';

        }
    } catch (error) {
        console.error("Error:", error);
        loader.style.display = "none"; // Hide the loader in case of an error
        document.body.style.overflow = 'auto';

    }
}