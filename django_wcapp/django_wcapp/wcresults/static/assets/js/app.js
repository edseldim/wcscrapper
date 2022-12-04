const dateInput = document.querySelector("#date-picker");
const submitBtn = document.querySelector(".date-form > input");
const matchesContainer = document.querySelector(".match-data");
const dateMatchInput = document.querySelector(".date-data");

let dateObj = {
    dateInput:""
}

class UI{
    removeHTML(){
        while(matchesContainer.firstChild){
            matchesContainer.firstChild.remove();
        }
    }

    loadingMessage(){
        const messageP = document.createElement("P");
        messageP.textContent = "loading..."
        submitBtn.parentElement.parentElement.append(messageP);
        return messageP;
    }

    loadMatches(matchData){
        matchData.forEach(data => {
            const rawHTMLElement = document.createElement("div");
            rawHTMLElement.innerHTML = `
            <div class="match-data-container">
            <h3>
                ${data["groupName"]}
            </h3>
            <div class="match-data-metadata">
                <p>
                    ${data["countryHost"]["name"]} -
                    ${data["countryAway"]["name"]}
                </p>
                <div class="match-data-result">
                    <p>
                        Result: ${data["countryHost"]["score"]} - ${data["countryAway"]["score"]}
                    </p>
                </div>
            </div>
            </div>
            `
            matchesContainer.append(rawHTMLElement);
        })
    }
}

const ui = new UI();
eventRegister();
function eventRegister(){
    submitBtn.addEventListener("click", (e) =>{
        if(dateObj["dateInput"] === ""){
            return;
        }

        e.preventDefault();
        loadingTxt = ui.loadingMessage();
        fetch(`http://127.0.0.1:8000/wcresults/results-${converTime(dateObj["dateInput"])}`)
            .then(response => response.json())
            .then(response => {
                let matchArray = [];
                response.data.forEach((data) => {
                    matchArray.push({
                        countryHost:{
                            name:data["Home"]["name"],
                            score:data["Home"]["score"]},
                        countryAway:{
                            name:data["Away"]["name"],
                            score:data["Away"]["score"]},
                        groupName:data["group_name"],
                    })
                })
                console.log(response, matchArray);
                loadingTxt.remove();
                ui.removeHTML();
                ui.loadMatches(matchArray);
                dateMatchInput.textContent = dateObj["dateInput"];
            })
            .catch(err => console.error(err));
    });
    dateInput.addEventListener("blur", dateChecker);
}

function dateChecker(e){
    if(e.target.value === ""){
        return;
    }
    dateObj["dateInput"] = e.target.value;
    console.log(dateObj);
}

function converTime(string){
    year = string.substring(0,4)
    month = string.substring(5,7)
    day = string.substring(8,10)
    return `${year}${month}${day}`
}