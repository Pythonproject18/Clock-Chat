
  function open_login_modal(){
    let loginModal = document.getElementById('log_in');
    loginModal.style.display="block";
  }
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    async function sendOTP() {
        let purpose = "login";
        let email = document.getElementById("email").value;
        let loader = document.getElementById("modal"); // Get the loader element

        if (!email) {
            console.log("Error: Please enter your email.");
            return;
        }

        console.log("Sending OTP to:", email, "Purpose:", purpose);
        loader.style.display = "block"; // Show the loader
        document.body.style.overflow = 'hidden';


        try {
            let response = await fetch("/api/send-otp/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken()
                },
                body: new URLSearchParams({ email: email, purpose: purpose })
            });

            let result = await response.json();
            console.log("Response received:", result);

            if (response.ok) {
                console.log("OTP sent successfully.");
                document.getElementById("otpSection").classList.remove("hidden");
                document.getElementById("emailSection").classList.add("hidden");
            } else {
                console.log("Error:", result.message);
            }
        } catch (error) {
            console.error("Error:", error);
        } finally {
            loader.style.display = "none"; // Hide the loader after request completes
            document.body.style.overflow = 'auto';
        }
    }

    async function verifyOTP() {
        let email = document.getElementById("email").value;
        let otp = document.getElementById("otp").value;
        let loader = document.getElementById("modal"); // Get the loader element
    
        if (!otp) {
            console.log("Error: Please enter the OTP.");
            return;
        }
    
        console.log("Verifying OTP for:", email, "OTP:", otp); // Debug Log
        loader.style.display = "block"; // Show the loader before making the request
        document.body.style.overflow = 'hidden';
    
        try {
            let response = await fetch("/api/verify-otp-login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken()
                },
                body: new URLSearchParams({ email: email, otp: otp })
            });
    
            let result = await response.json();
            console.log("Response received:", result); // Debug Log
    
            if (response.ok) {
                console.log("OTP verification successful. Redirecting...");
    
                // Keep the loader visible during redirection
                setTimeout(() => {
                    window.location.href = "/chat/";
                    loader.style.display = "none"; // Hide loader only if verification fails

                }, 2000);
                
                document.body.style.overflow = 'auto';
                
            } else {
                console.log("Error:", result.message);
                loader.style.display = "none"; // Hide loader only if verification fails
                document.body.style.overflow = 'auto';
            }
        } catch (error) {
            console.error("Error:", error); // Debug Log
            loader.style.display = "none"; // Hide loader on error
            document.body.style.overflow = 'auto';
        }
    }
    
    window.addEventListener('pageshow', function (event) {
        if (event.persisted || performance.getEntriesByType("navigation")[0].type === "back_forward") {
            location.reload()
          // Clear the OTP input
          const otpInput = document.getElementById("otp");
          if (otpInput) {
            otpInput.value = '';
          }
        }
      });
