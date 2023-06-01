function fetchCupcakes() {
    axios.get('/api/cupcakes')
        .then(function (response) {
            let cupcakes = response.data.cupcakes;
            let cupcakeList = $('#cupcake-list');
            cupcakeList.empty();

            cupcakes.forEach(function (cupcake) {
                let cupcakeItem = $('<li>').text(`Flavor: ${cupcake.flavor}, Size: ${cupcake.size}, Rating: ${cupcake.rating}, Image: ${cupcake.image}`);
                let deleteButton = $('<button>').text('Delete');
                deleteButton.click(function () {
                    deleteCupcake(cupcake.id);
                });
                cupcakeItem.append(deleteButton);
                cupcakeList.append(cupcakeItem);
            });
        })
        .catch(function (error) {
            console.error('Error fetching cupcakes:', error);
        });
}

// Function to handle form submission and add a new cupcake
function submitForm(event) {
    event.preventDefault();

    let flavor = $('#flavor').val();
    let size = $('#size').val();
    let rating = parseFloat($('#rating').val());
    let image = $('#image').val();

    axios.post('/api/cupcakes', {
        flavor: flavor,
        size: size,
        rating: rating,
        image: image
    })
        .then(function (response) {
            let cupcake = response.data.cupcake;
            let cupcakeItem = $('<li>').text(`Flavor: ${cupcake.flavor}, Size: ${cupcake.size}, Rating: ${cupcake.rating}, Image: ${cupcake.image}`);
            let deleteButton = $('<button>').text('Delete');
            deleteButton.click(function () {
                deleteCupcake(cupcake.id);
            });
            cupcakeItem.append(deleteButton);
            $('#cupcake-list').append(cupcakeItem);
        })
        .catch(function (error) {
            console.error('Error adding cupcake:', error);
        });

    // Reset the form fields after submission
    $('#cupcake-form')[0].reset();
}

// Function to delete a cupcake
function deleteCupcake(cupcakeId) {
    axios.delete(`/api/cupcakes/${cupcakeId}`)
        .then(function () {
            // Remove the cupcake from the list
            $(`li[data-cupcake-id="${cupcakeId}"]`).remove();
        })
        .catch(function (error) {
            console.error('Error deleting cupcake:', error);
        });
}

// Fetch cupcakes on page load
fetchCupcakes();

// Handle form submission
$('#cupcake-form').on('submit', submitForm);