let number_of_fields = 1;
let addButton = document.getElementById("add_choice_button");
let reduceButton = document.getElementById("reduce_choice_button");
let form = document.getElementById("new-edit-poll__fields");
let categories = logMovies();

function get_new_choice_element(){
    let new_element = Object.assign(document.createElement("div"), {class: "new-edit-poll__field"});
    new_element.className = "new-edit-poll__field";
    new_element.id = `new-edit-poll__field__${number_of_fields}`
    let label = document.createElement("label");
    label.textContent = "Choice text";
    let input = document.createElement("input");
    input.id = `choice_text_${number_of_fields}`;
    input.name = `choice_text_${number_of_fields}`;
    input.type = "text";
    new_element.appendChild(label);
    new_element.appendChild(input);
    return new_element;
}

async function logMovies() {
  const response = await fetch("http://127.0.0.1:8000/polls/category_list/");
  return response.json();
}


(function initial_field(){
    for(let i = 0; i < 2; i++){
        form.appendChild(get_new_choice_element());
        number_of_fields += 1;
    }

    //Create array of options to be added
    //Create and append select list
    let selectList = document.createElement("select");
    selectList.id = "mySelect";
    form.appendChild(selectList);

    //Create and append the options
    for (let i = 0; i < categories.length; i++) {
        let option = document.createElement("option");
        option.value = categories[i];
        option.text = categories[i];
        selectList.appendChild(option);
    }
}());

addButton.addEventListener('click', () => {
    if(number_of_fields < 10) {
        form.appendChild(get_new_choice_element());
        number_of_fields += 1;
    }
})

reduceButton.addEventListener('click', () => {
    if(number_of_fields > 3) {
        number_of_fields -= 1;
        let element = document.getElementById(`new-edit-poll__field__${number_of_fields}`);
        element.remove()
    }
});
