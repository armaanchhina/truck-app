const options = {
    insert:[
        {title: "Insert New Tractor Information", id: "insert-new-tractor-info"},
        {title: "Insert Repair Information", id: "insert-repair-info"},
    ],
    get: [
        {title: "Get Repair Information", id: "get-repair-info"},
        {title: "Get Tractor Information", id: "get-tractor-info"},
    ],
};

const categorySelect = document.getElementById('categorySelect');
const optionSelect = document.getElementById('optionSelect');
const goButton = document.getElementById('goButton');
const sumbit = document.getElementById

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

$(document).ready(function(){
    $('#tractorForm').on('submit', function(e) {
        e.preventDefault();  // Prevent the form from being submitted normally
        $.ajax({
            url: '/insert_tractor',
            type: 'POST',
            data: $(this).serialize(),  // Serialize the form data for sending
            success: function(response) {
                // This will show an alert box with the message from the server
                alert(response.message);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // Handle any errors here
                alert("An error occurred: " + errorThrown);
            }
        });
    });

    $('#repairForm').on('submit', function(e) {
        e.preventDefault();  // Prevent the form from being submitted normally
        $.ajax({
            url: '/insert_repair',
            type: 'POST',
            data: $(this).serialize(),  // Serialize the form data for sending
            success: function(response) {
                // This will show an alert box with the message from the server
                alert(response.message);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // Handle any errors here
                alert("An error occurred: " + errorThrown);
            }
        });
    });

});
  