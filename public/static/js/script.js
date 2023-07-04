const options = {
    insert:[
        {title: "Insert New Tractor Information", id: "insert-new-tractor-info"},
        {title: "Insert Repair Information", id: "insert-repair-info"},
    ],
    get: [
        {title: "Get Repair Information", id: "get-repair-info"}
    ]
};

const categorySelect = document.getElementById('categorySelect');
const optionSelect = document.getElementById('optionSelect');
const goButton = document.getElementById('goButton');

categorySelect.addEventListener('change', function() {
    const selectedCategory = this.value;

    optionSelect.innerHTML = '<option value="">--Choose an option--</option>';
    optionSelect.disabled = false;
    goButton.disabled = true;


    options[selectedCategory].forEach(function(option) {
        const optionElement = document.createElement('option');
        optionElement.value = option.id;
        optionElement.text = option.title;
        optionSelect.appendChild(optionElement);
    });


});

optionSelect.addEventListener("change", function () {
    goButton.style.visibility = 'visible'
    const selectedOption = this.value;
    goButton.onclick = function () {
        // Scroll to the selected section when the button is clicked
        const selectedSection = document.getElementById(selectedOption);
        if (selectedSection) {
            selectedSection.scrollIntoView({ behavior: "smooth" });
        }
    };
    if (selectedOption) {
        goButton.disabled = false;
    }
});

goButton.addEventListener('click', function(){
    categorySelect.value = '';
    optionSelect.value = '';
    optionSelect.disabled = true;
    goButton.disabled = true;
    goButton.style.visibility = 'hidden'


})

