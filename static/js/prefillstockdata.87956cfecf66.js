//https://iexcloud.io/docs/api/#company
//https://cloud.iexapis.com/stable/stock/aapl/logo

let HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        let anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4)
                aCallback({response:anHttpRequest.responseText, status:anHttpRequest.status});
        }

        anHttpRequest.open( "GET", aUrl, true );            
        anHttpRequest.send( null );
    }
}

let sandbox_token = "Tsk_c46651ad647e4025a8a36e634a4300d0"
let token = "pk_658d5ee229fe4c09a75a846c8777ad08"

document.onreadystatechange = () => {
    if (document.readyState === 'complete') {
        if(document.getElementById("id_symbol")) {

            var client = new HttpClient();
            console.log("test");
            symbol = document.getElementById("id_symbol")
            companyName = document.getElementById("id_companyName")
            employees = document.getElementById("id_employees")
            exchange = document.getElementById("id_exchange")
            industry = document.getElementById("id_industry")
            website = document.getElementById("id_website")
            description = document.getElementById("id_description")
            ceo = document.getElementById("id_ceo")
            securityName = document.getElementById("id_securityName")
            issueType = document.getElementById("id_issueType")
            sector = document.getElementById("id_sector")
            primarySicCode = document.getElementById("id_primarySicCode")
            tags = document.getElementById("id_tags")
            address	=document.getElementById("id_address")
            address2  = document.getElementById("id_address2")
            state = document.getElementById("id_state")
            city = document.getElementById("id_city")
            zip = document.getElementById("id_zip")
            country = document.getElementById("id_country")
            phone = document.getElementById("id_phone")
            symbol.oninput = (event) => {
                symbol.value = symbol.value.toUpperCase()
                let sandbox_url = "https://sandbox.iexapis.com/stable/stock/" + symbol.value + "/company?token=" + sandbox_token
                let url_request = "https://cloud.iexapis.com/stable/stock/" + symbol.value + "/company?token=" + token

                client.get(url_request, function(response) {
                    // do something with response

                    if(response.status == 200) {
                        let object = JSON.parse(response.response);
                        companyName.value = object["companyName"]
                        employees.value = object["employees"]
                        exchange.value = object["exchange"]
                        industry.value = object["industry"]
                        website.value = object["website"]
                        description.value = object["description"]
                        ceo.value = object["ceo"]
                        securityName.value = object["securityName"]
                        issueType.value = object["issueType"]
                        sector.value = object["sector"]
                        primarySicCode.value = object["primarySicCode"]
                        tags.value = object["tags"]
                        address.value = object["address"]
                        address2.value = object["address2"]
                        state.value = object["state"]
                        city.value = object["city"]
                        zip.value = object["zip"]
                        country.value = object["country"]
                        phone.value = object["phone"]
                    }
                    else {
                        companyName.value = ""
                        employees.value = ""
                        exchange.value = ""
                        industry.value = ""
                        website.value = ""
                        description.value = ""
                        ceo.value = ""
                        securityName.value = ""
                        issueType.value = ""
                        sector.value = ""
                        primarySicCode.value = ""
                        tags.value = ""
                        address.value = ""
                        address2.value = ""
                        state.value = ""
                        city.value = ""
                        zip.value = ""
                        country.value = ""
                        phone.value = ""
                    }

                });
            }
        }
    }
}



