const BASE_URL = "http://127.0.0.1:5000/api";

function print_cupcake(cupcake){
    return `
    <div cupcake_id=${cupcake.id}>
    <li>${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}</li>
    <img src="${cupcake.image}">
    </div>`
}

async function get_cupcakes(){
    const response= await axios.get(`${BASE_URL}/cupcakes`)
    for (let cupcakeData of response.data.cupcakes) {
        let newCupcake = $(print_cupcake(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
    }
}


$("#new-cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();
  
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();
  
    const newCupcakePost = await axios.post(`${BASE_URL}/cupcakes`, {
      flavor,
      rating,
      size,
      image
    });
  
    let newCupcake = $(print_cupcake(newCupcakePost.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
  });
$(get_cupcakes);