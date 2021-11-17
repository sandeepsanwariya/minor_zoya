console.log("Razor pay js attached successfully")


function Subscribe(creator, customer, id) {
    console.log(id)
    let subscribe_txt = document.getElementById(`subscribe_txt${id}`)
    let spinner = document.getElementById(`spinner${id}`)

    subscribe_txt.classList.toggle('hide')
    spinner.classList.toggle('hide')


    if (creator == customer) {
        alert("You Cannot Subscribe Yourself")
        subscribe_txt.classList.toggle('hide')
        spinner.classList.toggle('hide')
        return
    }
    let url = `/payment/subscribe/${creator}/`;
    data = {}
    fetch(url, {
        method: 'post',

        body: JSON.stringify(data)
    }).then(function(response) {

        return response.json()
    }).then(function(json_response) {

        console.log(json_response)
        subscribe_txt.classList.toggle('hide')
        spinner.classList.toggle('hide')
        var options = {
            "key": "rzp_test_J9Lxu7OB8M6GR3", // Enter the Key ID generated from the Dashboard
            // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            "currency": "INR",
            "name": "Abrar Ahmed",
            "description": "Test Transaction",
            "recurring": true,
            "subscription_id": json_response.id,
            "callback_url": `/${creator}/`,
            "prefill": {
                "name": json_response.name,
                "email": json_response.email,
                "contact": json_response.phone
            },
            "handler": function() {
                window.location.reload()
            },
            "notes": {
                "address": "Subscription Charges Monthly on Zocaya.com"
            },
            "theme": {
                "color": "#3399cc"
            },

        };
        var rzp1 = new Razorpay(options);
        rzp1.open();

    })


}




function Donation(creator, customer) {

    if (creator == customer) {
        alert("You Cannot Donate Yourself")
        return
    }
    let url = `/payment/donate/${creator}/`;
    var am=document.getElementById('donate_amount').value
    console.log(am)
    var formData = new FormData();
    formData.append('amount',am);
    fetch(url, {
        method: 'POST',
        body: formData
    }).then(function(response) {
        return response.json()
    }).then(function(json_response) {

        console.log(json_response)

        
        var options = {
            "key": "rzp_test_J9Lxu7OB8M6GR3", // Enter the Key ID generated from the Dashboard
            "currency": "INR",
            "name": "Zocaya",
            "description": "Test Transaction",
            "image": '/static/favicon.jpeg',
            "order_id": json_response.id, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
            "handler": function (response){
                console.log({
                    razorpay_payment_id:response.razorpay_payment_id,
                    razorpay_order_id:response.razorpay_order_id,
                    razorpay_signature:response.razorpay_signature
                })
                var data = new FormData();
                data.append('razorpay_payment_id',response.razorpay_payment_id);
                data.append('razorpay_order_id',response.razorpay_order_id)
                data.append('razorpay_signature',response.razorpay_signature)
                fetch(`/payment/donationvarify/${creator}/`, {
                    method: 'POST',
                    body: data
                }).then(function(response) {
                    console.log(response)
                    return response.json()
                }).then(function(json_response) {
                    console.log(json_response)
                    var res=(json_response)
                    
                    if (res['status']==='paid'){
                        console.log(res['status'])
                        var popup = document.getElementById("mobDonation");
                        console.log(popup)
                        popup.style.display='none';
                        var thank = document.getElementById("thankDonation");
                        console.log(thank)
                        thank.style.display='block';
                    }
                })
            },
            "prefill": {
                "name": json_response.name,
                "email": json_response.email,
                "contact": json_response.phone
            },
            "notes": {
                "address": "Razorpay Corporate Office"
            },
            "theme": {
                "color": "#3399cc"
            }
        };
        var rzp1 = new Razorpay(options);
        rzp1.on('payment.failed', function (response){
                
                alert(response.error.description);
        });
        var rzp1 = new Razorpay(options);
        rzp1.open();
        console.log(rzp1)

    })


}