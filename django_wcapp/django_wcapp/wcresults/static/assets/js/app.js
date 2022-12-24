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

    showMessage(messageText, relativeParent,disappear=true){ // submitBtn.parentElement.parentElement
        const messageP = document.createElement("P");
        const divBlock = document.createElement("DIV");
        messageP.textContent = messageText
        divBlock.setAttribute("style","text-align:center")
        divBlock.append(messageP)
        relativeParent.append(divBlock);
        if(!disappear){
            return divBlock;
        }
        setTimeout(()=>{
            messageP.remove()
        },3000)
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

        if(matchesContainer.children.length===0){
            this.showMessage("No data to show",submitBtn.parentElement.parentElement,true)
        }
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
        loadingTxt = ui.showMessage("loading...",submitBtn.parentElement.parentElement,false);
        fetch(`http://${document.location["host"]}/wcresults/results-${converTime(dateObj["dateInput"])}`)
            .catch(err => {
                loadingTxt.remove()
                ui.showMessage("Internal Error. Please try again later.",submitBtn.parentElement.parentElement,true)
            })
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
                loadingTxt.remove();
                ui.removeHTML();
                ui.loadMatches(matchArray);
                dateMatchInput.textContent = dateObj["dateInput"];
            });
    });
    dateInput.addEventListener("blur", dateChecker);
}

function dateChecker(e){
    if(e.target.value === ""){
        return;
    }
    dateObj["dateInput"] = e.target.value;
}

function converTime(string){
    year = string.substring(0,4)
    month = string.substring(5,7)
    day = string.substring(8,10)
    return `${year}${month}${day}`
}